import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-36', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-36');

  await runSteps({
    page,
    userFlow: 'PRISM-36',
    steps: [
      {
        description: 'Add two of the product to the cart.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that both items were added to the cart is shown.' }],
    test,
    expect,
  });
});
