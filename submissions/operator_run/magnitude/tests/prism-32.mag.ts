import { test } from 'magnitude-test';

test('PRISM-32', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-32` }, async (agent) => {
  await agent.act('Enter the profile details below, moving through each stage. Save the profile.', { data: { name: 'Ada Lovelace', email: 'ada.lovelace@example.com', phone: '+1 555 0142', location: 'London' } });
  await agent.check('The confirmation shows the name "Ada Lovelace".');
});
