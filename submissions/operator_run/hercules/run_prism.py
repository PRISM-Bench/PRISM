#!/usr/bin/env python3
"""Drive the 50 PRISM scenarios through testzeus-hercules, one at a time.

    PRISM_SANDBOX_URL=<the round's sandbox> python3 run_prism.py

Hercules takes one feature per invocation, so there is no suite-level runner to
configure: this file IS the suite runner, and the one-scenario-at-a-time rule
holds because the loop below is serial. Nothing here is parallel and nothing
should become parallel — several scenarios keep a single server-side serve
timestamp, and a second concurrent load of one scenario overwrites the first's
clock, which can grade a settled interaction as unsettled.

**It merges Hercules' own JUnit rather than deriving pass/fail itself.** Hercules
writes a real JUnit file per feature (`utils/junit_helper.py`), so the verdict
that reaches the evaluator is the framework's own. Re-deriving it from exit codes
would mean a misread failure becomes a False Heal recorded against Hercules for
a bug in this file, and the False-Heal count is the statistic PRISM is most
careful about.

Three details are load-bearing:

1. **`--project-base` points outside the entry.** Hercules roots `output/`,
   `proofs/` and `log_files/` at `PROJECT_SOURCE_ROOT`, and proofs contain
   network logs naming the sandbox. `validate_submission`'s `declared_hosts_only`
   reads hosts out of files inside the entry, so one run with artifacts landing
   here would fail the entry it describes.
2. **`{{BASE_URL}}` is resolved into a staged copy**, never in place. No sandbox
   address is ever written into a tracked file.
3. **An operational fault writes no JUnit at all.** A partial file would be
   scored as real results, and per `submissions/RANKED.md` a round that does not
   execute all 50 scenarios is reported incomplete rather than scored.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
# stdlib ET rather than defusedxml, deliberately. The file parsed here is the
# JUnit Hercules just wrote in this container, and `evaluators/runner/
# junit_results.py` parses the same bytes with junitparser moments later — so
# hardening only this reader would close nothing, while adding a dependency
# widens the entry's install surface. Python's ET does not fetch external
# entities; if the threat model ever changes, it changes for the evaluator first.
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
FEATURES_DIR = HERE / "features"
BASE_URL_PLACEHOLDER = "{{BASE_URL}}"

# The pinned environment PRISM scores at. Hercules takes `width,height` and
# drives headless Chromium, so this is the viewport directly rather than a
# window size the browser then subtracts its own chrome from.
REQUIRED_RESOLUTION = "1280,720"

EXPECTED_SCENARIOS = 50


class OperationalError(Exception):
    """The harness broke. Not a scenario result, and not scoreable."""


def assert_pinned_environment():
    """Refuse to start unless the settings that decide honesty are set.

    Each of these is silent when wrong, which is why they are checked rather
    than documented. `AUTO_MODE` is the sharpest: unset, Hercules treats the run
    as manual and asks for an email address, which stalls a 300-run round
    instead of failing it.
    """
    required = {
        "BROWSER_RESOLUTION": REQUIRED_RESOLUTION,
        "HEADLESS": "true",
        "AUTO_MODE": "1",
        "ENABLE_TELEMETRY": "0",
        "RECORD_VIDEO": "false",
        "TAKE_SCREENSHOTS": "false",
        "CAPTURE_NETWORK": "false",
    }
    wrong = {
        key: os.environ.get(key)
        for key, expected in required.items()
        if os.environ.get(key) != expected
    }
    if wrong:
        detail = ", ".join(f"{k}={v!r} (want {required[k]!r})" for k, v in sorted(wrong.items()))
        raise OperationalError(
            f"the run environment is not pinned: {detail}. These decide the graded "
            "viewport, whether the run stalls on an email prompt, and whether "
            "capture overhead distorts the timing-sensitive scenarios."
        )
    if not os.environ.get("LLM_MODEL_NAME") or not os.environ.get("LLM_MODEL_API_KEY"):
        raise OperationalError(
            "LLM_MODEL_NAME and LLM_MODEL_API_KEY must both be set; Hercules "
            "refuses to start without them and the model is published on the row."
        )


def scenario_id(path):
    """`PRISM-NN` from `prism-NN.feature`."""
    return path.stem.upper()


def discover(features_dir):
    found = sorted(Path(features_dir).glob("prism-*.feature"))
    if len(found) != EXPECTED_SCENARIOS:
        raise OperationalError(
            f"expected {EXPECTED_SCENARIOS} feature files under {features_dir}, "
            f"found {len(found)}. A round covers the whole suite or it is not a round."
        )
    return found


@contextmanager
def staged_feature(feature, base_url):
    """One feature with its base URL resolved, in a disposable directory.

    Hercules expects `input/` and `test_data/` beside the project base, so the
    staging directory mirrors that layout; `output/`, `proofs/` and `log_files/`
    are created by Hercules underneath it.
    """
    staging = Path(tempfile.mkdtemp(prefix=f"prism-hercules-{scenario_id(feature).lower()}-"))
    try:
        (staging / "input").mkdir()
        (staging / "test_data").mkdir()
        (staging / "test_data" / "td.txt").touch()
        target = staging / "input" / feature.name
        target.write_text(
            feature.read_text(encoding="utf-8").replace(BASE_URL_PLACEHOLDER, base_url.rstrip("/")),
            encoding="utf-8",
        )
        yield staging, target
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def collect_testcases(staging):
    """Every `<testcase>` Hercules wrote for one feature.

    It writes them under `<project base>/output/<timestamp>/`, so the glob is
    recursive rather than assuming the timestamp.

    The pattern is `*result*.xml`, not the `{feature}_{scenario}_results.xml` that
    `utils/junit_helper.py` builds — that is a different code path. What actually
    lands is `__main__.py`'s `<feature file name>_result.xml`, singular, named
    from the file rather than from the Gherkin. Verified against a real run; the
    plural glob matched nothing and aborted a scenario that had in fact passed.
    """
    cases = []
    for xml_path in sorted((staging / "output").rglob("*result*.xml")):
        try:
            root = ET.parse(xml_path).getroot()
        except ET.ParseError as exc:
            raise OperationalError(f"{xml_path.name} is not parseable JUnit: {exc}") from exc
        cases.extend(root.iter("testcase"))
    return cases


def run_one(feature, base_url, timeout_s):
    """Run one scenario. Returns its `<testcase>` elements.

    An empty return is an operational fault, not a failure: Hercules writes a
    JUnit file for a failing scenario too, so producing none means it never got
    far enough to have an opinion.
    """
    sid = scenario_id(feature)
    with staged_feature(feature, base_url) as (staging, staged):
        command = [
            "testzeus-hercules",
            "--input-file", str(staged),
            "--project-base", str(staging),
            "--output-path", str(staging / "output"),
            "--test-data-path", str(staging / "test_data"),
        ]
        started = time.monotonic()
        try:
            completed = subprocess.run(
                command, capture_output=True, text=True, timeout=timeout_s, cwd=str(staging)
            )
        except FileNotFoundError as exc:
            raise OperationalError(
                "testzeus-hercules is not on PATH. Run the entry's `setup` first."
            ) from exc
        except subprocess.TimeoutExpired:
            raise OperationalError(
                f"{sid} exceeded the {timeout_s}s harness ceiling. A hung scenario "
                "leaves the round incomplete rather than failed."
            ) from None

        cases = collect_testcases(staging)
        if not cases:
            tail = "\n".join((completed.stderr or completed.stdout or "").strip().splitlines()[-15:])
            raise OperationalError(
                f"{sid} produced no JUnit (exit {completed.returncode}). Hercules "
                f"writes one for a failing scenario too, so this is a harness "
                f"fault rather than a result:\n{tail}"
            )
        # Detach from the source tree before the staging directory is removed.
        return [ET.fromstring(ET.tostring(case)) for case in cases], time.monotonic() - started


def merged_suite(cases, total_time, suite_name="prism-hercules"):
    """One `<testsuite>` carrying every scenario's testcase.

    `classname` and `name` both already carry the scenario id, because the
    generator puts it in the Gherkin `Feature` and `Scenario` lines and
    Hercules maps them to exactly those attributes. Nothing is rewritten here —
    a consumer reads the framework's own verdict.
    """
    failures = sum(1 for case in cases if case.find("failure") is not None)
    errors = sum(1 for case in cases if case.find("error") is not None)
    suite = ET.Element(
        "testsuite",
        name=suite_name,
        tests=str(len(cases)),
        failures=str(failures),
        errors=str(errors),
        skipped="0",
        time=f"{total_time:.3f}",
    )
    suite.extend(cases)
    return suite


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--base-url",
        default=os.environ.get("PRISM_SANDBOX_URL"),
        help="sandbox base URL; defaults to PRISM_SANDBOX_URL. No address is\n"
             "baked in: an entry never names the sandbox it is graded against.",
    )
    parser.add_argument("--features-dir", default=str(FEATURES_DIR))
    parser.add_argument("--results", default=str(HERE / "results" / "junit.xml"))
    parser.add_argument(
        "--per-test-timeout", type=int, default=900,
        help="harness ceiling per scenario in seconds (default: 900)",
    )
    parser.add_argument(
        "--only", action="append", default=[],
        help="scenario id to run, repeatable (default: all 50)",
    )
    args = parser.parse_args(argv)

    if not args.base_url:
        print("No sandbox URL. Pass --base-url or export PRISM_SANDBOX_URL.", file=sys.stderr)
        return 2

    cases, elapsed = [], 0.0
    try:
        assert_pinned_environment()
        features = discover(args.features_dir)
        if args.only:
            wanted = {s.upper() for s in args.only}
            features = [f for f in features if scenario_id(f) in wanted]
            if not features:
                raise OperationalError(f"--only matched nothing: {sorted(wanted)}")
        print(f"hercules viewport {REQUIRED_RESOLUTION}, {len(features)} scenario(s), serial", flush=True)

        for feature in features:
            sid = scenario_id(feature)
            scenario_cases, duration = run_one(feature, args.base_url, args.per_test_timeout)
            cases.extend(scenario_cases)
            elapsed += duration
            failed = any(c.find("failure") is not None or c.find("error") is not None
                         for c in scenario_cases)
            print(f"{'FAIL' if failed else 'PASS'}  {sid}  {duration:.1f}s", flush=True)
    except OperationalError as exc:
        print(f"\nABORTED: {exc}", file=sys.stderr)
        print("No JUnit written — a partial file would be scored as real results.", file=sys.stderr)
        return 2

    destination = Path(args.results)
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(merged_suite(cases, elapsed)).write(
        destination, encoding="utf-8", xml_declaration=True
    )
    passed = sum(1 for c in cases
                 if c.find("failure") is None and c.find("error") is None)
    print(f"\n{passed}/{len(cases)} passed -> {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
