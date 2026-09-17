# The submission contract

This is the contract a PRISM entry must satisfy to be a **valid entry**: what
files it contains, what `metadata.yaml` declares, and what shape its test
suite must take. It does not cover how to submit one (see `README.md`) or how
a ranked run is conducted and reported (see `RANKED.md`).

Every rule below is tagged **[checked]** or **[honour system]**.
**[checked]** means `scripts/validate_submission.py` enforces it: the operator
runs that validator on your archive at intake, and an entry that fails is
rejected before it reaches a round. **[honour system]** means it cannot be seen
by static inspection — no test has run yet — so it is either recorded by the
sandbox once a run happens, or simply trusted.

## 1. Entry layout

You submit a single archive. Its **entry root** is the one directory containing
`metadata.yaml`, and every path in this contract is relative to that root:

```text
<entry-root>/
  metadata.yaml
  <your test files — whatever `tests.glob` resolves to>
```

Exactly one `metadata.yaml`. An archive carrying none, or several, is rejected
at intake: there is no unambiguous entry root to validate. What the archive is
named, and whether its root sits at the top level or one directory down, does
not matter.

[`TEMPLATE/`](TEMPLATE/) is this shape as files: copy the directory, rename
`metadata.example.yaml` to `metadata.yaml`, and author your test files. It
carries none so that it stays undiscoverable to the validator — an entry with
a `metadata.yaml` and no tests fails `scenario_coverage` with all 50 missing.

For test files as files, read the three operator-run entries under
[`operator_run/`](operator_run/). They are operator-authored references in three
framework shapes, and they are examples rather than a mandate: copy them
verbatim or author your own, whichever suits your system. Nothing in them is
material you could not already read. Every string an agent sees there is that
scenario's published `goal` and `success_signal`, byte-for-byte.

## 2. `metadata.yaml`

Every entry carries a `metadata.yaml` at its root. This is the full annotated
shape:

```yaml
framework: momentic
version: '3.55.0'
contact: you@example.com
submission_date: 2026-07-30

scope: full # the only scope — every round covers all 50 scenarios

tests:
  glob: web/prism-*.test.yaml # one file per scenario

run:
  setup: npm install && npx momentic install-browsers chromium # optional
  command: npx momentic run --env web --reporter junit --reporter-dir reports
  results: reports/*.xml # JUnit, relative to the entry

network:
  allowlist: # hosts your system contacts; [] declares none
    - app.momentic.ai
```

`quarter` and `submitter` are optional keys used only by operator entries;
they are not part of the vendor contract.

`version` is the version of **your framework** — the build this entry runs, as
its own release numbering gives it (`3.55.0`, `0.8.10`, `1.0.16`). It is not
the round you are entering: the round travels on your form response, and
`submission_date` dates the entry.

The distinction earns its keep when a score moves between quarters. A framework
that silently changed how it sizes a browser, or when it considers a page
settled, will score differently on an unchanged scenario set — and without the
build recorded against the run, that difference is unattributable. Give the
resolved version, not a range: `1.0.16`, never `^1.0.16`.

`contact` should be an address a human reads. Your entry is private — only your
score and the archive's SHA-256 are published — so this is how the operator
reaches you about a failing scenario, a stale version, or a re-run, and it is
the only channel that exists for it. The address stays with your form response
in the operator's private records; it is not published. (`TEMPLATE/` carries a
placeholder address rather than a real one, for the obvious reason: it is a file
in a public repository.)

## 3. Self-check before you submit

Run the same validator the operator runs on your archive at intake. Clone this
repository and run it from the **repository root** (it imports as
`scripts.validate_submission`; running it from inside your entry directory
fails with `No module named scripts`), with PyYAML installed
(`pip install pyyaml`), pointing it at your entry root — any path, inside this
repository or not:

```bash
python3 -m scripts.validate_submission /path/to/<entry-root>
```

It reports every failure — entry, file, and rule — and exits non-zero if
anything fails. A clean run does not guarantee your entry scores well; it
only guarantees your entry is shaped correctly.

## 4. `[checked]` — the validator enforces

**[checked] `metadata_schema`** — `metadata.yaml` parses, and every required
key is present: `framework`, `version`, `contact`, `submission_date`,
`scope`, `tests`, `run`, `network`. Beyond presence: `scope` must be `full`,
the only scope there is; `tests.glob` must be a non-empty string; `run.command`
and `run.results` must each be a non-empty string, and `run.setup` (optional)
must be a string when present; `network.allowlist` must be a list. An
**empty** `network.allowlist` (`[]`) is valid and declares no egress, but the
key itself is required so nobody omits it by accident.

**[checked] `scenario_coverage`** — `tests.glob` resolves to exactly the 50
scenarios `data/scenarios/` defines. One test file per scenario, no more, no
fewer, and each file's basename must carry a `prism-NN` token so the
scenario it covers is unambiguous. There is no partial entry: a round covers
the whole suite.

**[checked] `declared_hosts_only`** — every concrete `http(s)://host` literal
found anywhere in your entry's executable surface must have its host present
in `network.allowlist`. "Executable surface" excludes `*.md` files, the
directories `node_modules`, `reports`, `test-results`, `playwright-report`,
`.git`, `__pycache__` and `.momentic`,
and dependency lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`,
`poetry.lock`, `uv.lock`) — build output and installed dependencies, not
content you authored. This is an allow-list, not a denylist, so nothing you
didn't declare passes silently. The templated base-URL forms your test suite
uses to reach the sandbox (`{{ env.BASE_URL }}/…`, `${PRISM_SANDBOX_URL}`)
carry no literal scheme and host, so they pass by construction — you don't
need to allow-list the sandbox itself. A port is ignored on both sides when
matching, so `api.example.com` and `api.example.com:8443` are the same
declaration either in your suite or in `network.allowlist`.

**[checked] `paths_stay_inside_entry`** — `run.setup`, `run.command` and
`run.results` may contain no `..` and no absolute path. The operator runs
`run.command` with your entry directory as the working directory, and a
path reaching outside it would depend on the operator's machine layout,
which you cannot know.

## 5. `[honour system]` — not visible before a run

None of these can be verified by static inspection — there is no test run yet
to observe. Each is either recorded by the sandbox once your entry actually
runs, or simply trusted.

| Rule                                                                                                                                                     | Why it cannot be checked before a run                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Every `<testcase>` in your JUnit output carries a `prism-NN` token in its `name` or `classname` attribute, or in the name of its enclosing `<testsuite>` | No JUnit XML exists until your test command has run. A missing or mismatched token costs that scenario its score.                                                                                                                                                              |
| Your suite resolves the sandbox's base URL from `PRISM_SANDBOX_URL` and requests paths of the form `/scenarios/PRISM-NN`                                 | Only observable once the harness actually executes your suite against a live sandbox.                                                                                                                                                                                          |
| Your suite runs at viewport 1280x720, device scale factor 1, `prefers-reduced-motion: no-preference`                                                     | The sandbox records the browser's actual reading at run time; it is reported, not something a static file can attest to.                                                                                                                                                       |
| You drive one scenario at a time — no concurrent loads of the same scenario                                                                              | Some scenarios keep a single server-side serve timestamp; a second concurrent load of the same scenario overwrites the first's clock and can grade a genuine post-settle interaction as unsettled. This is a property of how your suite executes, not of any file it contains. |
