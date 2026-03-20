# Novel Series — Session Log

*"Forge" is the development tooling. The book series title is TBD.*
*Append each working session below. Most recent session at top.*

---

## Session 004 — 2026-03-20

**Platform:** Claude.ai web
**Focus:** Full project audit + codex corrections (all four backlogged items closed)

### What Was Done

**Full State Audit (Claude.ai web)**
- Pulled complete outline via forge-mcp: 32 chapters, 128 beats, all planned — confirmed clean
- Pulled all Codex entities via forge_codex_list: 63+ entities confirmed active
- Read all git-forge repo files: CLAUDE.md, SESSIONS.md, nate-hall.md, sonja-lee.md
- Reviewed all nova-capture captures (IDs 50-69): all routed, Capture #69 (test) still orphaned (no delete tool)
- Confirmed Entity #1 and #30 East Texas corrections were already applied in a prior session

**Voice Mode Discovery**
- Confirmed: MCP connectors (forge-mcp, git-forge) are NOT available in Claude app voice mode
- Voice mode is lighter transport — no MCP. Workaround: finish voice session, switch to typed chat in same conversation, then use forge_capture before context is lost.

**Codex Corrections (completed via Claude Code)**
- forge_codex_update confirmed live on Nova (deployed but schema hadn't refreshed in prior web sessions)
- Entity #58 (Progression Display Strategy): "Ethan" → "Nate" in description + 5 nested properties fields ✅
- Entity #52 (Narnia Principle): Removed hardcoded "~7,431" Anomaly count + "Ethan" → "Nate" ✅

### Final Codex Correction Scorecard

| Entity | Issue | Status |
|--------|-------|--------|
| #1 Nate Hall | "lives in RV" → East Texas | ✅ Done (prior session) |
| #30 Earth Post-Integration | RV/Bellevue reference | ✅ Done (prior session) |
| #58 Progression Display Strategy | "Ethan" × 8 across description + properties | ✅ Done (Session 004) |
| #52 Narnia Principle | "~7,431" hardcoded count + "Ethan" | ✅ Done (Session 004) |

### Known Orphans / Open Items

- Capture #69: Test capture — no MCP delete tool, not blocking anything
- AI companion name: Still TBD
- `characters/ai-companion.md`: File doesn't exist yet — create when name is decided
- Observation Point name: Still TBD (God's Eye / Mercy Seat / Vantage / Threshold all rejected)
- Sonja pre-Integration life: Undeveloped (profession, location, survival before Nate)
- Stag origin: Specific Welsh/Norse creature or something new? Reappears or one-time?

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
