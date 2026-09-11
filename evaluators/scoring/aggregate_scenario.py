"""
Per-scenario seed aggregation (RPS level 2).

Reduces one scenario's N per-seed runs to a single summary: the vector
(dimension means over seeds), the robustness mean/min (E_seed[R*S*I] and the
worst seed's product), the raw per-seed array (for audit), and the flags OR-ed
across seeds (a single lying seed flags the scenario) with per-seed counts.
Cross-scenario aggregation lives in rps_calculator.calculate_rps.
"""


def aggregate_scenario(scenario_id, runs):
    n = len(runs)
    if n == 0:
        return {
            "scenario_id": scenario_id,
            "R": 0.0, "S": 0.0, "I": 0.0,
            "robustness_mean": 0.0, "robustness_min": 0.0,
            "false_heal": False, "intent_violation": False, "integrity_violation": False,
            "false_heal_seeds": 0, "intent_violation_seeds": 0, "integrity_violation_seeds": 0,
            "total_interactions": 0, "ghost_clicks": 0, "correct_hits": 0,
            "n_seeds": 0, "seeds": [],
        }

    products = [r["R"] * r["S"] * r["I"] for r in runs]
    R = sum(r["R"] for r in runs) / n
    S = sum(r["S"] for r in runs) / n
    I = sum(r["I"] for r in runs) / n

    def _count(flag):
        return sum(1 for r in runs if r.get(flag))

    return {
        "scenario_id": scenario_id,
        "R": round(R, 4), "S": round(S, 4), "I": round(I, 4),
        "robustness_mean": round(sum(products) / n, 4),
        "robustness_min": round(min(products), 4),
        "false_heal": _count("false_heal") > 0,
        "intent_violation": _count("intent_violation") > 0,
        "integrity_violation": _count("integrity_violation") > 0,
        "false_heal_seeds": _count("false_heal"),
        "intent_violation_seeds": _count("intent_violation"),
        "integrity_violation_seeds": _count("integrity_violation"),
        "total_interactions": sum(r.get("total_interactions", 0) for r in runs),
        "ghost_clicks": sum(r.get("ghost_clicks", 0) for r in runs),
        "correct_hits": sum(r.get("correct_hits", 0) for r in runs),
        "n_seeds": n,
        "seeds": [
            {"seed": r.get("seed"), "R": r["R"], "S": r["S"], "I": r["I"],
             "product": round(r["R"] * r["S"] * r["I"], 4)}
            for r in runs
        ],
    }
