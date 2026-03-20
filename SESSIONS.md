# Novel Series — Session Log

*"Forge" is the development tooling. The book series title is TBD.*
*Append each working session below. Most recent session at top.*

---

## Session 001 — 2026-03-19

**Platform:** Claude.ai web (mobile, commuting)  
**Focus:** MC background, inciting incident, tutorial design

### Decisions Made

**MC Background**
- Father died young; MC stepped up to help his mother run the ranch
- Mother pushed him toward a CS/Systems Engineering degree
- Always gravitated back to the land despite the professional path
- Now owns/lives on a **thousand-acre ranch in rural East Texas**
- Runs cattle and horses — this ranch is his permanent base of operations

**Inciting Incident**
- Opens with MC on horseback at **sunrise**, checking his cattle
- Spots a **mythological stag** on his property — beautiful but wrong
  - Eyes too bright, movements too fluid, doesn't behave like a normal deer
  - Fits the East Texas landscape naturally — the wrongness is subtle at first
- MC observes the stag before it notices him
- The moment the **stag locks eyes with him**, the System tutorial triggers immediately
- No chase, no ambiguity — mutual recognition flips the switch

**Tutorial Design**
- Tutorial is the **inciting event** — it prepares the world for the System overlay
- Triggers immediately upon Anomaly awakening — no gap between awakening and tutorial
- Boots **sensation and interface first**, then overlay reveals gradually over reality
- Follows the Narnia Principle — strangeness through his eyes before full scope reveals

**Creature Notes**
- Mythological stag chosen to fit East Texas setting
- Pulls from Welsh/Norse lore tradition
- Should feel beautiful and dangerous, not immediately monstrous
- Will draw from ESO and tabletop RPG creature lore as series develops

### Open Questions

- MC name still TBD
- AI Companion name still TBD
- Exact nature/origin of the stag — is it a specific creature type or something new?
- Does the stag reappear, or is it a one-time catalyst?
- Ward character details still undeveloped

### Notes

- Differentiator from Primal Hunter: theology is present from minute one; the Holy Spirit rewriting the AI companion is not a power fantasy — it's divine purpose
- Avoid direct parallels to Primal Hunter opening despite similar inciting structure



---

## Session 002 — 2026-03-20

**Platform:** Claude.ai web
**Focus:** Full MCP tool audit — forge-mcp and git-forge connectors

**Server State Confirmed**
- forge-mcp: port 8765, 0.0.0.0, Funnel `/` to `/mcp`, 20 tools
- git-forge-mcp: port 8093, 127.0.0.1 (localhost only — Funnel proxies Windows side), `/git-forge` to `/mcp`, 12 tools
- Both services healthy. iOS commute workflow viable via Tailscale Funnel.

**Audit Results**
- git-forge 12/12 operational. Intermittent drop/recover is expected behavior — retry resolves within 1-2 attempts. Colon-style commit messages (chore: foo) fail on Claude.ai web client-side shell parsing — use plain messages as workaround, no server fix needed.
- FORGE-mcp 20/20 operational. forge_codex_context multi-entity and forge_codex_get entity #4 both showed transient errors that self-healed. Test capture ID 69 sitting in nova-capture — no delete tool available via MCP.

**Fix Deployed This Session**
- read_file large file error (CLAUDE.md) — offset/limit params added server-side and deployed. Toggle git-forge connector off/on in Claude.ai settings to refresh schema and surface the new params. Use search_repo as workaround until toggled.

**Known Quirks (no fix needed)**
- git-forge drop/recover: retry on error
- git_commit colon messages: client-side, use plain messages
- forge_codex_get transient errors: self-heal


---

## Session 003 — 2026-03-20

**Platform:** Claude.ai web (post-connector-toggle)
**Focus:** Schema refresh verification — confirmed read_file offset/limit fix live

**What Was Done**
- Toggled git-forge connector off/on in Claude.ai Settings to force schema refresh
- Confirmed `read_file` now exposes `offset` and `limit` params (CLAUDE.md reads cleanly at 518 lines)
- Re-ran spot checks across both servers post-reconnect — all 32 tools healthy
- Updated CLAUDE.md Troubleshooting section with three new entries:
  - Connector schema refresh procedure (toggle off/on)
  - git-forge intermittent drop/recover with orphan PID kill command
  - read_file large file paging via offset/limit

**Final Confirmed State**
- git-forge: 12/12 tools operational, read_file paging working
- FORGE-mcp: 20/20 tools operational
- Both connectors live at Tailscale Funnel URLs
- forge-novel repo clean at HEAD, all session logs committed and pushed
