import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-10', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-10');

  await runSteps({
    page,
    userFlow: 'PRISM-10',
    steps: [
      {
        description: 'Acknowledge the report.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the report was acknowledged is shown.' }],
    test,
    expect,
  });
});
