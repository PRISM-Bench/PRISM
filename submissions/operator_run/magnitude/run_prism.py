#!/usr/bin/env python3
"""Drive the 50 PRISM scenarios through Magnitude, one invocation per scenario.

    PRISM_SANDBOX_URL=<the round's sandbox> python3 run_prism.py

Magnitude has **no JUnit reporter** — there is no `junit`, `xml` or `reporter`
anywhere in `magnitude-test@0.3.13` — while PRISM's evaluator reads JUnit. So this
file is a CLI-to-JUnit adapter, the same role `kane/run_prism.py` fills.

**The verdict comes from the exit code, not from parsing output.** The CLI takes a
`[filter]` glob, so one scenario per invocation yields that scenario's own
`process.exit(overallSuccess ? 0 : 1)`. Keying off a documented exit code rather
than scraping prose matters: a misread line would turn a failure into a reported
pass, which is a False Heal recorded against Magnitude for a bug in this file, and
the False-Heal count is the statistic PRISM promises is least gameable.

Three more details are load-bearing:

1. **One at a time, and never parallel.** `-w/--workers` defaults to 1 and is left
   alone. Several scenarios keep a single server-side serve timestamp, and a
   second concurrent load of one scenario overwrites the first's clock.
2. **`--no-fail-fast` on every invocation.** Magnitude aborts the run at the first
   failure by default. Per invocation that would be harmless, but passing it makes
   the intent explicit and survives someone later batching the filter.
3. **An operational fault writes no JUnit at all.** A partial file would be scored
   as real results, and per `submissions/RANKED.md` a round that does not execute
   all 50 scenarios is reported incomplete rather than scored.
"""

import argparse
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
TESTS_DIR = HERE / "tests"

EXPECTED_SCENARIOS = 50

# Magnitude's documented exit codes: 0 when every test in the invocation passed,
# 1 otherwise. Anything else is the process failing rather than reporting.
EXIT_PASSED = 0
EXIT_FAILED = 1


class OperationalError(Exception):
    """The harness broke. Not a scenario result, and not scoreable."""


def scenario_id(path):
    """`PRISM-NN` from `prism-NN.mag.ts` — note `Path.stem` leaves `.mag`."""
    return path.name.split(".")[0].upper()


def discover(tests_dir):
    found = sorted(Path(tests_dir).glob("prism-*.mag.ts"))
    if len(found) != EXPECTED_SCENARIOS:
        raise OperationalError(
            f"expected {EXPECTED_SCENARIOS} test files under {tests_dir}, found "
            f"{len(found)}. A round covers the whole suite or it is not a round."
        )
    return found


def assert_pinned_environment():
    """Refuse to start without what the config and the model need.

    The viewport itself is pinned in `magnitude.config.ts` rather than here,
    because Magnitude takes Playwright context options directly; the sandbox
    records what the browser actually reported either way.
    """
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise OperationalError(
            "OPENROUTER_API_KEY is not set. magnitude.config.ts reads it for the "
            "model, and the model is published on the row."
        )
    if not (HERE / "magnitude.config.ts").exists():
        raise OperationalError("magnitude.config.ts is missing from the entry")


def run_one(test_path, base_url, timeout_s):
    """Run one scenario. Returns (passed, message, duration)."""
    sid = scenario_id(test_path)
    relative = test_path.relative_to(HERE).as_posix()
    command = ["npx", "magnitude", relative, "--plain", "--no-fail-fast"]
    environment = dict(os.environ, PRISM_SANDBOX_URL=base_url)

    started = time.monotonic()
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout_s,
            cwd=str(HERE), env=environment,
        )
    except FileNotFoundError as exc:
        raise OperationalError("npx is not on PATH. Run the entry's setup first.") from exc
    except subprocess.TimeoutExpired:
        # The harness's own ceiling. A suite that hangs is a failed attempt, not
        # a broken harness, so this is a result rather than an abort.
        return False, f"harness timeout after {timeout_s}s", time.monotonic() - started

    duration = time.monotonic() - started
    if completed.returncode == EXIT_PASSED:
        return True, None, duration
    if completed.returncode == EXIT_FAILED:
        return False, _failure_message(completed), duration

    tail = "\n".join((completed.stderr or completed.stdout or "").strip().splitlines()[-15:])
    raise OperationalError(
        f"{sid}: magnitude exited {completed.returncode}, which is neither pass "
        f"nor fail. That is the process failing rather than reporting a result, "
        f"so it is not a verdict about this scenario:\n{tail}"
    )


def _failure_message(completed):
    """A short reason for the JUnit `<failure>` body, from Magnitude's own output."""
    text = (completed.stdout or "").strip() or (completed.stderr or "").strip()
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()[:500]
    return "magnitude reported failure"


def junit_xml(records, suite_name="prism-magnitude"):
    """JUnit for the evaluator. One testcase per scenario.

    `classname` and `name` both carry the scenario id: the evaluator looks for a
    `prism-NN` token in either, and duplicating it means a consumer reading only
    one of them still resolves the scenario.
    """
    total = sum(r["duration"] for r in records)
    failures = sum(1 for r in records if not r["passed"])
    suite = ET.Element(
        "testsuite", name=suite_name, tests=str(len(records)),
        failures=str(failures), errors="0", skipped="0", time=f"{total:.3f}",
    )
    for record in records:
        case = ET.SubElement(
            suite, "testcase",
            classname=record["scenario_id"], name=record["scenario_id"],
            time=f"{record['duration']:.3f}",
        )
        if not record["passed"]:
            failure = ET.SubElement(case, "failure", message=record["message"] or "failed")
            failure.text = record["message"] or "failed"
    return suite


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
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
        help="scenario id to run, repeatable (default: all 50)",
    )
    args = parser.parse_args(argv)

    if not args.base_url:
        print("No sandbox URL. Pass --base-url or export PRISM_SANDBOX_URL.", file=sys.stderr)
        return 2

    records = []
    try:
        assert_pinned_environment()
        tests = discover(args.tests_dir)
        if args.only:
            wanted = {s.upper() for s in args.only}
            tests = [t for t in tests if scenario_id(t) in wanted]
            if not tests:
                raise OperationalError(f"--only matched nothing: {sorted(wanted)}")
        print(f"magnitude: {len(tests)} scenario(s), serial, one invocation each", flush=True)

        for test_path in tests:
            sid = scenario_id(test_path)
            passed, message, duration = run_one(test_path, args.base_url, args.per_test_timeout)
            records.append(
                {"scenario_id": sid, "passed": passed, "message": message, "duration": duration}
            )
            print(f"{'PASS' if passed else 'FAIL'}  {sid}  {duration:.1f}s", flush=True)
    except OperationalError as exc:
        print(f"\nABORTED: {exc}", file=sys.stderr)
        print("No JUnit written — a partial file would be scored as real results.", file=sys.stderr)
        return 2

    destination = Path(args.results)
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(junit_xml(records)).write(
        destination, encoding="utf-8", xml_declaration=True
    )
    passed = sum(1 for r in records if r["passed"])
    print(f"\n{passed}/{len(records)} passed -> {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
