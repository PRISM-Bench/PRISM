import { test } from 'magnitude-test';

test('PRISM-44', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-44` }, async (agent) => {
  await agent.act('View the report.');
  await agent.check('A confirmation that the report was generated is shown.');
});
