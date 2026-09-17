import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-38', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-38');

  await runSteps({
    page,
    userFlow: 'PRISM-38',
    steps: [
      {
        description: 'Using only the keyboard, advance the signup to the next step.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the step advanced is shown.' }],
    test,
    expect,
  });
});
