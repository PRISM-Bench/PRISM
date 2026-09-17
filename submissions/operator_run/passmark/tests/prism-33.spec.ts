import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-33', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-33');

  await runSteps({
    page,
    userFlow: 'PRISM-33',
    steps: [
      {
        description: 'Approve the refund for the order requested on the page.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the refund was approved is shown.' }],
    test,
    expect,
  });
});
