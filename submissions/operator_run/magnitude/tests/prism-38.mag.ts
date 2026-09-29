import { test } from 'magnitude-test';

test('PRISM-38', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-38` }, async (agent) => {
  await agent.act('Using only the keyboard, advance the signup to the next step.');
  await agent.check('A confirmation that the step advanced is shown.');
});
