import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-07', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-07');

  await runSteps({
    page,
    userFlow: 'PRISM-07',
    steps: [
      {
        description: 'Create an account.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the account was created is shown.' }],
    test,
    expect,
  });
});
