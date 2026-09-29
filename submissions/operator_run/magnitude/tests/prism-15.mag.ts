import { test } from 'magnitude-test';

test('PRISM-15', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-15` }, async (agent) => {
  await agent.act('Tell the support team what you need help with, then submit the request.');
  await agent.check('A confirmation that the request was submitted is shown.');
});
