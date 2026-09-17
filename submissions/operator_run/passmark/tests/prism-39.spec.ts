import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-39', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-39');

  await runSteps({
    page,
    userFlow: 'PRISM-39',
    steps: [
      {
        description: 'Send a message through the contact form.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the message was sent is shown.' }],
    test,
    expect,
  });
});
