# PRISM: Perceptual Reliability & Intent-based Software Measurement

> **Status:** What this repository publishes is the **task** and the **metric** — the 50 lean scenario specs, and the scoring implementation in `evaluators/scoring/`. The sandbox that implements those scenarios is deliberately private: a self-judging sandbox cannot be published without publishing its answers. PRISM claims no immunity from gaming — the boundary raises the cost of it rather than eliminating it, and `docs/methodology.md` §5.5 states each integrity measure alongside its limit.

## Abstract: Bridging the Perceptual Gap in Automated E2E Testing

Modern End-to-End (E2E) testing is currently bottlenecked by a **Perceptual Gap**: the systemic divergence between the Document Object Model (DOM) and the rendered user experience. While Generative AI and MCP-based tools have accelerated test authorship, they continue to rely on structural heuristics that are inherently brittle to React hydration cycles, asynchronous state transitions, and non-deterministic UI mutations.

**PRISM** is a standardized "stress test" for **automated E2E web testing**. It provides a rigorous, vendor-neutral methodology for evaluating how automated systems—ranging from scripted runners (Playwright, Cypress, Selenium) to autonomous AI testing agents—navigate the critical divergence between code-level DOM structures and actual human-perceived interfaces.

By moving beyond binary pass/fail metrics, PRISM introduces the **Resilience & Perception Score (RPS)**: a multi-dimensional framework that establishes a new high-water mark for reliability, safety, and intent-alignment by quantifying an automated system's ability to resolve:

- **Temporal Instability:** Race conditions between SSR/Static rendering and active event-listener attachment that lead to "Ghost Interactivity."
- **Visual Occlusion:** Functional targets obstructed by transient UI layers, sticky headers, or Cumulative Layout Shifts (CLS) that intercept interaction events.
- **Semantic Drift:** Component "morphing" and label mutations where functional intent remains constant despite radical structural or textual changes.
- **Graphics Blind Spots:** Interaction requirements in Canvas, WebGL, and Shadow DOM environments where the traditional accessibility tree is absent or obfuscated.

The goal of this benchmark is to shift the industry standard from **Structural Validation** (did the code load?) to **Perceptual Alignment** (can the user interact?). PRISM ensures that "Green" test results in CI/CD reflect a truly functional, stable, and accessible user experience.

---

### The RPS Framework

Each automated system is scored on three independent dimensions. Each scenario's robustness is the product $R \cdot S \cdot I$ (averaged over its seeded variants); the headline **RPS** is the mean of that product across scenarios, reported with the diagnostic vector of per-dimension means $(\bar{R}, \bar{S}, \bar{I})$:

$$
\text{RPS} = \frac{1}{n} \sum_{i=1}^{n} \mathbb{E}_{\text{seed}}\big[R_i \cdot S_i \cdot I_i\big] \qquad \mathbf{vector} = (\bar{R},\ \bar{S},\ \bar{I})
$$

- **$R$ (Deterministic Reliability):** Synchronization with layout stability and React lifecycle. _Continuous (graded)._
- **$S$ (Semantic Synchronization):** Functional intent mapping across dynamic UI mutations. _Binary perception gate._
- **$I$ (Intent Alignment):** Guarding against "False Heals" and unauthorized autonomous actions. _Continuous (graded)._

---

### Key Research Pillars

#### 1. Bridging the Perceptual Gap

Modern React and SPA frameworks create a delta between when an element is "Visible" in the DOM and when it is "Interactive" for a human. PRISM codifies that delta as a measurable metric to ensure tests don't just pass in code, but succeed in the user's hand.

#### 2. Behavioral Scoring via Authored Ground Truth

PRISM evaluates systems on what they _did_, not what they reasoned. Because the sandbox owns the chaos timeline — it injects every hydration delay, layout shift, and label mutation — it emits ground-truth telemetry with certainty and scores against it. There is no external perception model to fool: a run’s R · S · I comes from the sandbox’s own record of the interaction (see `docs/methodology.md` §3).

---

> Each scenario yields a triple $(R, S, I)$, each in $[0, 1]$ and scored **independently** — $R$ and $I$ continuous, $S$ the binary perception gate. A consummated False Heal or intent violation zeroes $I$ alone, leaving $R$ and $S$ honest; a detected cheat voids the whole triple. The scenario's robustness is the product $R \cdot S \cdot I$, averaged over seeds; the headline **RPS** $\in [0, 1]$ is the mean of that product across scenarios, reported alongside the diagnostic vector $(\bar{R}, \bar{S}, \bar{I})$.

PRISM is **report-only**: it publishes the RPS and the vector and assigns no tier or built-in pass/fail. Consumers threshold the RPS on their own terms, and the vector shows _which_ dimension a system fails — information a single collapsed score discards.

---

### Repository Structure

- `/data/scenarios`: The 50 public lean specs — each scenario's summary, goal, inputs, success signal and settled-state screenshot.
- `/evaluators/scoring`: Python logic that computes the **RPS Score** from sandbox telemetry.
- `/submissions`: The submission contract, how ranked runs work, and the maintainers' reference entry. Vendor entries arrive privately and are not published here (see `submissions/README.md`).
- `/docs`: The **PRISM White Paper**, the methodology, the generated benchmark taxonomy (`docs/benchmark.md`), and one settled-state screenshot per scenario (`docs/screenshots/`).

### What this repository is, and is not

- **The published evaluator will not run end-to-end.** The sandbox that generates
  the telemetry it scores is not public. `evaluators/scoring/` is an auditable
  artefact — every claim the metric makes can be checked against it — not a
  runnable harness.
- **The Playwright baseline behind the headline comparison is operator-reported,
  not reproducible by third parties.** It was run by the operator against the
  private sandbox. Treat it as a reported figure, not a replication.

---

### About the Author

A full-stack developer with over 15 years of experience building complex web applications and single-page applications (React, Angular, etc.). His work focuses on the intersection of AI tools and software development and reliability.

---

### Citation

If you use this benchmark in your research or commercial evaluation, please cite it as follows:

```bibtex
@software{prism_2026,
  author = {Chowdhury, Amanul},
  title = {PRISM: Perceptual Reliability & Intent-based Software Measurement},
  year = {2026},
  url = {https://github.com/PRISM-Bench/PRISM}
}

```

---

### Contributing

Scenario proposals are welcome — open an issue describing the perceptual failure you think PRISM does not yet cover, and what a human would perceive that a DOM query would not. Implementing a scenario means building it in the private sandbox, so accepted proposals are built operator-side. To enter a framework, see **Submitting your framework** below.

**Issues, not pull requests.** This repository is a generated artifact: it is republished wholesale from a private source, so a merged pull request is reverted or deleted at the next publish. Rather than let contributed work disappear that way, content pull requests are not a path here — issues are.

---

### Submitting your framework

Entries arrive privately, through an intake form — not by pull request. See
[`submissions/README.md`](submissions/README.md) for how to enter and
[`submissions/CONTRACT.md`](submissions/CONTRACT.md) for what a valid entry
must contain. Submitted entries are run each quarter against a private,
held-out seed set and the results published to the leaderboard. Your suite
itself stays private: what is published is your score and the SHA-256 of the
archive you submitted.

### Leaderboard

Rankings and downloadable per-submission JSON results are published at the PRISM
leaderboard (link coming soon).
