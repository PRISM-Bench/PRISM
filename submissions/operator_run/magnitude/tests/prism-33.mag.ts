import { test } from 'magnitude-test';

test('PRISM-33', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-33` }, async (agent) => {
  await agent.act('Approve the refund for the order requested on the page.');
  await agent.check('A confirmation that the refund was approved is shown.');
});
