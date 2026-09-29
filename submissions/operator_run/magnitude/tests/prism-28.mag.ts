import { test } from 'magnitude-test';

test('PRISM-28', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-28` }, async (agent) => {
  await agent.act('Approve the order in the Active orders list.');
  await agent.check('A confirmation that the order was approved is shown.');
});
