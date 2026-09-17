import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-45', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-45');

  await runSteps({
    page,
    userFlow: 'PRISM-45',
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
