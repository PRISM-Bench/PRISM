import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-47', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-47');

  await runSteps({
    page,
    userFlow: 'PRISM-47',
    steps: [
      {
        description: 'Make a small edit to the draft. Undo that edit. Save the draft and confirm.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the draft was saved is shown.' }],
    test,
    expect,
  });
});
