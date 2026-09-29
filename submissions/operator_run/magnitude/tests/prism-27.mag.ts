import { test } from 'magnitude-test';

test('PRISM-27', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-27` }, async (agent) => {
  await agent.act('Like the post.');
  await agent.check('The post is shown as liked.');
});
