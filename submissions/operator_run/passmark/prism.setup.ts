import { configure } from 'passmark';

/**
 * Passmark configuration for a PRISM run. Imported by every test file.
 *
 * **No Redis configured — an infra gap, not a policy.** Passmark caches each
 * successful action and replays it on later runs when a REDIS_URL is present;
 * this run sets none, so there is no cache backend to replay from here.
 * `bypassCache` is deliberately NOT set: per `submissions/RANKED.md`, PRISM
 * measures what a cache's replay actually does against a moved seed rather
 * than forbidding the cache — "A cache that keeps working is a capability."
 * A vendor entry that does wire up Redis should leave it connected.
 *
 * **OpenRouter as the gateway.** Passmark wants a model from Anthropic and one
 * from Google for its assertion consensus; routing through OpenRouter serves
 * both from one key. `gateway` defaults to "none", so this must be explicit.
 */
configure({
  ai: {
    gateway: 'openrouter',
    // "snapshot" is the default: the agent perceives through the ARIA
    // accessibility tree and aria-ref locators. Stated rather than inherited,
    // because it is a claim about HOW this system perceives.
    mode: 'snapshot',
  },
});
