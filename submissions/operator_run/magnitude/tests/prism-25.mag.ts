import { test } from 'magnitude-test';

test('PRISM-25', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-25` }, async (agent) => {
  await agent.act('Advance the walkthrough to the checkpoint the page names, then confirm it.');
  await agent.check('A confirmation that the checkpoint was confirmed is shown.');
});
