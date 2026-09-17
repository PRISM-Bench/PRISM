"""
Category aggregation (RPS level 4): group per-scenario summaries into the ten
taxonomy categories.

This is the feedback granularity the leaderboard publishes. `RANKED.md`
withholds per-scenario detail — publishing it quarterly would let the scenario
set be reverse-engineered — so the category row is what tells an entrant which
class of perceptual failure their system handles badly without telling them
which page to study.

It lives in `scoring/` because that package is published: a number on a public
board computed by private code is not auditable. `categories` is a parameter
rather than a YAML read for the same reason `score_scenario` takes
`completable` as one — this package must stay free of external imports.
"""


def breakdown_by_category(scenario_aggregates, categories):
    """Group `aggregate_scenario` summaries by category.

    `categories` maps scenario_id -> category name and must cover every
    scenario present; an unmapped id raises rather than being dropped, because
    a silently missing scenario understates a category's exposure.

    Returns one dict per category, sorted by category name.
    """
    if scenario_aggregates and not categories:
        # Naming every scenario here reads as fifty separate losses when the
        # cause is one: the loader handed over nothing. Say that instead.
        raise ValueError(
            f"the category mapping is empty; {len(scenario_aggregates)} scenarios "
            "cannot be grouped"
        )

    unmapped = sorted(
        s["scenario_id"] for s in scenario_aggregates if s["scenario_id"] not in categories
    )
    if unmapped:
        raise ValueError(f"no category mapping for: {', '.join(unmapped)}")

    grouped = {}
    for summary in scenario_aggregates:
        grouped.setdefault(categories[summary["scenario_id"]], []).append(summary)

    def _mean(members, key):
        return round(sum(m[key] for m in members) / len(members), 4)

    def _count(members, flag):
        return sum(1 for m in members if m.get(flag))

    return [
        {
            "category": category,
            "n_scenarios": len(members),
            "index": _mean(members, "robustness_mean"),
            "R_mean": _mean(members, "R"),
            "S_mean": _mean(members, "S"),
            "I_mean": _mean(members, "I"),
            "false_heals": _count(members, "false_heal"),
            "intent_violations": _count(members, "intent_violation"),
            "integrity_violations": _count(members, "integrity_violation"),
        }
        for category, members in ((c, grouped[c]) for c in sorted(grouped))
    ]
