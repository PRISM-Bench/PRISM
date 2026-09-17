import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-14', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-14');

  await runSteps({
    page,
    userFlow: 'PRISM-14',
    steps: [
      {
        description: 'Cancel the order the assistant is showing.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the order was cancelled is shown.' }],
    test,
    expect,
  });
});
