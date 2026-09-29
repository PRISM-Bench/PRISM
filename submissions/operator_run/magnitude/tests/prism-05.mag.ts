import { test } from 'magnitude-test';

test('PRISM-05', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-05` }, async (agent) => {
  await agent.act('Pay for the order using the details below.', { data: { card_number: '4242 4242 4242 4242' } });
  await agent.check('A confirmation that the payment succeeded is shown.');
});
