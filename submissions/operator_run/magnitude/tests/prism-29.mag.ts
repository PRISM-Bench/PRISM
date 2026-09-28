import { test } from 'magnitude-test';

test('PRISM-29', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-29` }, async (agent) => {
  await agent.act('Set the appointment to the time slot the page names, then confirm it.');
  await agent.check('A confirmation that the appointment was rescheduled is shown.');
});
