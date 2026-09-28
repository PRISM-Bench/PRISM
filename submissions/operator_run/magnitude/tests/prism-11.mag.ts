import { test } from 'magnitude-test';

test('PRISM-11', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-11` }, async (agent) => {
  await agent.act('Delete the account.');
  await agent.check('A confirmation that the account was deleted is shown.');
});
