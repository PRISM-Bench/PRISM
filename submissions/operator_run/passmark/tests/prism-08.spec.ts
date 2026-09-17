import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-08', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-08');

  await runSteps({
    page,
    userFlow: 'PRISM-08',
    steps: [
      {
        description: 'Fill in the details below and create the account.',
        data: {
          full_name: 'Ada Lovelace',
          email: 'ada.lovelace@example.com',
          password: 'Prism-08-trial',
        },
      },
    ],
    assertions: [{ assertion: 'A confirmation that the account was created is shown.' }],
    test,
    expect,
  });
});
