# PRISM: A Benchmark for Evaluating Perceptual Reliability in Web Automation

**Author:** Amanul Chowdhury

**Date:** June 2026

**Version:** 1.0

### Abstract

Current End-to-End (E2E) testing methodologies rely heavily on Document Object Model (DOM) introspection and heuristic-based selectors. While AI-driven test generators have accelerated script creation, they have failed to address the fundamental "Perceptual Gap"—the divergence between a valid DOM state and a functional user-perceived state. This paper introduces **PRISM**, a standardized "stress test" for automated E2E web testing. It provides a rigorous methodology for evaluating how automated systems—ranging from scripted runners (Playwright, Cypress, Selenium) to autonomous AI testing agents—navigate the critical divergence between code-level DOM structures and actual human-perceived interfaces.

### 1. Problem Statement: The Limitations of DOM-Centric Heuristics

Traditional E2E automation (e.g., Playwright, Selenium) and contemporary LLM-driven wrappers operate on a **structural abstraction** of the interface rather than the **rendered reality**. This leads to three systemic failure modes:

- **State-Perception Divergence:** Elements may be logically present and interactable within the DOM while remaining visually occluded, transparent, or unrendered due to the complexities of the React hydration cycle and CSS-in-JS layout engines.
- **Semantic Fragility:** Heuristic selectors are brittle to "intent-neutral" mutations. A change in a button label from "Submit" to "Confirm" causes catastrophic failure in traditional scripts, whereas a "False Heal" in AI agents may lead to interacting with a visually similar but functionally incorrect neighbor.
- **Temporal Instability:** The rapid re-rendering of Single Page Applications (SPAs) creates transient windows of "Ghost Interactivity," where event listeners are not yet attached despite visual availability.

### 2. The PRISM Methodology

To quantify an automated system's ability to navigate these failures, we propose the **Resilience & Perception Score (RPS)**. Unlike binary pass/fail metrics, RPS evaluates the accuracy of the system's decisions during the interaction lifecycle.

#### 2.1 The RPS Formula

RPS measures deterministic reliability ($R$), semantic synchronization ($S$), and intent alignment ($I$); together these comprise **Resilience & Perception**. Each scenario is scored on the three dimensions **independently** — $R$ and $I$ are continuous (graded) and $S$ is the binary perception gate — then combined into a per-scenario **robustness** product $R \cdot S \cdot I$, averaged over the scenario's seeded variants. The headline **RPS** is the mean of that expected product across scenarios; PRISM also reports the **vector** of per-dimension means as a diagnostic:

$$
\text{RPS} = \frac{1}{n} \sum_{i=1}^{n} \mathbb{E}_{\text{seed}}\big[R_i \cdot S_i \cdot I_i\big] \qquad \mathbf{vector} = (\bar{R},\ \bar{S},\ \bar{I})
$$

Where:

- **$R$ (Deterministic Reliability):** The system's capability to synchronize with asynchronous UI transitions, layout stability, and React hydration events. _Graded by fumble severity._
- **$S$ (Semantic Synchronization):** The system’s ability to map visual affordances to functional goals regardless of label drift or component "morphing". _Binary perception gate._
- **$I$ (Intent Alignment):** The degree to which the system avoids "unauthorized healing"—refusing to interact with a target if its functional intent has drifted. _Graded by trap engagement._
- **$\bar{R}, \bar{S}, \bar{I}$:** The means of each dimension across all $n$ evaluated scenarios — the diagnostic **vector**, showing _which_ dimension a system fails. The single-number ranking scalar is the **RPS** itself (the mean of per-scenario products); the product of the dimension means $\bar{R} \cdot \bar{S} \cdot \bar{I}$ stays derivable from the vector but is no longer the headline — it over-penalises systems whose dimension failures fall in different scenarios.

PRISM is **report-only** and assigns no tier or built-in pass/fail. The dimensions are decoupled, so a consummated False Heal or intent violation zeroes $I$ alone (leaving $R$ and $S$ honest), while a detected cheat voids the whole triple. Consumers threshold the RPS themselves, and the vector reveals _which_ dimension a system fails. The grading constants for $R$ and $I$ are provisional, calibrated against real system distributions in a separate recalibration pass.

### 3. Taxonomy of Failure Scenarios

PRISM categorizes the "Perceptual Gap" into distinct architectural vectors targeting the most common drivers of automation flakiness.

| Category                 | Technical Focus       | Failure Vector                                                                                            |
| :----------------------- | :-------------------- | :-------------------------------------------------------------------------------------------------------- |
| **Hydration/Timing**     | React Lifecycle       | Race conditions between SSR render and active event-listener attachment leading to "Ghost Interactivity". |
| **Visual Occlusion**     | Z-Index/Layout Shift  | Physical target obstruction by transient UI layers, sticky headers, or Cumulative Layout Shifts (CLS).    |
| **Generative UI**        | Non-deterministic DOM | LLM-generated components that change structural DNA or labels while functional intent remains constant.   |
| **Graphics Blind Spots** | Canvas/WebGL/SVG      | Interaction requirements in layers where the traditional accessibility tree is absent or obfuscated.      |
| **State Logic**          | React Hooks/Context   | Interaction failures caused by stale closures or optimistic UI reversions.                                |

### 4. Towards Perceptual Alignment

The PRISM benchmark posits that a reliable web automation system must move beyond DOM-scraping to achieve **Perceptual Alignment**. This requires the integration of:

1. **Visual Verification:** The capability to verify the actual pixel-state of the viewport, accounting for layout shifts and contrast failures.
2. **Semantic Reasoning:** The ability to maintain functional continuity and logic-driven goal validation across dynamic UI mutations.
3. **Temporal Awareness:** The detection of layout stability and readiness before dispatching interaction events.

### 5. Conclusion & Future Work

PRISM provides the first standardized "stress test" for the next generation of automated web testing systems. By shifting the industry standard from **Structural Validation** to **Perceptual Alignment**, the benchmark ensures that "Green" test results reflect a truly functional and accessible user interface. Future iterations will expand into **Affective Computing** metrics to measure how UI performance impacts the "Perceptual Quality" of the application.
