import { type MagnitudeConfig } from 'magnitude-test';

// Every setting that decides how honest this run is lives here or in
// metadata.yaml's run.command, never in a gitignored dotfile, so a reviewer
// reads it in the entry.
export default {
  // The sandbox address arrives per run. No literal host is written into this
  // entry — validate_submission's declared_hosts_only reads the entry's files.
  url: process.env.PRISM_SANDBOX_URL!,

  // Magnitude requires a visually grounded model; its README recommends Claude
  // Sonnet 4. Reached through OpenRouter via `openai-generic`, which is the
  // pattern magnitude-core's own bundled BAML config shows. Operator's model
  // choice, pinned and disclosed on the row.
  llm: {
    provider: 'openai-generic',
    options: {
      model: 'anthropic/claude-sonnet-4',
      baseUrl: 'https://openrouter.ai/api/v1',
      apiKey: process.env.OPENROUTER_API_KEY,
    },
  },

  // contextOptions are Playwright's own, so this is the graded viewport exactly
  // rather than a window size the browser subtracts its chrome from. Verified:
  // the sandbox's EnvironmentProbe read 1280x720, DSF 1, no reduced-motion.
  browser: {
    launchOptions: { headless: true },
    contextOptions: {
      viewport: { width: 1280, height: 720 },
      deviceScaleFactor: 1,
      reducedMotion: 'no-preference',
    },
  },

  // Analytics are on by default (posthog-node is a dependency).
  telemetry: false,

  // Magnitude FAILS FAST by default. On PRISM a failure is the correct answer on
  // several scenarios, so without this a round would abandon itself almost
  // immediately while still exiting as though it had a verdict. run_prism.py
  // invokes one scenario at a time and also passes --no-fail-fast, so this is
  // belt and braces rather than the only control.
  continueAfterFailure: true,
} satisfies MagnitudeConfig;
