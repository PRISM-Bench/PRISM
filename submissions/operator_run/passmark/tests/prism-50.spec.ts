import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-50', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-50');

  await runSteps({
    page,
    userFlow: 'PRISM-50',
    steps: [
      {
        description: 'Delete the user.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the user was deleted is shown.' }],
    test,
    expect,
  });
});
