import { test } from 'magnitude-test';

test('PRISM-21', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-21` }, async (agent) => {
  await agent.act('Select the highest point on the chart.');
  await agent.check('A confirmation that the selection succeeded is shown.');
});
