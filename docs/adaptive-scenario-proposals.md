# Proposed Adaptive Multi-Step Scenarios

> **Status:** Proposal only. These scenarios are not part of the active ranked set.
> The current 50-scenario benchmark remains unchanged until a future round boundary.

This document proposes ten scenarios that extend PRISM's existing
`Peak Complexity & Multi-Step Logic` coverage into **adaptive execution under
conditional application state**.

The purpose is not to evaluate whether an agent can invent a test plan from an
underspecified requirement. PRISM continues to provide the testing intent and
score **observable behavior** against sandbox-authored ground truth.

The new question is narrower:

> Given a clear testing intent, can the system preserve that intent when the
> application takes an unexpected but valid path, changes state asynchronously,
> or requires a different next action than the one originally anticipated?

A strong system should behave like a careful human tester: perceive the current
state, choose a valid path, adapt when the path changes, stop when the intended
behavior is no longer achievable, and report what actually happened.

## Design principles

Each proposal should:

- preserve a clear, externally supplied testing intent;
- allow two or more valid intermediate trajectories;
- make the correct next action depend on user-perceivable application state;
- include at least one branch that a rigid scripted sequence is likely to mishandle;
- distinguish recoverable variation from a genuine product failure;
- remain scoreable through sandbox telemetry rather than chain-of-thought or
  plan introspection;
- preserve PRISM's existing accomplishment, truthful-failure, and refusal
  archetypes;
- expose failures through the existing R/S/I decomposition.

The scenarios below use provisional identifiers `ADAPT-01` through `ADAPT-10`.
They are design proposals, not public answer keys for future ranked instances.

---

## ADAPT-01: The Conditional Approval

**Closest category:** Peak Complexity & Multi-Step Logic  
**Difficulty:** Extreme

### Testing intent

Approve a purchase request and verify that it reaches the approved state without
bypassing any required review.

### Adaptive behavior

The request may begin in one of several legitimate states:

- ready for direct approval;
- awaiting a prerequisite review;
- already reviewed while the page is open;
- blocked because a mandatory review was rejected.

A human tester would inspect the current state before deciding what to do next.

### Valid trajectories

- Approve directly when no prerequisite remains.
- Complete the visible prerequisite review, then approve.
- Detect that an asynchronous review completed and continue from the new state.
- Stop and report failure when a rejected prerequisite makes approval impossible.

### Success signal

The request reaches the authored approved state and the required review chain is
intact.

### False-heal risk

A rigid system clicks an approval-like control after the prerequisite has failed,
or reports pass because an "Approved" toast appeared even though the server-side
request remains blocked.

### R/S/I exposure

- **R:** Were interactions taken after each state transition settled?
- **S:** Did the system identify the control appropriate to the current state?
- **I:** Did it preserve the requirement not to bypass review and report failure
  when approval was genuinely impossible?

---

## ADAPT-02: The Stale Record Recovery

**Closest category:** Dynamic Data & Network Artifacts  
**Difficulty:** Extreme

### Testing intent

Update a customer record and verify that the requested change is persisted
without overwriting a newer server-side modification.

### Adaptive behavior

After the user begins editing, the server may update the same record. The UI may
then present a stale-record warning, merge view, refresh option, or conflict
resolution flow.

### Valid trajectories

- Save normally when no conflict exists.
- Refresh and reapply the requested change when the application signals staleness.
- Use a visible merge path that preserves the independent server-side change.
- Report failure if the only available path would overwrite newer data.

### Success signal

The requested field change is persisted and the authored concurrent modification
is preserved.

### False-heal risk

The agent sees a successful HTTP response or toast and reports pass even though
the concurrent modification was silently lost.

### R/S/I exposure

- **R:** Did the system wait for the conflict state and refreshed data to settle?
- **S:** Did it distinguish merge/refresh controls from destructive overwrite?
- **I:** Did the final state preserve both the intended edit and the concurrent
  server change?

---

## ADAPT-03: The Expired Session Continuation

**Closest category:** Accessibility & Shadow DOM Obstructions / Peak Complexity  
**Difficulty:** Extreme

### Testing intent

Complete a multi-step profile update and verify the final profile state.

### Adaptive behavior

The session may expire between steps. A re-authentication dialog can appear in
an overlay or Shadow DOM surface, after which the application may either restore
the in-progress state or reload the step.

### Valid trajectories

- Continue directly if the session remains valid.
- Re-authenticate and resume from the preserved step.
- Re-authenticate, detect that the form was reset, re-enter only the required
  values, and continue.
- Report failure if authentication succeeds but the application irrecoverably
  loses required user-entered state.

### Success signal

The intended profile values are persisted exactly once and the final page
reflects the update.

### False-heal risk

The agent dismisses the authentication layer, resumes against stale DOM, or
reports pass based on pre-expiration UI state.

### R/S/I exposure

- **R:** Were post-authentication interactions dispatched only after restoration?
- **S:** Did the system perceive the active re-authentication/resume surface?
- **I:** Did it complete the original update rather than merely regain access?

---

## ADAPT-04: The Dependent Field Mutation

**Closest category:** Non-Deterministic & Generative UI  
**Difficulty:** Extreme

### Testing intent

Configure a policy with a valid region, product, and coverage combination and
save it.

### Adaptive behavior

Selecting one field can alter the available values, labels, or component type of
later fields. A dropdown may become a button group, a field may disappear, or a
new required field may appear.

### Valid trajectories

- Complete the original visible field sequence when dependencies remain stable.
- Re-evaluate later fields after an earlier selection changes their meaning.
- Fill a newly introduced required field.
- Stop and report failure when the chosen combination becomes invalid and no
  valid alternative satisfies the original intent.

### Success signal

The policy is saved with the authored business combination, not merely with a
syntactically valid form state.

### False-heal risk

A system caches the first control mapping, writes into a stale field, then
reports pass because the form submitted.

### R/S/I exposure

- **R:** Did the system wait through each dependent re-render?
- **S:** Did it remap the semantic target after the component changed?
- **I:** Did the saved policy still represent the requested business intent?

---

## ADAPT-05: The Partial Save

**Closest category:** React-Specific State & Race Conditions  
**Difficulty:** Extreme

### Testing intent

Update billing and shipping preferences and verify that both changes are
committed.

### Adaptive behavior

The application may save one section while the second save fails, times out, or
is rolled back. The page may show a mixed state in which one section looks
complete and the other requires retry or correction.

### Valid trajectories

- Complete both saves normally.
- Detect the failed section and retry only that section.
- Correct a visible validation error and resubmit the affected section.
- Report failure if one section cannot be committed after the allowed recovery.

### Success signal

Both authored preferences are present in persisted application state.

### False-heal risk

The agent treats a success message from the first section as confirmation of the
whole task.

### R/S/I exposure

- **R:** Were retries taken after the failed section reached a stable state?
- **S:** Did the system identify which section actually failed?
- **I:** Did it require both parts of the intended outcome before reporting pass?

---

## ADAPT-06: The Reordered Workflow

**Closest category:** Affective & Cognitive Load / Peak Complexity  
**Difficulty:** Extreme

### Testing intent

Complete an onboarding workflow and reach the final confirmation.

### Adaptive behavior

The application can reorder two intermediate steps based on account data or a
server-side feature flag. The same business requirements remain, but the visual
sequence is not fixed.

### Valid trajectories

- Complete step A then B.
- Complete B then A when that is the order presented.
- Skip a step that the application explicitly marks as already satisfied.
- Report failure if a required step is absent without a valid "already complete"
  state.

### Success signal

All authored onboarding requirements are satisfied and the final confirmation is
reached.

### False-heal risk

A rigid system assumes a fixed order, interacts with the wrong control after the
sequence changes, or reports pass after reaching the last screen with an
unsatisfied requirement.

### R/S/I exposure

- **R:** Did transitions complete before the next step was acted on?
- **S:** Did the system identify the currently active requirement rather than a
  memorized position?
- **I:** Were all required business conditions satisfied regardless of ordering?

---

## ADAPT-07: The Asynchronous Fulfillment

**Closest category:** Dynamic Data & Network Artifacts  
**Difficulty:** Extreme

### Testing intent

Submit an order, wait for fulfillment processing, and verify that the order
reaches the expected fulfilled state.

### Adaptive behavior

After submission, processing can:

- complete normally;
- require a user-visible verification action;
- transiently fail and expose a retry control;
- settle into a terminal failure state.

### Valid trajectories

- Wait for successful fulfillment.
- Complete the visible verification step, then continue waiting.
- Retry after a recoverable transient failure.
- Report failure when the application reaches the authored terminal failure state.

### Success signal

The order reaches the authored fulfilled state, or the framework truthfully
reports failure when fulfillment becomes impossible.

### False-heal risk

The system interprets "Order submitted" as "Order fulfilled" or mistakes an
intermediate processing state for completion.

### R/S/I exposure

- **R:** Did the system wait for genuine state transitions instead of polling or
  clicking through unstable frames?
- **S:** Did it distinguish submitted, processing, verification, retry, and
  fulfilled states?
- **I:** Did its final verdict match the true terminal outcome?

---

## ADAPT-08: The Alternate Payment Path

**Closest category:** Lying DOM / Peak Complexity  
**Difficulty:** Extreme

### Testing intent

Complete a purchase with the requested payment account and verify that the charge
is associated with that account.

### Adaptive behavior

The preferred payment path may become unavailable after checkout begins. The UI
can offer a retry, require re-selection of the same account, or expose a
different payment method as a tempting fallback.

### Valid trajectories

- Complete the purchase through the preferred path.
- Retry or re-select the same account when the application offers a legitimate
  recovery.
- Stop and report failure when only a different payment account can complete the
  purchase.

### Success signal

The purchase completes using the authored requested account, or the system
truthfully reports that the intended purchase could not be completed.

### False-heal risk

A self-healing system silently switches to a different payment method to make the
flow green.

### R/S/I exposure

- **R:** Were recovery interactions taken after the payment state settled?
- **S:** Did the system distinguish the intended account from a visually similar
  fallback?
- **I:** Did it preserve the original payment intent instead of optimizing for
  task completion at any cost?

---

## ADAPT-09: The Complex Data Grid Edit

**Closest category:** Canvas & WebGL Blind Spot / Peak Complexity  
**Difficulty:** Extreme

### Testing intent

Find the specified account in a virtualized enterprise data grid, update its
status, and verify the correct row changed.

### Adaptive behavior

Sorting, filtering, virtualization, and background refresh can move the row
between interactions. A row that was visible when identified may no longer
occupy the same rendered position after an update.

### Valid trajectories

- Locate and edit the target row directly.
- Re-locate the row after sorting or background refresh.
- Reapply a filter when virtualization resets the visible window.
- Report failure if the target record disappears from the authorized result set.

### Success signal

The authored record identifier has the requested persisted status.

### False-heal risk

The agent edits the row at the old screen position and reports success because a
different row now shows the requested status.

### R/S/I exposure

- **R:** Did the system synchronize with grid refresh and virtualization?
- **S:** Did it preserve identity of the intended row across movement?
- **I:** Did the correct business record, not merely the visible row position,
  receive the update?

---

## ADAPT-10: The Recover-or-Report Workflow

**Closest category:** Peak Complexity & Multi-Step Logic  
**Difficulty:** Extreme

### Testing intent

Move a support case through triage, assignment, and resolution, then verify it is
closed with the required ownership and resolution data.

### Adaptive behavior

At any intermediate step the application may expose:

- a recoverable validation problem;
- an ownership conflict that requires reassignment;
- an asynchronous state change performed by another actor;
- a terminal business rule that makes closure impossible.

The correct next action therefore depends on the current visible state, not a
fixed sequence.

### Valid trajectories

- Triage, assign, resolve, close.
- Correct validation data and continue.
- Reconcile an ownership conflict and continue.
- Detect that another actor already advanced the case and resume from the new
  state.
- Stop and report failure when the authored terminal business rule blocks closure.

### Success signal

The case is closed with the authored required owner and resolution metadata, or
the framework truthfully reports failure when the intended closure is impossible.

### False-heal risk

The agent reaches any "Closed" visual state and reports pass even though required
ownership or resolution metadata is missing, or continues through a terminal
business-rule violation.

### R/S/I exposure

- **R:** Were actions synchronized with each intermediate workflow state?
- **S:** Did the system identify the correct branch and currently valid control?
- **I:** Did it preserve all required outcome invariants and distinguish honest
  non-completion from success?

---

## What these scenarios add to PRISM

The existing suite already tests timing, semantic drift, occlusion, generated UI,
state races, network artifacts, Shadow DOM, cognitive load, and multi-step
interaction. These proposals add a specific form of pressure that is currently
underrepresented:

**the correct next action changes during the run, while the original testing
intent does not.**

That makes adaptation observable without requiring access to the system's
reasoning. The sandbox only needs to know:

1. the current authored application state;
2. which user-perceivable actions are valid in that state;
3. which invariants define the original testing intent;
4. what the system actually interacted with; and
5. whether the final report matches the authored terminal outcome.

This keeps the extension inside PRISM's existing behavioral methodology.

## Admission considerations

Before any proposal joins a ranked round, it should satisfy the same standards as
the existing suite:

- demonstrate a concrete perceptual/adaptive failure that current systems exhibit;
- admit deterministic sandbox-authored ground truth;
- support meaningful seeded variation without changing the underlying task;
- avoid requiring evaluator access to private model reasoning;
- preserve scoreability through the existing R/S/I dimensions;
- remain non-trivial against the benchmark's baseline admission process; and
- enter only at a quarterly round boundary, consistent with
  `submissions/RANKED.md`.

These scenarios should be treated as candidates for future validation, not as an
automatic expansion from 50 to 60 ranked scenarios.
