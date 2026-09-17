import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-24', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-24');

  await runSteps({
    page,
    userFlow: 'PRISM-24',
    steps: [
      {
        description: 'Add your signature to the agreement.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the signature was recorded is shown.' }],
    test,
    expect,
  });
});
