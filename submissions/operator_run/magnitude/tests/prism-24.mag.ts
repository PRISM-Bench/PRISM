import { test } from 'magnitude-test';

test('PRISM-24', { url: `${process.env.PRISM_SANDBOX_URL}/scenarios/PRISM-24` }, async (agent) => {
  await agent.act('Add your signature to the agreement.');
  await agent.check('A confirmation that the signature was recorded is shown.');
});
