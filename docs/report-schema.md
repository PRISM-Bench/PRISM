# PRISM Evaluator Report Schema

The evaluator writes a JSON report. At launch these
become permanent public artefacts under `runs/<quarter>/<vendor>.json`, read by the
leaderboard generator and the audit script. `schema_version` lets a consumer tell a
shape it understands from a foreign one, instead of silently mis-reading it.

## Envelope

| Field                                                                   | Meaning                                                                                                                                                                                                           |
| :---------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schema_version`                                                        | File format version, semver `MAJOR.MINOR`.                                                                                                                                                                        |
| `seed_set_id`                                                           | Which seed set produced the run (e.g. `2026-Q3-scored`); `null` for a single fixed-surface run.                                                                                                                   |
| `sandbox_version`                                                       | Sandbox commit scored against (short git sha); `null` if undetectable.                                                                                                                                            |
| `system`                                                                | The system under test: `{ "name", "version" }`, or `null` if not supplied.                                                                                                                                        |
| `generated_at`                                                          | UTC ISO-8601 timestamp the run started — stamped before the SUT command runs, not after scoring; it also names the run's archive directory.                                                                       |
| `command` / `exit_code`                                                 | The test command, and (single-run only) its exit code.                                                                                                                                                            |
| `index`                                                                 | Headline RPS — mean over scenarios of `E_seed[R·S·I]`, in `[0, 1]`. Percentage is `index * 100`.                                                                                                                  |
| `rps`, `R_mean`/`S_mean`/`I_mean`                                       | The diagnostic `(R̄, S̄, Ī)` vector.                                                                                                                                                                                |
| `n`, `n_seeds`, `n_runs`, `worst_case`                                  | Scenario / seed counts and the worst-case floor.                                                                                                                                                                  |
| `false_heals`, `intent_violations`, `integrity_violations` (+ `*_runs`) | Fairness counts.                                                                                                                                                                                                  |
| `scenarios`                                                             | Per-scenario summaries (see `aggregate_scenario`).                                                                                                                                                                |
| `categories`                                                            | Per-category summaries — one row per category present in the run; ten for a complete 50-scenario run. Each carries its own vector, index, scenario count and fairness counts. The published feedback granularity. |
| `environment`                                                           | The pinned envelope plus observed readings, violations and missing; report-only, never scored.                                                                                                                    |
| `sandbox_mode`                                                          | The sandbox's build mode from `/api/health`: `production`, `development`, or `unknown`.                                                                                                                           |

## Versioning policy

- **Minor bump** (`1.0 → 1.1`) — additive, backward-compatible (a new field/stat).
  Consumers **must ignore unknown keys**, so `1.0`-built code reads a `1.4` report.
- **Major bump** (`1.x → 2.0`) — breaking (renamed/removed field, type change,
  restructured `scenarios[]`). A consumer built for major 1 **warns/refuses** rather
  than mis-reading.
- Historical reports under an older major are reproduced by **checking out that era's
  evaluator + sandbox** (`sandbox_version`), not by an upcasting layer — operator-side
  only, since the sandbox is not public.

## Consumer contract

A leaderboard generator / audit script implements exactly this compatibility rule:

1. Read `schema_version`; split on `.` into `(major, minor)`.
2. If `major` ≠ the major the consumer was built for → **warn and refuse** (do not
   partially parse).
3. If `major` matches → parse, **ignoring unknown keys** (a higher minor is fine).
