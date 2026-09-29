import { test } from 'magnitude-test';

test('PRISM-03', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-03` }, async (agent) => {
  await agent.act('Confirm the booking.');
  await agent.check('A confirmation that the booking succeeded is shown.');
});
