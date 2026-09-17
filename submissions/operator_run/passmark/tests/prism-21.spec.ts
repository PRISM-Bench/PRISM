import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-21', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-21');

  await runSteps({
    page,
    userFlow: 'PRISM-21',
    steps: [
      {
        description: 'Select the highest point on the chart.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the selection succeeded is shown.' }],
    test,
    expect,
  });
});
