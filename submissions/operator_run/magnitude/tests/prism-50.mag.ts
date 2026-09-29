import { test } from 'magnitude-test';

test('PRISM-50', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-50` }, async (agent) => {
  await agent.act('Delete the user.');
  await agent.check('A confirmation that the user was deleted is shown.');
});
