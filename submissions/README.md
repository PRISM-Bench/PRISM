# Submissions

PRISM measures how well an automated testing system — a scripted runner or
an autonomous agent — handles the **Perceptual Gap**: the divergence between
what the DOM reports and what a human actually perceives and can interact
with. Every run is scored on three dimensions — Deterministic Reliability,
Semantic Synchronization, and Intent Alignment — combined into the Resilience &
Perception Score (RPS). See [`docs/whitepaper.md`](../docs/whitepaper.md)
for what RPS measures and why, and
[`docs/methodology.md`](../docs/methodology.md) for how a run is scored.

## How to enter

Entries arrive privately, through an intake form. **Not by pull request** — see
[below](#this-repository-does-not-take-content-pull-requests) for why. Three
steps:

1. **Build against the contract.** [`CONTRACT.md`](CONTRACT.md) has the
   `metadata.yaml` schema, the test-file shape, and the environment your
   harness must run under. [`TEMPLATE/`](TEMPLATE/) is that shape as files.
2. **Self-check.** Run the same validator the operator runs on receipt
   ([`CONTRACT.md` §3](CONTRACT.md#3-self-check-before-you-submit)). It reports
   every contract failure and exits non-zero, so you find them before we do.
3. **Ask for a dry run.** One unscored pass, so the first time your harness
   meets the sandbox is not the round that counts. [See below](#the-dry-run).
4. **Submit the form.** Upload your entry as a single archive whose root is the
   directory holding `metadata.yaml`, and declare the archive's SHA-256.

<!-- TODO(operator): replace with the live intake form URL before the
     visibility flip. Greppable token: PRISM_INTAKE_FORM_URL -->

**Intake form:** `PRISM_INTAKE_FORM_URL` — _not published yet; the link appears
here when the first round opens, announced through the same channel as this
repo's releases._

**How your entry is run and scored:** see [`RANKED.md`](RANKED.md) — the
scenario set, seeds, result granularity, and cadence. Your suite stays private;
what gets published from your submission is the score and the archive's
SHA-256.

## Before you enter: two things that decide whether it's worth it

**Scripted runners are at a structural disadvantage on the ranked set.**
Ranked scenarios are authored blind from the published specs — you get the
scenario's `id`, `name`, `category` and `difficulty`, plus its `summary`,
`goal`, `success_signal` and a settled-state `screenshot` (and, for a handful
of scenarios, sample `inputs`) — never
its behavioral description, its failure mode, or the page itself. A
selector-based suite can't be written against markup you've never seen, so a
traditional scripted framework is starting all 50 at a real disadvantage
relative to a system that perceives the page at run time. This
is stated here, not discovered by you after a quarter's work scoring near
zero: the operator also runs a Playwright baseline against the same ranked
set, so the comparison still exists and you can see where a conventional
scripted approach lands.

**You never get to run against a PRISM sandbox.** Not before the round, not
during it, not afterwards. There is no practice environment and none is
planned: every scenario is ranked, and a scenario a vendor can execute against
repeatedly is a scenario that has been solved by observation rather than by
perception. What you author against is the [published scenario
specs](../data/scenarios/) — each with a summary, a goal, a success signal and
a settled-state screenshot — plus `CONTRACT.md`. What you get to execute
against is your own application, or any page you like; the harness contract is
small enough (drive a browser to `/scenarios/PRISM-NN`, attempt the task, emit
JUnit carrying `prism-NN`) that everything separating a working entry from a
broken one can be exercised without a PRISM page behind it. The dry run below
closes the rest of the gap.

## The dry run

Before a scored round, ask for one **unscored** pass. The operator runs your
entry exactly as a round would and reports back whether:

- your JUnit output parses
- its `prism-NN` tokens resolve to scenarios
- all 50 scenarios are covered by testcases that actually ran
- your declared hosts and timeouts look sane against what the run did

**No pass/fail results come back, and no scenario is named.** Not a summary, not
a count, not "the ones that timed out". That rule is the whole reason the dry
run can exist: per-scenario outcomes would make each dry run a free observation
round over the ranked set — practice by another name, and unbounded, since
nothing stops a vendor from asking again.

This is the division of labour with the offline validator. `validate_submission`
sees files: required keys, 50 filenames carrying resolvable tokens, no
undeclared host, no path escaping the entry. It deliberately **executes
nothing** — it is pointed at archives from strangers — so it cannot tell you
whether your reporter emits well-formed JUnit, whether your tokens survive into
the report, or whether your suite runs at all. The dry run is where those are
caught, and it is the only place they can be.

## Directory layout

Your entry never lands here. This directory carries the contract documents and
a template — nothing else:

```text
submissions/
  CONTRACT.md
  RANKED.md
  TEMPLATE/
    metadata.example.yaml
    momentic.config.yaml
    README.md
```

`TEMPLATE/` carries no test files. Its `metadata.example.yaml` keeps that name
so the validator does not mistake it for a real entry and fail it for covering
none of the 50 scenarios. `RANKED.md` has the quarterly cadence and what
"immutable once scored" means for a submitted archive.

## This repository does not take content pull requests

Everything here is generated from a private source repository and republished
wholesale: each publish deletes the tracked files and copies a fresh assembly
over the top. A merged pull request does not survive that — it is reverted or
deleted, in a commit that looks entirely routine. Rather than let contributed
work disappear that way, pull requests are not a contribution path here.

**Issues are open**, and are the right channel for:

- a question about the contract, a scenario spec, or a published result
- a **scenario proposal** — describe the perceptual failure you think PRISM
  does not yet cover, and what a human would perceive that a DOM query would
  not. Implementing one means building it in the private sandbox, so accepted
  proposals are built operator-side
- a correction to these documents
