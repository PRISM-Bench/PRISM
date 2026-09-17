import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-17', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-17');

  await runSteps({
    page,
    userFlow: 'PRISM-17',
    steps: [
      {
        description: 'Confirm the order.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the order succeeded is shown.' }],
    test,
    expect,
  });
});
