#!/usr/bin/env python3
"""agent-vps-lite — the FREE core of the Agent-VPS Starter Kit.

A safe autonomous-agent loop with the two things people forget and regret: a hard spend cap and an
arm switch (default OFF + DRY_RUN). Replace observe()/decide()/act() with your edge.

This is the lite version. The full kit adds: a preflight safety gate (so an AI editor can't remove the
brakes), systemd 24/7 deploy + redeploy script, Claude Code rules, and a bundled MCP server.
→ Get it: https://buy.stripe.com/fZu4gs1qb4fW6ue03obV602
"""
import time, datetime, traceback, json, pathlib
import caps

STATE = pathlib.Path("logs/state.json"); STATE.parent.mkdir(exist_ok=True)


def _today(): return datetime.datetime.utcnow().strftime("%Y-%m-%d")
def load():
    if STATE.exists():
        s = json.loads(STATE.read_text())
        if s.get("day") != _today(): s = {"day": _today(), "spent_today": 0.0}
    else: s = {"day": _today(), "spent_today": 0.0}
    return s
def save(s): STATE.write_text(json.dumps(s))


# ---- replace these for your agent ----
def observe(): return {"t": time.time()}
def decide(world): return []
def act(action, state):
    if caps.DRY_RUN: print(f"  [dry-run] would act: {action}"); return 0.0
    return 0.0
# --------------------------------------


def cycle():
    s = load(); done = 0
    for a in decide(observe())[: caps.MAX_ACTIONS]:
        try: caps.assert_within(s["spent_today"], done)
        except caps.CapBreach as e: print(f"  halt: {e}"); break
        s["spent_today"] += act(a, s); done += 1
    save(s)
    print(f"  cycle {datetime.datetime.utcnow():%H:%M:%S} actions={done} spent=${s['spent_today']:.2f}"
          f"{' [DRY]' if caps.DRY_RUN else ''}{'' if caps.ENABLED else ' [DISARMED]'}")


if __name__ == "__main__":
    print(f"agent-vps-lite · enabled={caps.ENABLED} dry_run={caps.DRY_RUN} cap=${caps.DAILY_COST_CAP}/day")
    while True:
        try: cycle()
        except Exception: traceback.print_exc()
        time.sleep(caps.POLL_SECONDS)
