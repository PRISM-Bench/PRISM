import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-18', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-18');

  await runSteps({
    page,
    userFlow: 'PRISM-18',
    steps: [
      {
        description: 'Open the Privacy Policy from the bottom of the page.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the privacy policy was opened is shown.' }],
    test,
    expect,
  });
});
