import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-01', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-01');

  await runSteps({
    page,
    userFlow: 'PRISM-01',
    steps: [
      {
        description: 'Submit the transaction.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the transaction succeeded is shown.' }],
    test,
    expect,
  });
});
