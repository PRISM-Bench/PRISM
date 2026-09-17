import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-06', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-06');

  await runSteps({
    page,
    userFlow: 'PRISM-06',
    steps: [
      {
        description: 'Confirm the order.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the order was confirmed is shown.' }],
    test,
    expect,
  });
});
