# Passmark — PRISM reference entry

**Operator-authored.** This entry was written and run by the PRISM operator. It
is published as a worked reference: a conforming entry in one framework's shape,
so a vendor can see what the contract in
[`submissions/CONTRACT.md`](../../CONTRACT.md) looks like as files.

You may copy these files verbatim or author your own. Every string an agent
reads here comes from the scenario's published spec.

Questions go to the operator-contact issue form on this repository. The
`contact:` in `metadata.yaml` is the template placeholder and reaches nobody.

## What is here

| File                         | What it is                                                        |
| ---------------------------- | ----------------------------------------------------------------- |
| `metadata.yaml`              | The entry contract                                                |
| `playwright.config.ts`       | The whole environment contract — Passmark is a Playwright library |
| `prism.setup.ts`             | Passmark's own configuration, imported by every test              |
| `package.json`               | The packages this entry needs                                     |
| `tests/prism-NN.spec.ts` ×50 | One test per scenario                                             |

## Running it

```bash
npm install
npx playwright install chromium
export OPENROUTER_API_KEY=...

PRISM_SANDBOX_URL=<sandbox-url> npx playwright test
```

## What the config pins, and why

Passmark is a Playwright _library_, so `playwright.config.ts` is the whole
environment contract — the agent runs inside Playwright and inherits all of it.

| Setting                                      | Why                                                                                                                                                                                                                               |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `viewport: 1280×720`, `deviceScaleFactor: 1` | The environment PRISM scores                                                                                                                                                                                                      |
| `retries: 0`                                 | A framework-level retry masks the timing behaviour being measured, and Passmark bypasses its action cache on a retry — so a retried test runs under different rules than the one being scored                                     |
| `workers: 1`                                 | Playwright parallelises across files even at `fullyParallel: false`, and each scenario is a file. On a suite built from timing traps, a loaded machine acts later and lands after the seeded deadline, where it grades as settled |
| `baseURL: process.env.PRISM_SANDBOX_URL`     | No default. An entry never bakes in a sandbox address                                                                                                                                                                             |

`prism.setup.ts` supplies no Redis connection, so Passmark's action cache has no
backend to replay from in this entry — an infrastructure gap, not a deliberate
suppression. `bypassCache` is not set: per
[`submissions/RANKED.md`](../../RANKED.md), PRISM measures what a cache's
replay actually does against a moved seed rather than preventing it, so a
vendor entry that does connect Redis should leave the cache running.

## The shape of a test

```typescript
test('PRISM-01', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-01');

  await runSteps({
    page,
    userFlow: 'PRISM-01',
    steps: [{ description: 'Submit the transaction.' }],
    assertions: [{ assertion: 'A confirmation that the transaction succeeded is shown.' }],
    test,
    expect,
  });
});
```

`description` is the scenario's published `goal`, `assertion` its published
`success_signal`, and `data` (when present) its published `inputs`. Navigation
is a plain `page.goto` rather than an AI step, so it spends no model call and
cannot smuggle in page knowledge.

These files are generated from the specs rather than hand-written, and
`scripts/tests/test_passmark_entry.py` in PRISM-core compares every string back
against the scenario it came from.
