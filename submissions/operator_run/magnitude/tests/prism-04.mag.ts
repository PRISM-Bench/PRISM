import { test } from 'magnitude-test';

test('PRISM-04', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-04` }, async (agent) => {
  await agent.act('Enter the email address below and confirm it.', { data: { email: 'tester@example.com' } });
  await agent.check('A confirmation that the submission succeeded is shown.');
});
