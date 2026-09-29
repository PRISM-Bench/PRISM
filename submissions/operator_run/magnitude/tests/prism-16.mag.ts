import { test } from 'magnitude-test';

test('PRISM-16', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-16` }, async (agent) => {
  await agent.act('Open the Edit control on the account settings row that has one.');
  await agent.check('A confirmation that the action succeeded is shown.');
});
