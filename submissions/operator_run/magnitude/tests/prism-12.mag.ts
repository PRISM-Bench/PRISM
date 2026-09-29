import { test } from 'magnitude-test';

test('PRISM-12', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-12` }, async (agent) => {
  await agent.act('Enter the requested date in each of the three date fields. Save the schedule.');
  await agent.check('A confirmation that the schedule was saved is shown.');
});
