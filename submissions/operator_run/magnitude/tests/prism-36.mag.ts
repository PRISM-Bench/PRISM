import { test } from 'magnitude-test';

test('PRISM-36', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-36` }, async (agent) => {
  await agent.act('Add two of the product to the cart.');
  await agent.check('A confirmation that both items were added to the cart is shown.');
});
