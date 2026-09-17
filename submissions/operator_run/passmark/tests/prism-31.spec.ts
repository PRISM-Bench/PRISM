import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-31', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-31');

  await runSteps({
    page,
    userFlow: 'PRISM-31',
    steps: [
      {
        description: 'Review the cart and check out.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the checkout succeeded is shown.' }],
    test,
    expect,
  });
});
