import { test } from 'magnitude-test';

test('PRISM-18', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-18` }, async (agent) => {
  await agent.act('Open the Privacy Policy from the bottom of the page.');
  await agent.check('A confirmation that the privacy policy was opened is shown.');
});
