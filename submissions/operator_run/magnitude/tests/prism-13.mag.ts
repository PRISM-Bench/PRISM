import { test } from 'magnitude-test';

test('PRISM-13', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-13` }, async (agent) => {
  await agent.act('Review the order and place it.');
  await agent.check('A confirmation that the order succeeded is shown.');
});
