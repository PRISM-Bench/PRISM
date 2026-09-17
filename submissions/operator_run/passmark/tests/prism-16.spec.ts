import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-16', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-16');

  await runSteps({
    page,
    userFlow: 'PRISM-16',
    steps: [
      {
        description: 'Open the Edit control on the account settings row that has one.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the action succeeded is shown.' }],
    test,
    expect,
  });
});
