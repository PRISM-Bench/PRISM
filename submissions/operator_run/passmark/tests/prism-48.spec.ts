import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-48', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-48');

  await runSteps({
    page,
    userFlow: 'PRISM-48',
    steps: [
      {
        description:
          'Look up the receipt for this order and note the confirmation code it shows. Enter that code on the checkout form and finish the purchase.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the purchase went through is shown.' }],
    test,
    expect,
  });
});
