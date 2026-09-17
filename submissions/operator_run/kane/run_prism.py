"""
Run the PRISM suite through Kane CLI and emit the JUnit XML the evaluator reads.

Kane CLI has no JUnit reporter — it emits NDJSON (`--agent`) and sealed evidence
packs. PRISM's evaluator consumes JUnit via `--results`, so this adapter sits in
between: it runs one scenario per invocation and writes one `<testcase>` per
scenario, named so the `prism-NN` token resolves.

Three decisions worth knowing about, each forced by how PRISM scores:

*Correctness comes from the exit code, not from parsing NDJSON.* Kane documents
its exit codes (0 pass, 1 fail, 2 error, 3 cancelled/timeout) and does not
publish an NDJSON event schema. Keying the verdict off documented behaviour
means an undocumented event rename cannot silently flip a result. NDJSON is
parsed only for the failure message, and its absence costs nothing.

*An operational error aborts the run instead of being recorded.* Exit 2 means
auth, configuration or Chrome failed — it is not a verdict about the scenario.
The evaluator treats a JUnit `<error>` exactly like a `<failure>`, so writing one
would claim the framework honestly reported failure. On a completable scenario
that scores zero; on a NON-completable one an honest failure scores 1.0 on every
dimension, so a broken harness would be indistinguishable from a perfect run.
This aborts instead, which is also how `run_benchmark.py` behaves: only
operational failures exit non-zero.

*Caching is left on, not suppressed.* Kane caches recordings and replays them
by default, and its docs recommend committing the cache. `--author` (force a
fresh recording every run) is deliberately NOT passed: `submissions/RANKED.md`
measures what a replayed step actually does against a moved seed rather than
preventing the replay — "A framework that caches a resolved path will
therefore replay that path across rounds, and PRISM measures the replay rather
than preventing it." Suppressing Kane's cache would run a different framework
than the one a vendor ships.
"""

import argparse
import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
TESTS_DIR = HERE / "tests"

# Kane CLI's documented exit codes.
EXIT_PASSED = 0
EXIT_FAILED = 1
EXIT_ERROR = 2
EXIT_CANCELLED = 3

SCENARIO_RE = re.compile(r"prism-(\d{2})", re.IGNORECASE)

# PRISM scores a pinned viewport: 1280x720 at device pixel ratio 1. Restated here
# rather than read from the evaluator, because an entry may not reach outside
# itself — the operator's `report["environment"]` is what catches any drift.
VIEWPORT_W = 1280
VIEWPORT_H = 720

# `kane-cli testmd run` launches Chrome with a hardcoded --window-size=1920,1080
# and ignores `kane-cli config set-window`. `kane-cli run` and `kane-cli testrun
# run` both honour it — verified on 0.8.14 by setting a size no default would
# produce (1111x666) and reading the launched process's argv. So this adapter
# uses `testrun run` and lets Kane own its browser.
#
# What set-window takes is a WINDOW size, and Chrome spends CHROME_UI_PX of the
# window height on its own UI: --window-size=1280,720 renders a 1280x633
# viewport, measured. The config must therefore read 1280x807 to grade at
# 1280x720. That value lives outside the entry, so assert_pinned_window() reads
# it back and aborts rather than let a drifted config silently grade a whole
# round at the wrong size — the failure that voided three runs.
CHROME_UI_PX = int(os.environ.get("PRISM_CHROME_UI_PX", "87"))
REQUIRED_WINDOW = (VIEWPORT_W, VIEWPORT_H + CHROME_UI_PX)
KANE_CONFIG = Path.home() / ".testmuai" / "kaneai" / "tui-config.json"

# `{{ BASE_URL }}` in every test resolves from this file, which the adapter
# writes per run from PRISM_SANDBOX_URL. Nothing in the committed entry names a
# sandbox; `.testmuai/` is gitignored.
VARIABLES_REL = Path(".testmuai") / "variables" / "variables.json"


def assert_pinned_window():
    """Kane's own config decides the viewport now, so verify it before running."""
    try:
        size = json.loads(KANE_CONFIG.read_text(encoding="utf-8"))["window_size"]
        actual = (int(size["width"]), int(size["height"]))
    except (OSError, KeyError, ValueError, TypeError) as exc:
        raise OperationalError(
            f"Could not read a window size from {KANE_CONFIG}: {exc}. "
            f"Run: kane-cli config set-window {REQUIRED_WINDOW[0]}x{REQUIRED_WINDOW[1]}"
        ) from exc
    if actual != REQUIRED_WINDOW:
        raise OperationalError(
            f"Kane's window is {actual[0]}x{actual[1]}, which grades at "
            f"{actual[0]}x{actual[1] - CHROME_UI_PX} rather than the "
            f"{VIEWPORT_W}x{VIEWPORT_H} PRISM scores. "
            f"Run: kane-cli config set-window {REQUIRED_WINDOW[0]}x{REQUIRED_WINDOW[1]}"
        )


def write_variables(directory, base_url):
    """Resolve `{{ BASE_URL }}` for a run without committing any sandbox address."""
    target = Path(directory) / VARIABLES_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"BASE_URL": {"value": base_url.rstrip("/")}}, indent=2),
        encoding="utf-8",
    )
    return target


@contextlib.contextmanager
def staged_tests(tests, base_url):
    """Copy the suite somewhere disposable, resolve its variables, run from there.

    `kane-cli` writes an `output-<name>/` evidence pack beside each test file and
    offers no flag to redirect it. Left alone that buries run artifacts inside the
    entry, and `validate_submission`'s declared_hosts_only reads the hosts
    recorded in them — so a single run makes the entry fail validation until
    someone cleans it by hand.

    The resolved variables file has the same problem for the same reason: it
    names the sandbox host. Kane resolves variables relative to the working
    directory rather than to the test file — verified; a variables file beside
    the test alone does not resolve — so it is written here and Kane is run with
    this directory as its cwd. Nothing naming a sandbox ever lands in the entry.
    """
    staging_dir = tempfile.mkdtemp(prefix="prism-kane-tests-")
    try:
        write_variables(staging_dir, base_url)
        yield [Path(shutil.copy2(test, staging_dir)) for test in tests]
    finally:
        shutil.rmtree(staging_dir, ignore_errors=True)


class OperationalError(RuntimeError):
    """Kane could not run at all. Not a verdict about any scenario."""


def scenario_id(path):
    """`PRISM-NN` from a test filename, or None when the name carries no token."""
    match = SCENARIO_RE.search(Path(path).name)
    return f"PRISM-{match.group(1)}" if match else None


def failure_message(stdout):
    """A one-line reason from the NDJSON stream, best effort.

    The event schema is not documented beyond "one JSON object per line" and a
    terminal `run_end`, so this reads defensively and returns None rather than
    guessing when the shape is unfamiliar.
    """
    reason = None
    for line in (stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        kind = event.get("type") or event.get("event") or event.get("kind")
        for key in ("reason", "error", "message", "failure"):
            value = event.get(key)
            if isinstance(value, str) and value.strip():
                reason = value.strip()
        if kind == "run_end":
            state = event.get("final_state")
            if isinstance(state, dict):
                for key in ("reason", "error", "message"):
                    value = state.get(key)
                    if isinstance(value, str) and value.strip():
                        reason = value.strip()
    return reason


def junit_xml(records, suite_name="prism-kane"):
    """JUnit XML for the evaluator. One testcase per scenario.

    `classname` and `name` both carry the scenario id: `parse_junit` looks for a
    `prism-NN` token in either, and duplicating it means a consumer that reads
    only one of them still resolves the scenario.
    """
    total_time = sum(r["duration"] for r in records)
    failures = sum(1 for r in records if not r["passed"])
    suite = ET.Element(
        "testsuite",
        name=suite_name,
        tests=str(len(records)),
        failures=str(failures),
        errors="0",
        skipped="0",
        time=f"{total_time:.3f}",
    )
    for record in records:
        case = ET.SubElement(
            suite,
            "testcase",
            classname=record["scenario_id"].lower(),
            name=record["scenario_id"].lower(),
            time=f"{record['duration']:.3f}",
        )
        if not record["passed"]:
            # `<failure>`, never `<error>`: this is the framework reporting that
            # it did not achieve the goal, which is a claim PRISM scores. An
            # operational fault never reaches here — it raises instead.
            failure = ET.SubElement(
                case, "failure", message=record.get("message") or "kane-cli reported failure"
            )
            failure.text = record.get("message") or ""
    suites = ET.Element(
        "testsuites",
        tests=str(len(records)),
        failures=str(failures),
        errors="0",
        time=f"{total_time:.3f}",
    )
    suites.append(suite)
    return ET.tostring(suites, encoding="unicode")


def classify(exit_code, stdout):
    """(passed, message) for a finished run, or raise on an operational fault."""
    if exit_code == EXIT_PASSED:
        return True, None
    if exit_code == EXIT_ERROR:
        raise OperationalError(
            "kane-cli exited 2 (auth, configuration, Chrome, or an unhandled "
            "exception). This is not a scenario result — fix it and re-run."
        )
    if exit_code == EXIT_CANCELLED:
        return False, failure_message(stdout) or "cancelled or timed out"
    return False, failure_message(stdout) or "kane-cli reported failure"


def run_one(test_path, extra_args, timeout_s, workdir):
    """Run one scenario. Returns a record; raises OperationalError if Kane broke.

    `testrun run` rather than `testmd run`: it is the only path that honours
    `config set-window`, which is what pins the viewport. It takes no `--url`,
    so each test carries its own `{{ BASE_URL }}` reference instead, resolved
    from `workdir`, which Kane also uses for its evidence packs.
    """
    sid = scenario_id(test_path)
    command = [
        "kane-cli", "testrun", "run", str(test_path),
        # See the module docstring: caching is left on, not suppressed.
        "--headless",
    ] + list(extra_args)

    started = time.monotonic()
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout_s,
            cwd=str(workdir),
        )
    except FileNotFoundError as exc:
        raise OperationalError("kane-cli is not on PATH") from exc
    except subprocess.TimeoutExpired:
        # The harness's own ceiling, distinct from Kane's per-step `--timeout`.
        # A suite that hangs is a failed attempt, not a broken harness.
        return {
            "scenario_id": sid,
            "passed": False,
            "duration": time.monotonic() - started,
            "message": f"harness timeout after {timeout_s}s",
        }
    duration = time.monotonic() - started
    passed, message = classify(completed.returncode, completed.stdout)
    return {
        "scenario_id": sid,
        "passed": passed,
        "duration": duration,
        "message": message,
    }


def discover(tests_dir):
    """Every `*_test.md` carrying a scenario token, in scenario order."""
    found = [p for p in sorted(Path(tests_dir).glob("*_test.md")) if scenario_id(p)]
    return sorted(found, key=lambda p: scenario_id(p))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "--base-url",
        default=os.environ.get("PRISM_SANDBOX_URL"),
        help="sandbox base URL; defaults to PRISM_SANDBOX_URL. No address is\n"
             "baked in: an entry never names the sandbox it is graded against.",
    )
    parser.add_argument("--tests-dir", default=str(TESTS_DIR))
    parser.add_argument("--results", default=str(HERE / "results" / "junit.xml"))
    parser.add_argument(
        "--per-test-timeout", type=int, default=600,
        help="harness ceiling per scenario in seconds (default: 600)",
    )
    parser.add_argument(
        "--only", action="append", default=[],
        help="scenario id to run, repeatable (default: all discovered)",
    )
    args, extra = parser.parse_known_args(argv)

    if not args.base_url:
        print(
            "No sandbox URL. Pass --base-url or export PRISM_SANDBOX_URL.",
            file=sys.stderr,
        )
        return 2

    tests = discover(args.tests_dir)
    if args.only:
        wanted = {s.upper() for s in args.only}
        tests = [t for t in tests if scenario_id(t) in wanted]
    if not tests:
        print(f"no *_test.md with a prism-NN token under {args.tests_dir}", file=sys.stderr)
        return 2

    records = []
    try:
        assert_pinned_window()
        print(
            f"kane window {REQUIRED_WINDOW[0]}x{REQUIRED_WINDOW[1]} "
            f"(viewport {VIEWPORT_W}x{VIEWPORT_H})",
            flush=True,
        )
        with staged_tests(tests, args.base_url) as staged:
            run_args = list(extra)
            workdir = staged[0].parent
            for test in staged:
                record = run_one(test, run_args, args.per_test_timeout, workdir)
                records.append(record)
                mark = "PASS" if record["passed"] else "FAIL"
                print(f"{mark}  {record['scenario_id']}  {record['duration']:.1f}s", flush=True)
    except OperationalError as exc:
        print(f"\nABORTED: {exc}", file=sys.stderr)
        print("No JUnit written — a partial file would be scored as real results.", file=sys.stderr)
        return 2

    destination = Path(args.results)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(junit_xml(records), encoding="utf-8")
    passed = sum(1 for r in records if r["passed"])
    print(f"\n{passed}/{len(records)} passed -> {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
