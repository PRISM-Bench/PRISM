import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-25', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-25');

  await runSteps({
    page,
    userFlow: 'PRISM-25',
    steps: [
      {
        description: 'Advance the walkthrough to the checkpoint the page names, then confirm it.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the checkpoint was confirmed is shown.' }],
    test,
    expect,
  });
});
