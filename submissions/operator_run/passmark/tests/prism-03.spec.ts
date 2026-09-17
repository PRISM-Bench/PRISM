import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-03', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-03');

  await runSteps({
    page,
    userFlow: 'PRISM-03',
    steps: [
      {
        description: 'Confirm the booking.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the booking succeeded is shown.' }],
    test,
    expect,
  });
});
