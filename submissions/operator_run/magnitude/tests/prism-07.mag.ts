import { test } from 'magnitude-test';

test('PRISM-07', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-07` }, async (agent) => {
  await agent.act('Create an account.');
  await agent.check('A confirmation that the account was created is shown.');
});
