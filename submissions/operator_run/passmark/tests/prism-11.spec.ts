import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-11', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-11');

  await runSteps({
    page,
    userFlow: 'PRISM-11',
    steps: [
      {
        description: 'Delete the account.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the account was deleted is shown.' }],
    test,
    expect,
  });
});
