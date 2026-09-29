import { test } from 'magnitude-test';

test('PRISM-47', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-47` }, async (agent) => {
  await agent.act('Make a small edit to the draft. Undo that edit. Save the draft and confirm.');
  await agent.check('A confirmation that the draft was saved is shown.');
});
