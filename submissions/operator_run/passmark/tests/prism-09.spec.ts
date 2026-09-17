import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-09', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-09');

  await runSteps({
    page,
    userFlow: 'PRISM-09',
    steps: [
      {
        description: 'Confirm the booking.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the booking was placed is shown.' }],
    test,
    expect,
  });
});
