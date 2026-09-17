import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-43', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-43');

  await runSteps({
    page,
    userFlow: 'PRISM-43',
    steps: [
      {
        description: 'Fill in the card details below and place the order.',
        data: { card_number: '4242 4242 4242 4242', name_on_card: 'Ada Lovelace' },
      },
    ],
    assertions: [{ assertion: 'A confirmation that the order was placed is shown.' }],
    test,
    expect,
  });
});
