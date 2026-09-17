import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-35', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-35');

  await runSteps({
    page,
    userFlow: 'PRISM-35',
    steps: [
      {
        description: 'Publish the article.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the article was published is shown.' }],
    test,
    expect,
  });
});
