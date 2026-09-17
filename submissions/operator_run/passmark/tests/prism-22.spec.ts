import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-22', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-22');

  await runSteps({
    page,
    userFlow: 'PRISM-22',
    steps: [
      {
        description: 'Pick a seat for the event and confirm it.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the seat was reserved is shown.' }],
    test,
    expect,
  });
});
