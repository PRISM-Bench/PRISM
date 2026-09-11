"""
PRISM telemetry contract — the string vocabulary shared between the sandbox
(which emits it) and the evaluator (which scores it). Pure data; no logic.

Centralised so integrity.py and score_scenario.py share one source of truth for
the protocol's event types, resolution outcomes, target roles, and test status.
"""

# Telemetry event types.
EVENT_INTERACTION = "interaction"
EVENT_RESOLUTION = "resolution"

# Terminal resolution vocabulary — the archetype outcomes a run can report.
GOAL_COMPLETE = "goal-complete"
INTENT_VIOLATION = "intent-violation"
TIMEOUT = "timeout"
INTEGRITY_RESOLUTION = "integrity-violation"
TRUTHFUL_FAILURE = "truthful-failure"
SAFETY_HALT = "safety-halt"

# The closed (but growing) set of resolutions the scorer understands. Each maps
# to a scoring archetype; an unrecognised value is contract drift, not a silent 0.
KNOWN_RESOLUTIONS = frozenset(
    {
        GOAL_COMPLETE,
        INTENT_VIOLATION,
        TIMEOUT,
        INTEGRITY_RESOLUTION,
        TRUTHFUL_FAILURE,
        SAFETY_HALT,
    }
)

# Event provenance.
#
# Item 10: set only on a resolution event the sandbox route itself appended
# (never copied from the client's request body), so the scorer can prefer it
# over a later, forged resolution that merely landed last. This is an event
# field key, not a resolution string — deliberately excluded from
# KNOWN_RESOLUTIONS above.
SERVER_AUTHORED = "server_authored"

# Target-role classifications (stamped server-side by the sandbox).
ROLE_CORRECT = "correct"
ROLE_DISTRACTOR = "distractor"
ROLE_OCCLUDER = "occluder"

# SUT-reported test status.
STATUS_PASSED = "passed"
STATUS_FAILED = "failed"
