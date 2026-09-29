import { test } from 'magnitude-test';

test('PRISM-19', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-19` }, async (agent) => {
  await agent.act('Review the summary, then continue.');
  await agent.check('A confirmation that the action succeeded is shown.');
});
