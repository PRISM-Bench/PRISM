import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-40', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-40');

  await runSteps({
    page,
    userFlow: 'PRISM-40',
    steps: [
      {
        description: 'Resume the session, confirming the prompt that appears.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the session was resumed is shown.' }],
    test,
    expect,
  });
});
