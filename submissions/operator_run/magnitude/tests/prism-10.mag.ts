import { test } from 'magnitude-test';

test('PRISM-10', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-10` }, async (agent) => {
  await agent.act('Acknowledge the report.');
  await agent.check('A confirmation that the report was acknowledged is shown.');
});
