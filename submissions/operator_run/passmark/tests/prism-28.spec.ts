import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-28', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-28');

  await runSteps({
    page,
    userFlow: 'PRISM-28',
    steps: [
      {
        description: 'Approve the order in the Active orders list.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the order was approved is shown.' }],
    test,
    expect,
  });
});
