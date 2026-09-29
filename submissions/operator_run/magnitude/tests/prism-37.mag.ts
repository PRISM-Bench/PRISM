import { test } from 'magnitude-test';

test('PRISM-37', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-37` }, async (agent) => {
  await agent.act('Open the help.');
  await agent.check('The help content is shown.');
});
