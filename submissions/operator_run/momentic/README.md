# Momentic — PRISM reference entry

**Operator-authored.** This entry was written and run by the PRISM operator, not
by Momentic. It is published as a worked reference: a conforming entry in one
framework's shape, so a vendor can see what the contract in
[`submissions/CONTRACT.md`](../../CONTRACT.md) looks like as files.

You may copy these files verbatim or author your own — neither is penalised.
Every string an agent reads here comes from the scenario's published spec, so
copying them gives you no advantage and no disadvantage.

Questions go to the operator-contact issue form on this repository. The
`contact:` in `metadata.yaml` is the template placeholder and reaches nobody.

## What is here

| File                         | What it is                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------- |
| `metadata.yaml`              | The entry contract: framework, version, test glob, run commands, declared hosts |
| `momentic.config.yaml`       | Momentic's own config. `baseUrl` reads `PRISM_SANDBOX_URL`; retries are off     |
| `package.json`               | The packages this entry needs                                                   |
| `web/prism-NN.test.yaml` ×50 | One test per scenario                                                           |

## Running it

Requires a Momentic account — the AI steps run in Momentic's cloud and consume
its credits. There is no offline mode.

```bash
npm install
npx momentic install-browsers chromium
npx @momentic/wizard login          # or: export MOMENTIC_API_KEY=...

PRISM_SANDBOX_URL=<sandbox-url> npx momentic run --env web -y \
  --reporter junit --reporter-dir reports
```

`--env web` is required: it is the environment whose `baseUrl` reads
`PRISM_SANDBOX_URL`. `-y` skips Momentic's confirmation prompts, matching the
`run.command` this entry declares in `metadata.yaml`. The sandbox address is
assigned per run and is never written into an entry.

## The shape of a test

One `navigate`, one `act` carrying a goal and a postcondition. No step list, no
selectors, no waits:

```yaml
steps:
  - navigate:
      url: '{{ env.BASE_URL }}/scenarios/PRISM-01'
  - act:
      goal: Submit the transaction.
      postcondition: A confirmation that the transaction succeeded is shown.
```

The `goal` is the scenario's published `goal`, verbatim; the `postcondition` is
its published `success_signal`. A postcondition states the durable outcome that
proves success, which is what PRISM scores — a scenario is passed by reaching a
real end state, not by a spinner or a toast appearing.

## The viewport is pinned per test

PRISM scores a pinned environment of 1280×720 at device pixel ratio 1. Momentic
has **no project-level viewport setting** — `browser.viewport` in
`momentic.config.yaml` is silently ignored, which `momentic lint` reports — so
every test pins it:

```yaml
viewport:
  width: 1280
  height: 720
```

Without this the run is graded at the wrong viewport: scoring clamps the fold to
the scored viewport, so a taller window puts content above the fold that the
scenario intends to be below it.

## Reporting

Momentic emits standard JUnit (`--reporter junit` → `reports/*.xml`). Pass/fail
is the whole claim; nothing else in the report is read. A pass reached through
failure recovery is still a pass — the sandbox decides independently whether it
holds.
