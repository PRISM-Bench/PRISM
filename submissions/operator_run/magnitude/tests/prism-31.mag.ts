import { test } from 'magnitude-test';

test('PRISM-31', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-31` }, async (agent) => {
  await agent.act('Review the cart and check out.');
  await agent.check('A confirmation that the checkout succeeded is shown.');
});
