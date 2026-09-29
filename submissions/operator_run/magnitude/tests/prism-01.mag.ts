import { test } from 'magnitude-test';

test('PRISM-01', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-01` }, async (agent) => {
  await agent.act('Submit the transaction.');
  await agent.check('A confirmation that the transaction succeeded is shown.');
});
