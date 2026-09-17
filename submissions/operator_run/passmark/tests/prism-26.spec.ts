import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-26', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-26');

  await runSteps({
    page,
    userFlow: 'PRISM-26',
    steps: [
      {
        description: 'Update the profile name to the value below and save it.',
        data: { name: 'Updated Name' },
      },
    ],
    assertions: [{ assertion: 'The profile shows the updated name.' }],
    test,
    expect,
  });
});
