import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-19', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-19');

  await runSteps({
    page,
    userFlow: 'PRISM-19',
    steps: [
      {
        description: 'Review the summary, then continue.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the action succeeded is shown.' }],
    test,
    expect,
  });
});
