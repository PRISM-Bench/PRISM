import { test } from 'magnitude-test';

test('PRISM-45', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-45` }, async (agent) => {
  await agent.act('Confirm the order.');
  await agent.check('A confirmation that the order succeeded is shown.');
});
