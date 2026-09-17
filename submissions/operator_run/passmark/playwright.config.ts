import { defineConfig } from '@playwright/test';
import dotenv from 'dotenv';

// Passmark reads OPENROUTER_API_KEY from the environment. Supply it however you
// prefer; an entry-local .env is read if present and nothing here writes a key
// to disk.
dotenv.config();

/**
 * Passmark is a Playwright *library*, so this file is the whole environment
 * contract — the agent runs inside Playwright and inherits everything below.
 * The settings PRISM pins are therefore pinned here once. A framework with no
 * project-level equivalent has to pin them per test instead; check, because a
 * silently ignored setting grades the run at the wrong viewport.
 */
export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  // `retries: 0` for two reasons here. A framework-level retry masks the timing
  // behaviour PRISM measures — and Passmark bypasses its action cache on a
  // Playwright retry, so a retried test would run under different rules than
  // the one being scored.
  retries: 0,
  // One worker. Playwright parallelises across FILES even at
  // `fullyParallel: false`, and each scenario is its own file, so the default
  // (half the host's cores) would run several scenarios at once. On a suite
  // built from timing traps that buys lenience: a loaded machine acts later and
  // lands after the seeded deadline, where it is graded as settled.
  workers: 1,
  reporter: [['list'], ['junit', { outputFile: 'results/junit.xml' }]],
  use: {
    // No default: an entry never bakes in a sandbox address. The operator
    // supplies it at run time, and validate_submission's declared_hosts_only
    // check fails any literal host an entry did not declare.
    baseURL: process.env.PRISM_SANDBOX_URL,
    // The pinned environment: 1280x720 at device scale factor 1 with no
    // reduced-motion preference. Stated explicitly so a config change cannot
    // move them silently.
    viewport: { width: 1280, height: 720 },
    deviceScaleFactor: 1,
    trace: 'off',
    actionTimeout: 20000,
  },
});
