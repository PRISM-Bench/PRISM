import { test } from 'magnitude-test';

test('PRISM-26', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-26` }, async (agent) => {
  await agent.act('Update the profile name to the value below and save it.', { data: { name: 'Updated Name' } });
  await agent.check('The profile shows the updated name.');
});
