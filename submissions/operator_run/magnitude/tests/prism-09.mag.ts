import { test } from 'magnitude-test';

test('PRISM-09', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-09` }, async (agent) => {
  await agent.act('Confirm the booking.');
  await agent.check('A confirmation that the booking was placed is shown.');
});
