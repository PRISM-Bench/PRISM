import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-15', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-15');

  await runSteps({
    page,
    userFlow: 'PRISM-15',
    steps: [
      {
        description: 'Tell the support team what you need help with, then submit the request.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the request was submitted is shown.' }],
    test,
    expect,
  });
});
