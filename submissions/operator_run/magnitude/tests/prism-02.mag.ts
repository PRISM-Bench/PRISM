import { test } from 'magnitude-test';

test('PRISM-02', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-02` }, async (agent) => {
  await agent.act('Complete the action.');
  await agent.check('A confirmation that the action succeeded is shown.');
});
