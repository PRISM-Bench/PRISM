# TestZeus Hercules — PRISM operator entry

**Operator-authored.** This entry was written and run by the PRISM operator, not
by TestZeus. It measures the **self-hosted** Hercules runner on PRISM's web
scenarios; TestZeus's hosted platform is out of scope, as are Hercules' API,
security and accessibility modes, for which PRISM has no scenarios.

Every string an agent reads here comes from the scenario's published spec.

Questions go to the operator-contact issue form on this repository. The
`contact:` in `metadata.yaml` is the template placeholder and reaches nobody.

## What is here

| File                        | What it is                                                     |
| --------------------------- | -------------------------------------------------------------- |
| `metadata.yaml`             | The entry contract, including every pinned run setting          |
| `run_prism.py`              | The suite runner. Hercules takes one feature per invocation     |
| `features/prism-NN.feature` ×50 | One Gherkin scenario each, from the published spec          |

## Running it

```bash
apt-get update && apt-get install -y --no-install-recommends gcc python3-dev
pip install testzeus-hercules==1.0.2
python3 -m playwright install chromium

PRISM_SANDBOX_URL=<sandbox-url> python3 run_prism.py
```

The exact environment the scored run used is in `metadata.yaml`'s `run.command`,
not in a dotfile, so it can be read rather than reconstructed.

## Why a runner exists

Hercules takes **one feature file per invocation** and has no suite mode, so
something has to loop the 50. That also means the one-scenario-at-a-time rule
holds by construction: the loop is serial, and nothing in it is concurrent.

Three decisions in `run_prism.py` are worth knowing if you write your own:

**The verdict is Hercules' own.** Hercules writes a real JUnit file per feature,
so the runner merges those rather than deriving pass/fail from exit codes. A
runner that re-decides the verdict can turn a failure into a reported pass — a
False Heal recorded against the framework for a bug in the harness.

**Artifacts are written outside the entry.** Hercules roots `output/`, `proofs/`
and `log_files/` at its project base, and proofs include network logs naming the
sandbox. The runner points the project base at a temporary directory, so one run
cannot leave hosts inside the entry — which would fail the entry's own
`declared_hosts_only` check.

**An operational fault writes no JUnit at all.** If Hercules never produced a
result for a scenario, the round did not execute all fifty, and per
[`submissions/RANKED.md`](../../RANKED.md) that is reported incomplete rather
than scored. A partial file would be read as real results.

## The shape of a test

```gherkin
Feature: PRISM-01
  Scenario: PRISM-01
    Given I open the page at {{BASE_URL}}/scenarios/PRISM-01
    When Submit the transaction.
    Then A confirmation that the transaction succeeded is shown.
```

The `When` step is the scenario's published `goal`, verbatim; the `Then` step is
its published `success_signal`. Scenarios that publish `inputs` carry them as a
Gherkin data table under `And I use these values:`.

`Feature` and `Scenario` both carry the scenario id deliberately: Hercules maps
them to a JUnit testcase's `classname` and `name`, and PRISM resolves a result
back to its scenario by finding a `prism-NN` token in either.

`{{BASE_URL}}` is resolved per run from `PRISM_SANDBOX_URL` into a staged copy.
No sandbox address is written into this entry.
