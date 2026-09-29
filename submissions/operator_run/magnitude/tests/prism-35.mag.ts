import { test } from 'magnitude-test';

test('PRISM-35', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-35` }, async (agent) => {
  await agent.act('Publish the article.');
  await agent.check('A confirmation that the article was published is shown.');
});
