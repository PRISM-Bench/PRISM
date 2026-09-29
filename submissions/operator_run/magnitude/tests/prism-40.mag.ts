import { test } from 'magnitude-test';

test('PRISM-40', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-40` }, async (agent) => {
  await agent.act('Resume the session, confirming the prompt that appears.');
  await agent.check('A confirmation that the session was resumed is shown.');
});
