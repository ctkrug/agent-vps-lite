# agent-vps-lite 🟢 (free)

The free core of a **safe autonomous-agent loop for a VPS** — hard spend cap + arm switch + DRY-RUN by
default, so your agent can't melt your API bill or go rogue. Drop in `observe() → decide() → act()`.

```bash
cp .env.example .env     # set caps; starts disarmed + dry-run
python3 agent.py
```

## Why a "safe loop" matters
The two things people forget when they put an LLM/agent on a server: a **hard cost cap** and a **kill
switch**. This gives you both in ~60 lines, no dependencies. Caps reset at UTC midnight; the loop never
crashes on a bad cycle; nothing executes until you flip `AGENT_ENABLED=1`.

## Upgrade → the full Agent-VPS Starter Kit ($149, lifetime updates)
The lite version is the loop + caps. The **full kit** adds the parts that make it production-grade:
- 🛡️ **`preflight.py` safety gate** — refuses to deploy if the brakes were removed (so an AI editor can't quietly delete them).
- 🚀 **systemd 24/7 deploy** + `redeploy.sh` (preflight → rsync → restart).
- 🤖 **Claude Code / Cursor rules** so your AI pair-programmer extends it without breaking the safety model.
- 🔌 **Bundled MCP server** — query your agent's status/caps from your editor.
- Recipes for trading bots, scrapers, and monitors.

**→ Get the full kit: https://buy.stripe.com/fZu4gs1qb4fW6ue03obV602**

MIT licensed. Built by [@ctkrug](https://github.com/ctkrug). ⭐ the repo if it's useful.
