import { test } from 'magnitude-test';

test('PRISM-49', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-49` }, async (agent) => {
  await agent.act('Drag the ticket card from To Do to Done.');
  await agent.check('A confirmation that the card reached Done is shown.');
});
