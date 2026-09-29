import { test } from 'magnitude-test';

test('PRISM-43', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-43` }, async (agent) => {
  await agent.act('Fill in the card details below and place the order.', { data: { card_number: '4242 4242 4242 4242', name_on_card: 'Ada Lovelace' } });
  await agent.check('A confirmation that the order was placed is shown.');
});
