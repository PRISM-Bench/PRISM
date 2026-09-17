import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-30', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-30');

  await runSteps({
    page,
    userFlow: 'PRISM-30',
    steps: [
      {
        description: 'Place the order.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the order was placed is shown.' }],
    test,
    expect,
  });
});
