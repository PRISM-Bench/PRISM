import { test } from 'magnitude-test';

test('PRISM-08', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-08` }, async (agent) => {
  await agent.act('Fill in the details below and create the account.', { data: { full_name: 'Ada Lovelace', email: 'ada.lovelace@example.com', password: 'Prism-08-trial' } });
  await agent.check('A confirmation that the account was created is shown.');
});
