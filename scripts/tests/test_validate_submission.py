import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from scripts import validate_submission
from scripts.validate_submission import (
    check_declared_hosts_only,
    check_metadata_schema,
    check_paths_stay_inside_entry,
    check_scenario_coverage,
    discover_entries,
    main,
    scenario_ids,
    validate_entry,
)

VALID_METADATA = {
    "framework": "example",
    "version": "2026-Q3",
    "contact": "you@example.com",
    "submission_date": "2026-07-30",
    "scope": "full",
    "tests": {"glob": "web/prism-*.test.yaml"},
    "run": {
        "command": "npx example run --reporter junit --reporter-dir reports",
        "results": "reports/*.xml",
    },
    "network": {"allowlist": ["api.example.com"]},
}


def write_entry(root, metadata=VALID_METADATA, scenario_ids_=(), name="entry"):
    """Build a submission entry on disk and return its path."""
    entry = Path(root) / name
    (entry / "web").mkdir(parents=True)
    (entry / "metadata.yaml").write_text(yaml.safe_dump(metadata), encoding="utf-8")
    for scenario_id in scenario_ids_:
        number = scenario_id.split("-")[1]
        (entry / "web" / f"prism-{number}.test.yaml").write_text(
            "steps:\n  - act: Do the task.\n", encoding="utf-8"
        )
    return entry


ALL_IDS = tuple(f"PRISM-{n:02d}" for n in range(1, 51))


class MetadataSchemaTests(unittest.TestCase):
    def test_valid_metadata_produces_no_failures(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root)
            self.assertEqual(check_metadata_schema(entry, VALID_METADATA), [])

    def test_missing_required_key_is_reported_by_name(self):
        metadata = {k: v for k, v in VALID_METADATA.items() if k != "network"}
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            failures = check_metadata_schema(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("network", failures[0].message)

    def test_empty_allowlist_is_valid_but_missing_key_is_not(self):
        metadata = dict(VALID_METADATA, network={"allowlist": []})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            self.assertEqual(check_metadata_schema(entry, metadata), [])

    def test_unknown_scope_is_rejected(self):
        metadata = dict(VALID_METADATA, scope="partial")
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            failures = check_metadata_schema(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("scope", failures[0].message)

    def test_the_retired_practice_scope_is_rejected(self):
        """`practice` was a valid scope until the practice set was removed. An
        entry still declaring it must fail rather than be read as `full`."""
        metadata = dict(VALID_METADATA, scope="practice")
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            failures = check_metadata_schema(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("scope", failures[0].message)

    def test_non_string_tests_glob_is_rejected(self):
        """A truthy non-string (e.g. `glob: 123`) must not pass the schema
        check and then blow up in a later regex/glob call."""
        metadata = dict(VALID_METADATA, tests={"glob": 123})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            failures = check_metadata_schema(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("tests.glob", failures[0].message)

    def test_non_string_run_command_is_rejected(self):
        metadata = dict(VALID_METADATA, run={**VALID_METADATA["run"], "command": 123})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            failures = check_metadata_schema(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.command", failures[0].message)

    def test_non_string_run_results_is_rejected(self):
        """`results: 123` must not pass the schema check and then blow up
        in check_scenario_coverage/etc. downstream."""
        metadata = dict(VALID_METADATA, run={**VALID_METADATA["run"], "results": 123})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            failures = check_metadata_schema(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.results", failures[0].message)

    def test_non_string_run_setup_is_rejected(self):
        metadata = dict(VALID_METADATA, run={**VALID_METADATA["run"], "setup": 123})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata)
            failures = check_metadata_schema(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.setup", failures[0].message)

    def test_absent_run_setup_is_still_optional(self):
        """A non-string check on an optional key must not turn it required."""
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA)
            self.assertEqual(check_metadata_schema(entry, VALID_METADATA), [])

    def test_unparseable_metadata_short_circuits_with_one_failure(self):
        with tempfile.TemporaryDirectory() as root:
            entry = Path(root) / "entry"
            entry.mkdir()
            (entry / "metadata.yaml").write_text("framework: [unclosed", encoding="utf-8")
            failures = validate_entry(entry)
            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0].rule, "metadata_schema")


class ScenarioIdTests(unittest.TestCase):
    def test_reads_fifty_ids_from_the_repo(self):
        ids = scenario_ids()
        self.assertEqual(len(ids), 50)
        self.assertIn("PRISM-01", ids)
        self.assertIn("PRISM-50", ids)


class ScenarioCoverageTests(unittest.TestCase):
    def test_full_scope_with_all_fifty_passes(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            self.assertEqual(check_scenario_coverage(entry, VALID_METADATA), [])

    def test_full_scope_missing_one_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS[:-1])
            failures = check_scenario_coverage(entry, VALID_METADATA)
            self.assertEqual(len(failures), 1)
            self.assertIn("PRISM-50", failures[0].message)

    def test_a_ten_scenario_subset_no_longer_passes(self):
        """Coverage is all 50 for every entry. A partial set that the retired
        practice scope would have accepted is now 40 missing files."""
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS[:10])
            failures = check_scenario_coverage(entry, VALID_METADATA)
            self.assertEqual(len(failures), 1)
            self.assertIn("PRISM-50", failures[0].message)

    def test_an_undefined_scenario_id_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, list(ALL_IDS) + ["PRISM-51"])
            failures = check_scenario_coverage(entry, VALID_METADATA)
            self.assertEqual(len(failures), 1)
            self.assertIn("PRISM-51", failures[0].message)

    def test_file_without_a_prism_token_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "web" / "prism-helper.test.yaml").write_text("steps: []\n", encoding="utf-8")
            failures = check_scenario_coverage(entry, VALID_METADATA)
            self.assertEqual(len(failures), 1)
            self.assertIn("prism-helper.test.yaml", failures[0].file)

    def test_two_files_for_one_scenario_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "web" / "prism-07-extra.test.yaml").write_text("steps: []\n", encoding="utf-8")
            failures = check_scenario_coverage(entry, VALID_METADATA)
            self.assertEqual(len(failures), 1)
            self.assertIn("PRISM-07", failures[0].message)

    def test_malformed_glob_pattern_is_a_failure_not_a_traceback(self):
        """An absolute-path pattern makes pathlib's glob() raise
        NotImplementedError. Under --all, an unhandled raise here would abort
        every other entry's validation with no rule name attached."""
        metadata = dict(VALID_METADATA, tests={"glob": "/etc/*"})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            failures = check_scenario_coverage(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0].rule, "scenario_coverage")
            self.assertIn("tests.glob", failures[0].message)


class DeclaredHostsTests(unittest.TestCase):
    def test_clean_entry_passes(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])

    def test_undeclared_host_is_reported(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "web" / "prism-01.test.yaml").write_text(
                "url: http://localhost:3100/scenarios/PRISM-01\n", encoding="utf-8"
            )
            failures = check_declared_hosts_only(entry, VALID_METADATA)
            self.assertEqual(len(failures), 1)
            self.assertIn("localhost", failures[0].message)

    def test_vendor_staging_sandbox_is_reported(self):
        """The case a denylist of localhost would have passed."""
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "web" / "prism-02.test.yaml").write_text(
                "url: https://staging.vendor.example/scenarios/PRISM-02\n", encoding="utf-8"
            )
            failures = check_declared_hosts_only(entry, VALID_METADATA)
            self.assertEqual(len(failures), 1)
            self.assertIn("staging.vendor.example", failures[0].message)

    def test_declared_host_is_allowed(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "runner.config.yaml").write_text(
                "api: https://api.example.com/v1\n", encoding="utf-8"
            )
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])

    def test_port_is_ignored_when_matching_the_host(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "runner.config.yaml").write_text(
                "api: https://api.example.com:8443/v1\n", encoding="utf-8"
            )
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])

    def test_ported_allowlist_entry_matches_a_bare_host(self):
        """`network.allowlist: [api.example.com:8443]` must match a literal
        naming that host, with or without the port — the port is stripped on
        both sides, not just the extracted host's."""
        metadata = dict(VALID_METADATA, network={"allowlist": ["api.example.com:8443"]})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            (entry / "runner.config.yaml").write_text(
                "api: https://api.example.com/v1\n", encoding="utf-8"
            )
            self.assertEqual(check_declared_hosts_only(entry, metadata), [])

    def test_ported_allowlist_entry_matches_the_same_ported_host(self):
        metadata = dict(VALID_METADATA, network={"allowlist": ["api.example.com:8443"]})
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            (entry / "runner.config.yaml").write_text(
                "api: https://api.example.com:8443/v1\n", encoding="utf-8"
            )
            self.assertEqual(check_declared_hosts_only(entry, metadata), [])

    def test_templated_base_url_passes_by_construction(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "web" / "prism-03.test.yaml").write_text(
                'url: "{{ env.BASE_URL }}/scenarios/PRISM-03"\n', encoding="utf-8"
            )
            (entry / "runner.config.yaml").write_text(
                "baseUrl: ${PRISM_SANDBOX_URL}\n", encoding="utf-8"
            )
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])

    def test_markdown_is_not_scanned(self):
        """A doc link is not an egress target; requiring it in the allowlist
        would overload an egress declaration with documentation hosts."""
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "README.md").write_text(
                "See https://docs.example.com and run against http://localhost:3100\n",
                encoding="utf-8",
            )
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])

    def test_a_lockfile_is_skipped(self):
        """Registry URLs are resolver output, not a host the entry chose."""
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "package-lock.json").write_text(
                '{"resolved": "https://registry.npmjs.org/momentic/-/momentic-3.7.3.tgz"}\n',
                encoding="utf-8",
            )
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])

    def test_runner_output_directories_are_skipped(self):
        """A run writes HAR logs and console dumps under `test-results/` (both
        Momentic and Playwright default there), and those record every host the
        run touched — the sandbox included. Scanning them fails an honest entry
        for its own debug artifacts."""
        for directory in ("test-results", "playwright-report"):
            with self.subTest(directory):
                with tempfile.TemporaryDirectory() as root:
                    entry = write_entry(root, VALID_METADATA, ALL_IDS)
                    noisy = entry / directory / "runs" / "1"
                    noisy.mkdir(parents=True)
                    (noisy / "console.json").write_text(
                        '{"url": "http://localhost:3100/scenarios/PRISM-01"}\n',
                        encoding="utf-8",
                    )
                    self.assertEqual(
                        check_declared_hosts_only(entry, VALID_METADATA), []
                    )

    def test_node_modules_and_reports_are_skipped(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            (entry / "node_modules" / "dep").mkdir(parents=True)
            (entry / "node_modules" / "dep" / "index.js").write_text(
                "const u = 'http://localhost:3000';\n", encoding="utf-8"
            )
            (entry / "reports").mkdir()
            (entry / "reports" / "junit.xml").write_text(
                "<testsuite name='http://localhost:3100'/>\n", encoding="utf-8"
            )
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])

    def test_symlinks_pointing_outside_entry_are_not_scanned(self):
        """Malicious symlinks in public CI should not leak external file contents."""
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            # Create a file outside the entry with an undeclared host
            outside = Path(root) / "outside.yaml"
            outside.write_text("url: http://secret.internal/data\n", encoding="utf-8")
            # Symlink it into the entry
            try:
                symlink = entry / "leaked.yaml"
                symlink.symlink_to(outside)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlinks not supported on this platform: {exc}")
            # The check should not scan through the symlink
            self.assertEqual(check_declared_hosts_only(entry, VALID_METADATA), [])


class PathContainmentTests(unittest.TestCase):
    def test_relative_run_declaration_passes(self):
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, VALID_METADATA, ALL_IDS)
            self.assertEqual(check_paths_stay_inside_entry(entry, VALID_METADATA), [])

    def test_parent_traversal_in_command_is_reported(self):
        metadata = dict(
            VALID_METADATA,
            run={"command": "cd ../../evaluators && npx example run", "results": "reports/*.xml"},
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            failures = check_paths_stay_inside_entry(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.command", failures[0].message)

    def test_absolute_results_path_is_reported(self):
        metadata = dict(
            VALID_METADATA,
            run={"command": "npx example run", "results": "/tmp/junit.xml"},
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            failures = check_paths_stay_inside_entry(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.results", failures[0].message)

    def test_absolute_path_inside_setup_is_reported(self):
        metadata = dict(
            VALID_METADATA,
            run={
                "setup": "cp /Users/me/creds.json .",
                "command": "npx example run",
                "results": "reports/*.xml",
            },
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            failures = check_paths_stay_inside_entry(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.setup", failures[0].message)

    def test_a_flag_value_is_not_mistaken_for_an_absolute_path(self):
        metadata = dict(
            VALID_METADATA,
            run={
                "command": "npx example run --reporter junit --reporter-dir reports",
                "results": "reports/*.xml",
            },
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            self.assertEqual(check_paths_stay_inside_entry(entry, metadata), [])

    def test_absolute_path_glued_to_equals_is_reported(self):
        metadata = dict(
            VALID_METADATA,
            run={"command": "npx example run --out=/etc/passwd", "results": "reports/*.xml"},
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            failures = check_paths_stay_inside_entry(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.command", failures[0].message)

    def test_absolute_path_after_quote_is_reported(self):
        metadata = dict(
            VALID_METADATA,
            run={"command": 'npx example run --config "/etc/my.conf"', "results": "reports/*.xml"},
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            failures = check_paths_stay_inside_entry(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.command", failures[0].message)

    def test_parent_traversal_glued_to_equals_is_reported(self):
        metadata = dict(
            VALID_METADATA,
            run={"command": "npx example run --dir=../evaluators", "results": "reports/*.xml"},
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            failures = check_paths_stay_inside_entry(entry, metadata)
            self.assertEqual(len(failures), 1)
            self.assertIn("run.command", failures[0].message)

    def test_url_scheme_slashes_are_not_mistaken_for_absolute_path(self):
        metadata = dict(
            VALID_METADATA,
            run={
                "command": "npx example run --base-url=https://api.example.com/v1",
                "results": "reports/*.xml",
            },
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            self.assertEqual(check_paths_stay_inside_entry(entry, metadata), [])

    def test_double_dot_not_followed_by_path_separator_is_not_a_traversal(self):
        metadata = dict(
            VALID_METADATA,
            run={
                "command": "npx example run --name a..b",
                "results": "reports/*.xml",
            },
        )
        with tempfile.TemporaryDirectory() as root:
            entry = write_entry(root, metadata, ALL_IDS)
            self.assertEqual(check_paths_stay_inside_entry(entry, metadata), [])


class DiscoverEntriesTests(unittest.TestCase):
    def test_a_metadata_yaml_under_node_modules_is_not_a_phantom_entry(self):
        """A vendor who commits node_modules/ should not turn a dependency's
        own metadata.yaml into an entry that public CI then fails with an
        undecodable message."""
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            real_entry = root_path / "real-framework"
            real_entry.mkdir()
            (real_entry / "metadata.yaml").write_text(
                yaml.safe_dump(VALID_METADATA), encoding="utf-8"
            )
            phantom = real_entry / "node_modules" / "some-dep"
            phantom.mkdir(parents=True)
            (phantom / "metadata.yaml").write_text(
                yaml.safe_dump(VALID_METADATA), encoding="utf-8"
            )
            self.assertEqual(discover_entries(root_path), [real_entry])

    def test_reports_dir_is_also_skipped(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            real_entry = root_path / "real-framework"
            real_entry.mkdir()
            (real_entry / "metadata.yaml").write_text(
                yaml.safe_dump(VALID_METADATA), encoding="utf-8"
            )
            phantom = real_entry / "reports" / "nested"
            phantom.mkdir(parents=True)
            (phantom / "metadata.yaml").write_text(
                yaml.safe_dump(VALID_METADATA), encoding="utf-8"
            )
            self.assertEqual(discover_entries(root_path), [real_entry])


class MainTests(unittest.TestCase):
    def test_all_on_an_empty_tree_exits_zero(self):
        """Public CI runs `--all` against a tree that ships no submission
        entry. Finding nothing is success, not a usage error."""
        with tempfile.TemporaryDirectory() as root:
            with mock.patch.object(validate_submission, "REPO_ROOT", Path(root)):
                (Path(root) / "submissions").mkdir()
                self.assertEqual(main(["--all"]), 0)

    def test_no_entries_and_no_flag_still_errors(self):
        with self.assertRaises(SystemExit) as caught:
            main([])
        self.assertEqual(caught.exception.code, 2)

    def test_all_still_validates_a_discovered_entry(self):
        with tempfile.TemporaryDirectory() as root:
            submissions = Path(root) / "submissions"
            submissions.mkdir()
            write_entry(submissions, VALID_METADATA, ALL_IDS[:1], name="partial")
            with mock.patch.object(validate_submission, "REPO_ROOT", Path(root)):
                self.assertEqual(main(["--all"]), 1)


if __name__ == "__main__":
    unittest.main()
