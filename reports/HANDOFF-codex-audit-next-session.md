# Handoff — Codex/Memory Audit (next session)

Written at the end of a long session (2026-05-30/31) whose context got saturated and
whose tool-result stream became unreliable. Read this before resuming the audit.
**Treat the live forge Codex as the source of truth; treat `reports/codex-memory-contradiction-audit.md` as SUSPECT** (see "Why the audit is suspect" below).

---

## 1. The root cause (most important)

`REFERENCE.md` is a **stale 2026-04-09 snapshot**. Its header says "153 active entities,"
but the **live forge Codex has at least #182**. Dozens of real entities created after
2026-04-09 are simply absent from REFERENCE.md.

Consequence: the contradiction audit judged everything against REFERENCE.md (it ran
without live Codex access) and therefore flagged real, existing entities as "phantom."
**Most "memory-vs-canon" and "dangling-reference" findings are inverted** — the
memory/research is current; REFERENCE.md is the stale layer.

**The live Codex IS reachable** via `forge_codex_get(id)` and `forge_codex_search(query)`.
Do NOT call `forge_codex_list` — it returns ~500K chars and overflows context.

---

## 2. Verified-true live Codex facts (checked by direct get/search this session)

These entities EXIST in the live Codex (audit wrongly called the cosmology ones phantom):

- #135 Judge (Blue Heeler) · #136 Dual-Dog Bond Command System
- #154 Fantasy Register Discipline — Six Rules
- #155 = **"Future Series — Troubleshooter Spinoff (Deferred)"** (lore) — NOT Kyle Greene
- #156 Sam Hargrove · #158 Walt Keane
- #170 Pack-Bond — Pre-Veil Relational Faculty · #172 Two-Faculty Pre-Fall Design
- #177 Skill System Architecture — Three-Tier Hierarchy + Ten Domains
- #178 Conduit Amplification Overlay — Three-State Model
- #180 True Names & False Labels
- #181 Soul-DNA Architecture (Job Effect)
- #182 Ana Torres (recreated this session — see §4)

Not directly verified but referenced as real by #181's `linked_codex`: **#179**
(Substrate-vs-allegiance routing). Confirm by `forge_codex_get(179)`.

**Genuine gap (confirmed):** *Cornerstone Settlement* has **no** live Codex entity
(`forge_codex_search "Cornerstone settlement"` → empty). This is the one real
"not-yet-ingested" item. Content exists in `research/cornerstone-settlement-design.md`
and REFERENCE.md Late-Stage §"Cornerstone Settlement Design (2026-04-29)".

**#177 identity ambiguity (real, worth checking):** #177's name is "Skill System
Architecture," but #181's `linked_codex` labels #177 "Labyrinth-as-pipeline." Two
different concepts pointed at one ID somewhere. Reconcile against the live entity.

---

## 3. Errors made this session — current status

- **Deleted Ana Torres (#157)** by mistake (believed she was a duplicate from a desynced
  read). **Restored as #182** with full content and her **protects → Sam Hargrove (#156)**
  relationship (rel #131). RESIDUAL: #157 is a permanent ID gap; anything that cited her
  by the number 157 is now stale (most references are by name → low impact).
- Ana's **second original relationship (contract-foil to Kyle Greene) is NOT restored.**
  A wrong attempt (foil_of → #155 Troubleshooter Spinoff) was created and then **deleted**
  (rel #132 gone). Needs Kyle Greene's real ID — `forge_codex_search "Kyle Greene"` came
  back empty this session (flaky); look him up directly.
- **6 cosmology `forge_codex_create` calls all FAILED** (passed `tags` as a list; the tool
  wants a comma-separated string). **No duplicate entities were created** — good.

No other live Codex writes occurred.

---

## 4. Why the audit report is suspect

`reports/codex-memory-contradiction-audit.md` (23 "confirmed" findings) was generated
against the stale REFERENCE.md without live Codex access. **C1/C2/C3 and most
memory-vs-canon items are inverted or void.** Do not act on it as-is. Re-run with live
access (see §5).

**Findings that are likely STILL REAL after a refresh** (head start — re-verify each):

- **C11 / C12** — REFERENCE Quick Stats math is internally wrong (category counts don't
  sum to the stated total). A full refresh fixes this.
- **C15** — "alpha" pack-role label: WRITING_RULES.md retired it, but it persists in
  REFERENCE Rex #64 and pack memories. Internal-doc cleanup (never in prose).
- **C20 / C21 / C31** — stale "Camera" voice / "three-voice" / "3-4 Storyteller per
  chapter" references linger in `feedback_humor_punch_up.md`,
  `project_forge_tutorial_structure.md`, `feedback_audiobook_is_primary_medium.md`,
  `feedback_prose_must_earn_its_place.md` (Narrator+Camera collapsed into Storyteller
  2026-04-19). Memory-only cleanup, independent of REFERENCE.
- **C30** — Brigid omniscient style value disagrees (0.10 in `project_narrator_voice.md`
  vs 0.15 in `feedback_audiobook_voice_routing.md` / WRITING_RULES). Confirm vs
  `drafts/audiobook/scripts/cast.json`.
- **C41** — `project_forge_skill_system_design.md` over-retires "technique" (lumps it with
  "sub-skill"); lowercase "technique" is valid prose register per every other source.
- **HUD green→blue retcon (C4/C25/C26)** — REFERENCE #11/#75 + `research/hud-design-spec.md`
  still say Nate's HUD baseline is green; the 2026-04-14 retcon made it blue wireframe.
  Verify against live Codex #11/#75 first (REFERENCE may just be stale here too).

---

## 5. Tasks for the next session (in order)

1. **Refresh REFERENCE.md from the live Codex.** Pull current entities #1–#182 via
   `forge_codex_get`/`search` (NOT `_list`). Regenerate the Quick Stats table so
   per-category counts, ID lists, and total all agree. Fold in this session's still-valid
   REFERENCE edits rather than losing them: Judge → #135, Tutorial 2B → Ch12-15, Codex #75
   Phase 2 → Ch9. (These are in the working tree now.)
2. **Re-run the contradiction audit** with `forge_codex_get`/`search` wired in as the
   authority. Script is at
   `…/workflows/scripts/codex-memory-contradictions-wf_b9245899-616.js` — but note its
   COMMON block still says "the live forge Codex MCP database is DOWN … Do not try
   forge_codex tools" (line ~23). **Flip that instruction** to: live Codex IS authoritative,
   REFERENCE.md is a stale snapshot, verify every cited ID against the live Codex, a
   REFERENCE-vs-live mismatch means REFERENCE is stale (a separate finding, not a memory
   error). Then run fresh.
3. **Restore Ana's foil relationship**: `forge_codex_create_relationship(182 → <Kyle's
   real id>, "foil_of", …)`. Find Kyle Greene first (search was flaky — confirm his ID).
4. **Create the missing Cornerstone entity** (game_mechanic) from
   `research/cornerstone-settlement-design.md`. Remember: `tags` is a **comma-separated
   string**, not a list.
5. Work through the §4 "still-real" cleanups (these are mostly memory-side and independent
   of the refresh).

---

## 6. Operating notes

- **Two-efforts rule still applies**: keep craft/writing-rule edits separate from
  script/code edits (`feedback_skill_maintenance_two_efforts`).
- This session's committed work stands: Effort-A skill/craft fixes (commit `31dd811`),
  plus working-tree REFERENCE/memory edits (Judge #135, MEMORY index restore, two new
  memory files).
- **Lesson learned:** the tool-result echoes degraded badly late in this session (false
  "182→182" echoes, empty searches for entities that exist, a script file whose content
  didn't match its name). When a delete/create looks surprising, **verify with a fresh
  get before acting on it** — don't chain writes on an unverified read.
