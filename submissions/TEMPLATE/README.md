# Submission template

A worked reference for a PRISM submission entry. Copy this directory, rename
`metadata.example.yaml` to `metadata.yaml`, and author your 50 test files.

`submissions/CONTRACT.md` is the authority on what an entry must contain;
`submissions/README.md` covers how a submission reaches the operator, including
the pre-submission dry run. This directory shows the shape.

## What an entry is

| File                          | What it is                                                                       |
| ----------------------------- | -------------------------------------------------------------------------------- |
| `metadata.yaml`               | The contract: framework, contact, scope, test glob, run commands, declared hosts |
| Runner config                 | Your framework's own config. The Momentic one here is an example                 |
| `web/prism-NN.test.yaml` × 50 | Your tests. Not in this template — see `operator_run/` for three worked sets     |

No results, no reports, no scores. The operator runs the entry and scores it;
an entry that ships its own results is claiming an outcome nobody observed.

This directory shows the shape with the values blanked. For three filled-in
entries in real framework shapes, see [`../operator_run/`](../operator_run/).

## The naming convention that matters

One test file per scenario, named `prism-NN.test.yaml`. The scorer maps a JUnit
testcase back to a scenario by the `prism-NN` token in the testcase name or
classname, which frameworks derive from the file. A test's internal `id` can be
anything; the **filename** is the contract.

`scripts/validate_submission.py` checks that the glob resolves to exactly 50
files, one token each — it does **not** parse JUnit. Malformed reports and
tokens that fail to resolve are caught by the dry run.

## The sandbox address

Read it from `PRISM_SANDBOX_URL`. It is assigned per run, and an entry that
hardcodes a host fails `declared_hosts_only` — which scans every non-Markdown
file in the entry for `http(s)://` hosts and compares them against
`network.allowlist`. Declare every host your framework itself contacts; leave
the sandbox out of it.

## Reporting

Emit standard JUnit to the path `run.results` names. Pass/fail is the whole
claim — nothing else in the report is read, and nothing about how a pass was
reached changes what it asserts. A pass a framework's recovery logic salvaged
is still a pass, and the sandbox decides independently whether it holds.

## Before you submit

```bash
python3 -m scripts.validate_submission submissions/your-entry
```

Static shape only: required keys, 50 files with resolvable tokens, no
undeclared hosts, no path escaping the entry. It executes nothing — deliberately,
because it is pointed at archives from strangers.
