import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-27', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-27');

  await runSteps({
    page,
    userFlow: 'PRISM-27',
    steps: [
      {
        description: 'Like the post.',
      },
    ],
    assertions: [{ assertion: 'The post is shown as liked.' }],
    test,
    expect,
  });
});
