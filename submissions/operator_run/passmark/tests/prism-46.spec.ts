import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-46', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-46');

  await runSteps({
    page,
    userFlow: 'PRISM-46',
    steps: [
      {
        description: 'Pick something from the catalog and buy it.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the purchase succeeded is shown.' }],
    test,
    expect,
  });
});
