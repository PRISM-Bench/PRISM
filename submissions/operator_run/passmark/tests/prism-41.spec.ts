import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-41', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-41');

  await runSteps({
    page,
    userFlow: 'PRISM-41',
    steps: [
      {
        description: 'Export the report.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the export succeeded is shown.' }],
    test,
    expect,
  });
});
