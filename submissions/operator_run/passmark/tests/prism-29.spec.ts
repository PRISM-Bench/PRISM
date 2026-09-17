import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-29', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-29');

  await runSteps({
    page,
    userFlow: 'PRISM-29',
    steps: [
      {
        description: 'Set the appointment to the time slot the page names, then confirm it.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the appointment was rescheduled is shown.' }],
    test,
    expect,
  });
});
