import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-42', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-42');

  await runSteps({
    page,
    userFlow: 'PRISM-42',
    steps: [
      {
        description: 'Complete the action.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the action succeeded is shown.' }],
    test,
    expect,
  });
});
