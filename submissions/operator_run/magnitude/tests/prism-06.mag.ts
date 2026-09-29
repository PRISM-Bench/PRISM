import { test } from 'magnitude-test';

test('PRISM-06', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-06` }, async (agent) => {
  await agent.act('Confirm the order.');
  await agent.check('A confirmation that the order was confirmed is shown.');
});
