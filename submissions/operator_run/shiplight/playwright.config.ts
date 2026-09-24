import { defineConfig, shiplightConfig } from 'shiplightai';

/**
 * shiplight transpiles each `*.test.yaml` into a Playwright spec and runs it,
 * so this file is the whole environment contract — the agent runs inside
 * Playwright and inherits everything below. `shiplightConfig()` supplies the
 * YAML transpilation; the settings PRISM pins are stated here rather than
 * inherited, because a silently ignored setting grades the run at the wrong
 * viewport.
 *
 * The reporter list deliberately replaces shiplight's own. Its HTML reporter
 * feeds `npx shiplight report`, which uploads results to the vendor's cloud,
 * and a scored run publishes nothing anywhere but the operator's own record.
 */
export default defineConfig({
  ...shiplightConfig(),
  testDir: './tests',
  fullyParallel: false,
  // A framework-level retry masks the timing behaviour PRISM measures: a
  // scenario that fails a hydration race on the first attempt and passes on
  // the second is a scenario the framework did not perceive.
  retries: 0,
  // One worker. Playwright parallelises across FILES even at
  // `fullyParallel: false`, and each scenario is its own file, so the default
  // (half the host's cores) would run several scenarios at once. On a suite
  // built from timing traps that buys lenience: a loaded machine acts later
  // and lands after the seeded deadline, where it is graded as settled.
  workers: 1,
  reporter: [['list'], ['junit', { outputFile: 'results/junit.xml' }]],
  use: {
    // No default: an entry never bakes in a sandbox address. The operator
    // supplies it at run time, and validate_submission's declared_hosts_only
    // check fails any literal host an entry did not declare.
    baseURL: process.env.PRISM_SANDBOX_URL,
    // The pinned environment: 1280x720 at device scale factor 1 with no
    // reduced-motion preference. Confirmed against the sandbox's own
    // `environment` telemetry event on a PRISM-01 run.
    viewport: { width: 1280, height: 720 },
    deviceScaleFactor: 1,
    trace: 'off',
  },
});
