import { test } from 'magnitude-test';

test('PRISM-46', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-46` }, async (agent) => {
  await agent.act('Pick something from the catalog and buy it.');
  await agent.check('A confirmation that the purchase succeeded is shown.');
});
