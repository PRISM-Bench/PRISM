import { test, expect } from '@playwright/test';
import { runSteps } from 'passmark';
import '../prism.setup';

test('PRISM-49', async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto('/scenarios/PRISM-49');

  await runSteps({
    page,
    userFlow: 'PRISM-49',
    steps: [
      {
        description: 'Drag the ticket card from To Do to Done.',
      },
    ],
    assertions: [{ assertion: 'A confirmation that the card reached Done is shown.' }],
    test,
    expect,
  });
});
