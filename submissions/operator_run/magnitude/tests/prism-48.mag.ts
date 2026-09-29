import { test } from 'magnitude-test';

test('PRISM-48', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-48` }, async (agent) => {
  await agent.act('Look up the receipt for this order and note the confirmation code it shows. Enter that code on the checkout form and finish the purchase.');
  await agent.check('A confirmation that the purchase went through is shown.');
});
