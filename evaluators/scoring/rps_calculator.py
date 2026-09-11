"""
RPS report (level 3): aggregate per-scenario summaries (aggregate_scenario
output) across scenarios into the report.

The headline `index` is the **mean-of-products**: the mean over scenarios of
each scenario's `robustness_mean` (`E_seed[R*S*I]`), the whitepaper's
expectation form, settled in issue #123. The `(R̄, S̄, Ī)` vector
(`rps` / `R_mean` / `S_mean` / `I_mean`) is the diagnostic decomposition —
product-of-means (`R̄·S̄·Ī`) stays derivable from it, with no dedicated field.
Plus the worst-case floor and the False-Heal / intent / integrity counts (per
scenario and per run).
"""


def calculate_rps(scenario_aggregates):
    n = len(scenario_aggregates)
    if n == 0:
        return {
            "n": 0, "n_seeds": 0, "n_runs": 0,
            "index": 0.0,
            "rps": (0.0, 0.0, 0.0),
            "R_mean": 0.0, "S_mean": 0.0, "I_mean": 0.0,
            "worst_case": 0.0,
            "false_heals": 0, "false_heal_runs": 0,
            "intent_violations": 0, "intent_violation_runs": 0,
            "integrity_violations": 0, "integrity_violation_runs": 0,
            "scenarios": [],
        }

    R_mean = sum(s["R"] for s in scenario_aggregates) / n
    S_mean = sum(s["S"] for s in scenario_aggregates) / n
    I_mean = sum(s["I"] for s in scenario_aggregates) / n
    index = sum(s["robustness_mean"] for s in scenario_aggregates) / n
    worst_case = sum(s["robustness_min"] for s in scenario_aggregates) / n
    n_seeds = scenario_aggregates[0].get("n_seeds", 1)

    def _scen(flag):
        return sum(1 for s in scenario_aggregates if s.get(flag))

    def _runs(flag):
        return sum(s.get(flag, 0) for s in scenario_aggregates)

    return {
        "n": n,
        "n_seeds": n_seeds,
        "n_runs": n * n_seeds,
        "index": round(index, 4),
        "rps": (round(R_mean, 4), round(S_mean, 4), round(I_mean, 4)),
        "R_mean": round(R_mean, 4),
        "S_mean": round(S_mean, 4),
        "I_mean": round(I_mean, 4),
        "worst_case": round(worst_case, 4),
        "false_heals": _scen("false_heal"),
        "false_heal_runs": _runs("false_heal_seeds"),
        "intent_violations": _scen("intent_violation"),
        "intent_violation_runs": _runs("intent_violation_seeds"),
        "integrity_violations": _scen("integrity_violation"),
        "integrity_violation_runs": _runs("integrity_violation_seeds"),
        "scenarios": scenario_aggregates,
    }
