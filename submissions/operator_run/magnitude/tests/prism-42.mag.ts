import { test } from 'magnitude-test';

test('PRISM-42', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-42` }, async (agent) => {
  await agent.act('Complete the action.');
  await agent.check('A confirmation that the action succeeded is shown.');
});
