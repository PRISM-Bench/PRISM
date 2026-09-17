import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-12', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-12');

  await runSteps({
    page,
    userFlow: 'PRISM-12',
    steps: [
      {
        description:
          'Enter the requested date in each of the three date fields. Save the schedule.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the schedule was saved is shown.' }],
    test,
    expect,
  });
});
