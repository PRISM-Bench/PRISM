# Kane CLI — PRISM reference entry

**Operator-authored.** This entry was written and run by the PRISM operator, not
by TestMu/LambdaTest. It is published as a worked reference: a conforming entry
in one framework's shape, so a vendor can see what the contract in
[`submissions/CONTRACT.md`](../../CONTRACT.md) looks like as files.

You may copy these files verbatim or author your own. Every string an agent
reads here comes from the scenario's published spec.

Questions go to the operator-contact issue form on this repository. The
`contact:` in `metadata.yaml` is the template placeholder and reaches nobody.

## What is here

| File                         | What it is                                                   |
| ---------------------------- | ------------------------------------------------------------ |
| `metadata.yaml`              | The entry contract, including the window-size setup step     |
| `run_prism.py`               | A CLI-to-JUnit adapter. Kane emits NDJSON, PRISM reads JUnit |
| `tests/prism-NN_test.md` ×50 | One plain-English objective per scenario                     |

## Running it

```bash
brew install LambdaTest/kane/kane-cli
kane-cli login
kane-cli config set-window 1280x807

PRISM_SANDBOX_URL=<sandbox-url> python3 run_prism.py
```

`set-window 1280x807` is load-bearing, not a rounding error: Chrome spends 87
CSS px of the window on its own UI, so a 1280×807 window is what renders the
1280×720 viewport PRISM grades. `run_prism.py` refuses to start if the config
says anything else.

## Why an adapter exists

Kane CLI has no JUnit reporter — it emits NDJSON (`--agent`) and sealed evidence
packs — while PRISM's evaluator reads JUnit. `run_prism.py` runs one scenario per
invocation and writes one `<testcase>` per scenario, named so the `prism-NN`
token resolves back to the scenario.

Three decisions in it are worth knowing if you write your own adapter:

**The verdict comes from the exit code, not from NDJSON.** Kane documents its
exit codes (`0` pass, `1` fail, `2` error, `3` cancelled/timeout) and publishes
no event schema. Keying off documented behaviour means an undocumented event
rename cannot silently flip a result.

**An operational error aborts the run rather than being recorded.** Exit 2 means
auth, configuration or Chrome failed — that is not a verdict about a scenario.
Recording it as a `<failure>` would claim the framework honestly reported
failure, which is a claim the run did not earn.

**Caching is left on, not suppressed.** Kane caches recordings and replays them
by default, and its docs recommend committing the cache. `--author` is **not**
passed, so a cached step replays normally. See
[`submissions/RANKED.md`](../../RANKED.md): PRISM measures what a replayed
step does against a moved seed rather than preventing the replay — a cache
that keeps working is a capability the score should credit.

## The shape of a test

Markdown with YAML frontmatter, three sections:

```markdown
---
mode: testing
---

# PRISM-01

## Open the page

Open {{ BASE_URL }}/scenarios/PRISM-01.

## Complete the task

Submit the transaction.

## Confirm the outcome

A confirmation that the transaction succeeded is shown.
```

The task section is the scenario's published `goal`, verbatim; the outcome
section is its published `success_signal`.
