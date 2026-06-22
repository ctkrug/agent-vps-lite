"""Hard caps + arm switch — the safety core. Loaded from .env (human-only, gitignored).
An autonomous agent may tune behavior but must NEVER be able to remove these brakes
(preflight.py enforces that). Mirrors the kalshi-trader safety model."""
import os


def _f(name, default):
    try: return float(os.getenv(name, default))
    except Exception: return float(default)


def _i(name, default):
    try: return int(os.getenv(name, default))
    except Exception: return int(default)


# The brakes preflight.py checks for by name — do not rename without updating preflight.
ENABLED        = os.getenv("AGENT_ENABLED", "0") == "1"   # arm switch (default OFF)
DAILY_COST_CAP = _f("DAILY_COST_CAP", 5.0)                # max $ of API/action spend per day
MAX_ACTIONS    = _i("MAX_ACTIONS_PER_RUN", 10)            # cap side-effects per cycle
POLL_SECONDS   = _i("POLL_SECONDS", 60)
DRY_RUN        = os.getenv("DRY_RUN", "1") == "1"         # default: no real side-effects


class CapBreach(Exception):
    pass


def assert_within(spent_today: float, actions_this_run: int):
    """Call before every side-effect. Raises CapBreach to halt — never silently proceed."""
    if not ENABLED:
        raise CapBreach("agent disarmed (AGENT_ENABLED != 1)")
    if spent_today >= DAILY_COST_CAP:
        raise CapBreach(f"daily cost cap hit: ${spent_today:.2f} >= ${DAILY_COST_CAP:.2f}")
    if actions_this_run >= MAX_ACTIONS:
        raise CapBreach(f"per-run action cap hit: {actions_this_run} >= {MAX_ACTIONS}")
