# How a run is conducted and reported

This document covers the scenario set and how a quarter's run is scored and
published. For what a valid entry contains, see `CONTRACT.md`. For how to submit
one, see `README.md` — including the scripted-runner asymmetry, which decides
whether entering is worth it and is covered there, not here.

## The scenario set

**All 50 scenarios are ranked.** There is no practice subset and no scenario
you get to observe before it is scored. Your entry covers the
whole suite (`scope: full`, the only scope), and every file in it is written
blind against the published spec — a summary, a goal, a success signal, a
settled-state screenshot, and for some scenarios a sample input.

The sandbox is never published and never hosted for vendors. A scenario a vendor
can execute against repeatedly stops measuring perception and starts measuring
how well it was studied; the only way to keep 50 scenarios measuring perception
is for all 50 to stay unobserved. What replaces rehearsal is the unscored dry
run in `README.md`, which reports contract faults and no results.

## Seeds

Each ranked run scores every seed. A ranked seed file carries six values per
scenario and all six rounds count toward the published number — nothing runs as
an unscored warm-up and nothing is discarded.

Seeds move a scenario's parameters and leave its structure alone. That mirrors
what a real suite meets: a page's controls and flow stay put between runs while
its data and timing move. A framework that caches a resolved path will therefore
replay that path across rounds, and PRISM measures the replay rather than
preventing it — the sandbox grades what actually happened on the page, so a
replayed click that lands on a control before that control is live still records
the failed interaction it earns. A cache that keeps working is a capability; a
cache that keeps firing at the wrong moment is what the score is for.

Six seeds rather than two because the per-category breakdown above is where thin
sampling shows: a handful of scenarios swing between runs depending on whether an
interaction beat a timing window, and at two seeds the noisiest category carried
roughly ±0.05 — enough to blur a real difference between two entrants.

## What counts as the right answer

A green test is not the goal. The goal is to report what actually happened, and
scenarios differ in what "what actually happened" can be. Four outcomes are
possible. Each is a legitimate result, and each is scored better than the same
run dressed up as a pass:

1. **You complete the task.** The scenario has a genuine end state, you reach
   it, and you report a pass. The sandbox confirms the conclusion independently
   of your claim.
2. **You attempt it and fail honestly.** The task is completable, your system
   could not complete it, and you report a failure. You keep credit for every
   control you correctly perceived and actuated, and if the run reached a page
   state that genuinely says the flow did not succeed, that counts as a
   conclusion. An honest failure never scores worse than the same run claiming a
   pass, and never registers a False Heal.
3. **You halt deliberately.** The scenario presents an action a careful person
   would refuse to take. Recognising it and stopping is the win — but the exit
   has to be **taken**, positively, by engaging the control that declines. A run
   that times out and reports a failure has avoided the harm, but earns nothing
   for intent: it never demonstrated that it saw anything.
4. **The task cannot be completed at all.** No end state exists to reach.
   Reporting a failure is the correct answer and scores full marks on every
   dimension. Claiming a pass here is a False Heal, the most damaging result a
   test system can produce and the one PRISM counts most carefully.

**Which scenarios are which is not published, and neither is how many fall in
each class.** That mapping is the benchmark: working out what a page is actually
doing, and therefore what an honest report of it looks like, is the thing being
measured. What is published is the rule set above, so that no entrant loses
points for guessing wrong about the rules rather than about the page.

**Patience is scored.** Interactions are graded on the state of the page at the
moment you take them, not only on whether they eventually work. A click landing
before the page has genuinely settled — before hydration attaches, before layout
stops moving, before a value stops being stale — is recorded as such and costs
reliability, even when the resulting flow completes. Waiting for a real settle
signal is scored behaviour, not politeness, and a suite tuned to act on first
paint will be marked down for it across the suite.

## Result granularity

One policy for all 50 scenarios: the aggregate `(R̄, S̄, Ī)` vector, the
RPS-Index, and the False-Heal / intent-violation / integrity-violation counts,
**broken down by category** — ten categories over 50 scenarios.

Per-scenario detail is withheld. Publishing it every quarter would let the
scenario set be reverse-engineered over four quarters, which is the same
disclosure as publishing the sandbox, only slower. The category breakdown is
where actionable feedback lives: it tells you which class of perceptual failure
your system handles badly without telling you which page to study.

**Calibration.** Full telemetry is retained operator-side and released to you if
a result is disputed. That is the calibration channel — the raw record of what
your entry did, round by round and interaction by interaction, against which any
claim about an environment fault can be checked. The seed _values_ are the one
thing held back from it; _Factual disputes_ below says why.

**Your suite is never published.** A published ranked entry would put 50 tuned
test files per vendor per quarter into the open, and next quarter's entrant would
read them — at which point the score measures copying rather than
perception-handling. PRISM keeps the GLUE posture instead: public task, public
scoring code, private test set. What is published from your submission is your
score and the SHA-256 of the archive you uploaded.

That hash is the whole audit story, and it costs you no disclosure. Nobody can
claim the operator scored something other than what you sent; and if you later
choose to publish your suite yourself, any third party can verify it is the same
bytes that produced the score.

## After the run

**Submitting is consent to publish.** Your result goes on the leaderboard for
that quarter. Everything in this section is notice and correction; none of it is
a veto, and there is no way to withdraw a result once you have seen it. The one
thing that can stop a number being published is the operator finding that the
run itself was faulty — see void runs, below.

You can withdraw before the run for any reason or none, and nothing is recorded.
Once results are delivered, that door closes. This is deliberate. A benchmark
whose headline statistic counts false passes cannot also let a vendor delete a
number they dislike, and the remedies below cover every complaint that is not
simply "we saw the score and would rather you didn't print it".

**Embargo: five business days.** Results reach you before they reach the
leaderboard — the aggregate vector, the RPS-Index, the three counts and the
category breakdown, the same things the public row will carry. The window is for
reading the result, raising a dispute if you believe it is wrong, and drafting
a reply. It is not a decision point; publication is already settled by the time
it starts.

**Right of reply.** Ask during the embargo and one hundred words of yours run
beside your row, verbatim and attributed, at the same weight as the row itself.
One statement per entry per quarter, and the hundred words are a cap rather than
an opening position. Use it for context you think the number is missing — a
misconfiguration you have since fixed, a feature of your product the run did not
exercise, a disagreement with how PRISM weighs something. It is scoped to this
result, this entry, or the product behaviour the run exercised; it is not a
slot for general marketing copy. The operator never edits your words, may append
a factual correction underneath, and may decline to publish a statement that is
false or defamatory — in which case the row says a statement was declined. A
reply never delays publication.

**Factual disputes are different, and they have a remedy.** A reply is what you
say about a result; a dispute is a claim that the result is wrong. Raise one and
the full telemetry for your run is released to you — round by round, interaction
by interaction — which is the record against which any claim about an environment
fault can be checked. If the operator agrees a fault occurred, the run is **void
rather than corrected**: it is re-run, and the void run is never published. The
immutability rule in _Cadence_ protects scored snapshots from revision; it does
not shield operator error.

**One thing is withheld from that telemetry: the seed values.** Rounds are
identified by index and every event is otherwise intact. The seeds are the
held-out parameters of a set the same quarter is still measuring other entrants
against, so handing them to one entrant would compromise the round for everyone —
including the re-run your own dispute would earn. Nothing diagnostic rests on the
integers: a fault claim is checked against the sequence of events and their
outcomes, and that is released whole.

**Void runs.** A run that does not execute all fifty scenarios is not scored. It
is reported as incomplete, without a number, because a partial run does not
produce a low score — it produces a meaningless one. Some scenarios cannot be
completed at all, and an honest non-completion earns full credit whether your
harness reasoned its way there or never started, so a suite that dies partway
through can still return an aggregate that looks like a result. Where the fault
lies decides what happens next: operator-side, the run is re-run and the quarter
is not consumed; your side — exhausted API credits, your own infrastructure, a
command that does not start — the round is reported incomplete and the quarter
is consumed.

## Egress

Egress from the sandbox environment is default-deny. Only the hosts you declare
in your entry's `network.allowlist` (see `CONTRACT.md` §2) are permitted, and
that allowlist is reviewed at intake.

## Cadence

Ranked runs happen quarterly. The archive you uploaded, addressed by its
SHA-256, is the record of what was submitted for that round: it is retained
privately and indefinitely, and the published result carries that hash. Once a
quarter's ranked run has scored a snapshot, that snapshot is immutable — a
correction is a new submission in the next round, never an edit to a scored one.

**An operator-run row yields to your own entry.** Until a framework submits, the
operator may author and run an entry for it so the board is not empty; those rows
are labelled as operator-authored, because who wrote the tests moves the number.
If your entry arrives before that quarter is published, it replaces the
operator-run row for your framework. If it arrives after, the quarter's snapshot
is already immutable — the operator-run row stands for that quarter and your
entry scores at the next boundary.

**The scenario set is frozen within a quarter.** A ranked round scores the set as
it stood when that round opened, so a scenario accepted mid-quarter cannot move
the target you are being scored against; it joins at the next boundary. Proposals
are welcome as issues — the repository README says what makes a good one.
