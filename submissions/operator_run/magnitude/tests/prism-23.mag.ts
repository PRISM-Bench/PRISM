import { test } from 'magnitude-test';

test('PRISM-23', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-23` }, async (agent) => {
  await agent.act('Drag the logo to the requested zone.');
  await agent.check('A confirmation that the logo landed in the right zone is shown.');
});
