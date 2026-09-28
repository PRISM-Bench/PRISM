import { test } from 'magnitude-test';

test('PRISM-34', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-34` }, async (agent) => {
  await agent.act('Buy the asset the page asks for, then confirm the purchase.');
  await agent.check('A confirmation that the purchase succeeded is shown.');
});
