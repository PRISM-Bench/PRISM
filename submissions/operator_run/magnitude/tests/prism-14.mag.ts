import { test } from 'magnitude-test';

test('PRISM-14', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-14` }, async (agent) => {
  await agent.act('Cancel the order the assistant is showing.');
  await agent.check('A confirmation that the order was cancelled is shown.');
});
