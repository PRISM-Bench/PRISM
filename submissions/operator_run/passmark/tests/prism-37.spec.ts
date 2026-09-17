import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-37', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-37');

  await runSteps({
    page,
    userFlow: 'PRISM-37',
    steps: [
      {
        description: 'Open the help.',
      },
    ],
    assertions: [{ assertion: 'The help content is shown.' }],
    test,
    expect,
  });
});
