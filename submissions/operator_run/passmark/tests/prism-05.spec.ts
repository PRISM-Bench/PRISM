import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-05', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-05');

  await runSteps({
    page,
    userFlow: 'PRISM-05',
    steps: [
      {
        description: 'Pay for the order using the details below.',
        data: { card_number: '4242 4242 4242 4242' },
      },
    ],
    assertions: [{ assertion: 'A confirmation that the payment succeeded is shown.' }],
    test,
    expect,
  });
});
