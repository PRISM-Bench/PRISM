import { test } from 'magnitude-test';

test('PRISM-22', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-22` }, async (agent) => {
  await agent.act('Pick a seat for the event and confirm it.');
  await agent.check('A confirmation that the seat was reserved is shown.');
});
