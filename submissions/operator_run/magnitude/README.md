# Magnitude — PRISM operator entry

**Operator-authored.** This entry was written and run by the PRISM operator, not
by Magnitude. It measures the **self-hosted, open-source `magnitude-test` runner**
on PRISM's web scenarios.

Every string an agent reads here comes from the scenario's published spec.

Questions go to the operator-contact issue form on this repository. The
`contact:` in `metadata.yaml` is the template placeholder and reaches nobody.

## What is here

| File                        | What it is                                                  |
| --------------------------- | ----------------------------------------------------------- |
| `metadata.yaml`             | The entry contract, including every pinned run setting       |
| `magnitude.config.ts`       | Viewport, model, telemetry, and the fail-fast override       |
| `run_prism.py`              | A CLI-to-JUnit adapter. Magnitude has no reporter            |
| `tests/prism-NN.mag.ts` ×50 | One natural-language objective each, from the published spec |

## Running it

```bash
npm install
npx patchright install chromium

PRISM_SANDBOX_URL=<sandbox-url> python3 run_prism.py
```

Run it against `mcr.microsoft.com/playwright:v1.63.0-noble`, or any environment
whose browsers match Playwright 1.63 — see below.

## Why an adapter exists

Magnitude has **no JUnit reporter** — there is no `junit`, `xml` or `reporter`
anywhere in the package — while PRISM's evaluator reads JUnit. `run_prism.py`
runs one scenario per invocation and writes one `<testcase>` per scenario, named
so the `prism-NN` token resolves back to the scenario.

Three decisions in it are worth knowing if you write your own adapter:

**The verdict comes from the exit code, not from parsing output.** The CLI takes a
glob filter, so one scenario per invocation yields that scenario's own
`process.exit(overallSuccess ? 0 : 1)`. A runner that scrapes prose for a verdict
can turn a failure into a reported pass — a False Heal recorded against the
framework for a bug in the harness.

**One scenario at a time.** `-w/--workers` defaults to 1 and is left alone.
Several PRISM scenarios keep a single server-side serve timestamp, so a second
concurrent load of one scenario overwrites the first's clock.

**An operational fault writes no JUnit at all.** An exit code that is neither 0
nor 1 is the process failing rather than reporting, and per
[`submissions/RANKED.md`](../../RANKED.md) a round that does not execute all fifty
scenarios is reported incomplete rather than scored.

## Two things about this framework that shape the entry

**It fails fast by default.** Magnitude aborts the run at the first failure unless
told otherwise. On PRISM a failure is the *correct* answer on several scenarios,
so `continueAfterFailure: true` is set in the config and `--no-fail-fast` is
passed on every invocation.

**It drives patchright, not stock Playwright.** `magnitude-core` pins
`playwright: npm:patchright@^1.52.0` — a fork that alters browser fingerprints —
which resolves to Playwright 1.63. Its browsers are therefore not the ones a
differently-pinned image ships, which is why `setup` installs them and why the
image version above matters.

## The shape of a test

```ts
import { test } from 'magnitude-test';

test('PRISM-01', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-01` }, async (agent) => {
  await agent.act('Submit the transaction.');
  await agent.check('A confirmation that the transaction succeeded is shown.');
});
```

The `act` argument is the scenario's published `goal`, verbatim; the `check`
argument is its published `success_signal`. Scenarios that publish `inputs` pass
them through `ActOptions.data` rather than pasting them into the instruction.

The base URL is read from the environment per run, so no sandbox address is
written into this entry.
