import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-04', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-04');

  await runSteps({
    page,
    userFlow: 'PRISM-04',
    steps: [
      {
        description: 'Enter the email address below and confirm it.',
        data: { email: 'tester@example.com' },
      },
    ],
    assertions: [{ assertion: 'A confirmation that the submission succeeded is shown.' }],
    test,
    expect,
  });
});
