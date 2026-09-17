import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-23', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-23');

  await runSteps({
    page,
    userFlow: 'PRISM-23',
    steps: [
      {
        description: 'Drag the logo to the requested zone.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the logo landed in the right zone is shown.' }],
    test,
    expect,
  });
});
