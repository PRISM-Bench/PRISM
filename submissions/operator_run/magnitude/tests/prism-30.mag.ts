import { test } from 'magnitude-test';

test('PRISM-30', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-30` }, async (agent) => {
  await agent.act('Place the order.');
  await agent.check('A confirmation that the order was placed is shown.');
});
