import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-34', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-34');

  await runSteps({
    page,
    userFlow: 'PRISM-34',
    steps: [
      {
        description: 'Buy the asset the page asks for, then confirm the purchase.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the purchase succeeded is shown.' }],
    test,
    expect,
  });
});
