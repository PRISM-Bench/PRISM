import { test } from 'magnitude-test';

test('PRISM-39', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-39` }, async (agent) => {
  await agent.act('Send a message through the contact form.');
  await agent.check('A confirmation that the message was sent is shown.');
});
