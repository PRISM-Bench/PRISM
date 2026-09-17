import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-32', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-32');

  await runSteps({
    page,
    userFlow: 'PRISM-32',
    steps: [
      {
        description:
          'Enter the profile details below, moving through each stage. Save the profile.',
        data: {
          name: 'Ada Lovelace',
          email: 'ada.lovelace@example.com',
          phone: '+1 555 0142',
          location: 'London',
        },
      },
    ],
    assertions: [{ assertion: 'The confirmation shows the name "Ada Lovelace".' }],
    test,
    expect,
  });
});
