"""
Static-shape validator for a PRISM submission entry.

Checks what can be seen without executing anything: that `metadata.yaml` carries
the contract, that the test files cover all 50 scenarios exactly once, that
it names no host it did not declare, and that the run declaration stays inside
the entry.

Deliberately does NOT execute `run.setup` or `run.command`. This script is
pointed at entries from strangers — a vendor's submitted archive at intake, or
whatever a PR put in the tree — and installing and running a submitted command
is arbitrary code execution. The failure it would catch (a broken command) is
caught by the operator on the first quarterly run anyway.

Ships to the public repo. Scenario IDs come from `data/scenarios/*.yml`, which
holds the full specs here and the lean specs there — same IDs, so this module is
correct in both repos with no conditional and no private import.

    python3 -m scripts.validate_submission submissions/operator_run/momentic/2026-Q3
    python3 -m scripts.validate_submission --all
"""

import argparse
import re
import sys
from collections import namedtuple
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

Failure = namedtuple("Failure", "entry file rule message")

_REQUIRED_TOP_LEVEL = (
    "framework",
    "version",
    "contact",
    "submission_date",
    "scope",
    "tests",
    "run",
    "network",
)
# `full` is the only scope: every ranked round covers all 50 scenarios. The
# enum stays a tuple so a submission naming a retired scope fails loudly rather
# than being silently read as full.
_VALID_SCOPES = ("full",)


def scenario_ids():
    """Every scenario ID the repo defines, from data/scenarios/PRISM-NN.yml."""
    return {path.stem for path in (REPO_ROOT / "data" / "scenarios").glob("PRISM-*.yml")}


def check_metadata_schema(entry, metadata):
    """Every required key present, with the right shape."""
    failures = []

    def fail(message):
        failures.append(Failure(entry.name, "metadata.yaml", "metadata_schema", message))

    for key in _REQUIRED_TOP_LEVEL:
        if key not in metadata:
            fail(f"missing required key '{key}'")
    if failures:
        return failures

    if metadata["scope"] not in _VALID_SCOPES:
        fail(f"scope must be one of {list(_VALID_SCOPES)}, got {metadata['scope']!r}")
    tests = metadata["tests"] if isinstance(metadata["tests"], dict) else {}
    glob_pattern = tests.get("glob")
    if not isinstance(glob_pattern, str) or not glob_pattern:
        fail("tests.glob is required and must be a non-empty string")
    run = metadata["run"] if isinstance(metadata["run"], dict) else {}
    for key in ("command", "results"):
        value = run.get(key)
        if not isinstance(value, str) or not value:
            fail(f"run.{key} is required and must be a non-empty string")
    setup = run.get("setup")
    if setup is not None and not isinstance(setup, str):
        fail("run.setup must be a string when present")
    network = metadata["network"] if isinstance(metadata["network"], dict) else {}
    if not isinstance(network.get("allowlist"), list):
        fail("network.allowlist is required and must be a list (use [] to declare none)")

    return failures


# Directories that are build output or installed dependencies, not authored
# entry content. Scanning them produces noise and false positives.
# Build output and installed dependencies, not authored content. `test-results`
# and `playwright-report` are where Momentic and Playwright write HAR logs,
# console dumps and traces — which record every host the run touched, including
# the sandbox itself. Scanning them fails an honest entry for its own debug
# artifacts, which is how this list grew: the operator's own entry stopped
# validating the first time anyone ran it.
_SKIP_DIRS = frozenset(
    {
        "node_modules",
        "reports",
        "test-results",
        "playwright-report",
        ".git",
        "__pycache__",
        ".momentic",
    }
)

# Markdown is prose, not behaviour. A README's link to the vendor's own docs is
# not an egress target, and requiring it in network.allowlist would overload an
# egress declaration with documentation hosts.
_SKIP_SUFFIXES = frozenset({".md"})

# Generated dependency manifests, same category as node_modules: their
# registry URLs are resolver output, not hosts the entry chose to name.
_SKIP_NAMES = frozenset(
    {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "uv.lock"}
)

_URL_LITERAL = re.compile(r"\bhttps?://([^\s\"\'`/\\)>\]]+)", re.IGNORECASE)

_SCENARIO_TOKEN = re.compile(r"prism-(\d{2})(?!\d)", re.IGNORECASE)


def _entry_files(entry):
    """Authored, executable entry content — no build output, no Markdown.

    This module is pointed at entries from strangers. Symlinks reaching outside
    the entry could read arbitrary files on whatever machine runs it — a CI
    runner, or the operator's own box at intake, which is the worse of the two.
    Skip any path that resolves outside the entry directory.
    """
    entry_resolved = entry.resolve()
    for path in sorted(entry.rglob("*")):
        if not path.is_file():
            continue
        # Containment check: resolved path must stay under entry root.
        # Catches symlinks and any other escape mechanisms.
        try:
            path.resolve().relative_to(entry_resolved)
        except ValueError:
            continue
        if _SKIP_DIRS.intersection(path.relative_to(entry).parts):
            continue
        if path.suffix.lower() in _SKIP_SUFFIXES or path.name in _SKIP_NAMES:
            continue
        yield path


def check_declared_hosts_only(entry, metadata):
    """Every concrete host the entry names is one it declared.

    An allow-list, not a denylist: forbidding `localhost` and friends passes a
    vendor's own staging sandbox by default and fails silently. The templated
    forms (`{{ env.BASE_URL }}/…`, `${PRISM_SANDBOX_URL}`) carry no scheme+host,
    so they never match and need no special case.
    """
    allowed = {str(host).lower().split(":")[0] for host in metadata["network"]["allowlist"]}
    failures = []
    for path in _entry_files(entry):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        relative = path.relative_to(entry).as_posix()
        seen = set()
        for match in _URL_LITERAL.finditer(text):
            # Strip any userinfo prefix, then the port.
            host = match.group(1).rsplit("@", 1)[-1].split(":")[0].lower()
            if host in allowed or host in seen:
                continue
            seen.add(host)
            failures.append(
                Failure(
                    entry.name,
                    relative,
                    "declared_hosts_only",
                    f"names host '{host}', which is not in network.allowlist; "
                    "resolve the sandbox base URL from PRISM_SANDBOX_URL",
                )
            )
    return failures


def check_scenario_coverage(entry, metadata):
    """tests.glob resolves to exactly the 50 scenarios, one file each."""
    expected = scenario_ids()
    failures = []
    seen = {}

    try:
        matches = sorted(entry.glob(metadata["tests"]["glob"]))
    except (ValueError, NotImplementedError, OSError) as exc:
        return [
            Failure(
                entry.name,
                "metadata.yaml",
                "scenario_coverage",
                f"tests.glob is not a valid glob pattern: {exc}",
            )
        ]

    for path in matches:
        relative = path.relative_to(entry).as_posix()
        match = _SCENARIO_TOKEN.search(path.name)
        if match is None:
            failures.append(
                Failure(
                    entry.name,
                    relative,
                    "scenario_coverage",
                    "filename carries no prism-NN token",
                )
            )
            continue
        scenario_id = f"PRISM-{match.group(1)}"
        seen.setdefault(scenario_id, []).append(relative)

    for scenario_id, paths in sorted(seen.items()):
        if len(paths) > 1:
            failures.append(
                Failure(
                    entry.name,
                    paths[0],
                    "scenario_coverage",
                    f"{scenario_id} has {len(paths)} test files: {', '.join(paths)}",
                )
            )

    missing = sorted(expected - set(seen))
    if missing:
        failures.append(
            Failure(
                entry.name,
                "metadata.yaml",
                "scenario_coverage",
                f"no test file for {', '.join(missing)}",
            )
        )

    extra = sorted(set(seen) - expected)
    if extra:
        failures.append(
            Failure(
                entry.name,
                "metadata.yaml",
                "scenario_coverage",
                f"names {', '.join(extra)}, which the benchmark does not define",
            )
        )

    return failures


# A bare token starting with `/` is an absolute path. A path may be glued to
# `=`, a quote, or a shell operator. Matching on token boundaries keeps
# `--reporter-dir reports` and `a/b` from tripping the check.
_ABSOLUTE_PATH = re.compile(r"(?:^|[\s=\"'>;&|(])/\S")
_PARENT_TRAVERSAL = re.compile(r"(?:^|[\s/=\"'>;&|(])\.\.(?:/|\s|$)")


def check_paths_stay_inside_entry(entry, metadata):
    """The run declaration cannot reach outside its own directory.

    The operator executes `run.command` with the entry as the working directory.
    A traversal or absolute path would depend on the operator's machine layout,
    which no vendor can know.
    """
    failures = []
    run = metadata["run"]
    for key in ("setup", "command", "results"):
        value = run.get(key)
        if not value:
            continue
        for label, pattern in (
            ("parent traversal", _PARENT_TRAVERSAL),
            ("absolute path", _ABSOLUTE_PATH),
        ):
            if pattern.search(value):
                failures.append(
                    Failure(
                        entry.name,
                        "metadata.yaml",
                        "paths_stay_inside_entry",
                        f"run.{key} contains a {label}; it runs with the entry as cwd",
                    )
                )
                break
    return failures


CHECKS = (
    ("metadata_schema", check_metadata_schema),
    ("scenario_coverage", check_scenario_coverage),
    ("declared_hosts_only", check_declared_hosts_only),
    ("paths_stay_inside_entry", check_paths_stay_inside_entry),
)


def validate_entry(entry):
    """Run every check against one entry directory.

    A schema failure short-circuits: every later check reads keys the schema
    check is what guarantees are present, so running them on a malformed
    metadata would raise instead of reporting.
    """
    metadata_path = entry / "metadata.yaml"
    try:
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [Failure(entry.name, "metadata.yaml", "metadata_schema", str(exc))]
    if not isinstance(metadata, dict):
        return [
            Failure(entry.name, "metadata.yaml", "metadata_schema", "not a YAML mapping")
        ]

    failures = []
    for name, check in CHECKS:
        found = check(entry, metadata)
        failures.extend(found)
        if found and name == "metadata_schema":
            break
    return failures


def discover_entries(root=None):
    """Every directory under submissions/ that declares a metadata.yaml.

    Skips the same build-output/dependency directories `_entry_files` does —
    a vendor who commits `node_modules/` should not turn a dependency's own
    `metadata.yaml` into a phantom entry. `root` defaults to the repo's
    `submissions/` directory; a test may pass a fixture directory instead.
    """
    root = Path(root) if root is not None else REPO_ROOT / "submissions"
    return sorted(
        p.parent
        for p in root.rglob("metadata.yaml")
        if not _SKIP_DIRS.intersection(p.relative_to(root).parts)
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("entries", nargs="*", type=Path, help="entry directories")
    parser.add_argument("--all", action="store_true", help="validate every entry")
    args = parser.parse_args(argv)

    entries = discover_entries() if args.all else args.entries
    if not entries:
        if not args.all:
            parser.error("pass one or more entry directories, or --all")
        # Finding nothing under --all is success, not a usage error. The public
        # tree ships no submission entry at all — `submissions/TEMPLATE/` names
        # its file `metadata.example.yaml` so `discover_entries` skips it — and
        # public CI runs `--all`, which would otherwise be red from day one.
        print("no submission entries found; nothing to validate")
        return 0

    failures = []
    for entry in entries:
        failures.extend(validate_entry(entry))

    for failure in failures:
        print(f"{failure.entry}/{failure.file}: [{failure.rule}] {failure.message}")
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"{len(entries)} entr(y/ies) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
