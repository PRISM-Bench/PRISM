import { test } from 'magnitude-test';

test('PRISM-41', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-41` }, async (agent) => {
  await agent.act('Export the report.');
  await agent.check('A confirmation that the export succeeded is shown.');
});
