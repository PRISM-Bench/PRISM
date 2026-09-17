import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-13', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-13');

  await runSteps({
    page,
    userFlow: 'PRISM-13',
    steps: [
      {
        description: 'Review the order and place it.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the order succeeded is shown.' }],
    test,
    expect,
  });
});
