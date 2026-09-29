import { test } from 'magnitude-test';

test('PRISM-20', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-20` }, async (agent) => {
  await agent.act('Complete the action.');
  await agent.check('A confirmation that the action succeeded is shown.');
});
