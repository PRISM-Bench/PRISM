import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-44', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-44');

  await runSteps({
    page,
    userFlow: 'PRISM-44',
    steps: [
      {
        description: 'View the report.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the report was generated is shown.' }],
    test,
    expect,
  });
});
