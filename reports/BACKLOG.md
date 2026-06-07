# Forge Novel — Consolidated Backlog

*Single source of truth for outstanding work. Started 2026-06-07. Supersedes the
scattered "Pending / Deferred / Open Items" sections in `SESSIONS.md` going forward.
When the forge MCP **tasks** tool is back, sync open items into it.*

**Status tags**

- **[GIT]** — blocked on git-forge MCP (commit / push) being back
- **[MCP]** — blocked on forge MCP (Codex / tasks / outline) being back
- **[DAVID]** — needs David's decision or approval before action
- **[READY]** — actionable now, no blocker
- **[DRAFT]** — creative drafting / editorial work
- **[VERIFY]** — re-verify against current chapter status before acting (may be stale)

---

## 1. Uncommitted work — commit when git-forge MCP is back

- [ ] **[GIT]** Commit **Ch2** — `drafts/ch02-integration-draft01.md` (interactive control-room Integration rewrite; linter-clean)
- [ ] **[GIT]** Commit **Ch3** — `drafts/ch03-first-boot-draft01.md` (em-dash repass 17.9→0.13/1k; line-edits L117 pronoun, L147 Flint refine, L149 twenty-years)
- [ ] **[GIT]** Commit **Ch4** — `drafts/ch04-safe-room-draft01.md` (full editors-hat pass 2026-06-07: typo/grammar fixes, 3 length-discipline trims, bold/case fixes, Heather age mid-forties→mid-twenties, spawn-count staging reconcile w/ Ch5, **full em-dash repass 19.67→1.35/1k** — nameplate labels + title em-dashes preserved by design. 0 FAIL; remaining WARNs all deliberate-voice keep)
- [ ] **[GIT]** Commit **new design doc** — `research/labyrinth-node-on-nates-land.md`
- [ ] **[GIT]** Commit **progression bible** — `research/progression-system-proposal.md` (LOCKED RULINGS section added this session)
- [ ] **[GIT]** Commit the other untracked research/report files surfaced at session start (`research/ch02-interactive-integration-design.md`, `reports/HANDOFF-codex-audit-next-session.md`, `reports/codex-memory-contradiction-audit.md`, `research/snippets I like.md`, this file)
- [ ] **[GIT]** Run `git status` / `git branch -a` first to confirm the full changed set; **do not push without David's say-so**

---

## 2. Needs David — decisions / approvals

- [ ] **[DAVID]** Approve editing **`magic_system.md`** (LOCKED file) — required before progression-bible propagation can touch it
- [ ] **[DAVID]** Confirm **#149 death-tax = one Level-step**
- [ ] **[DAVID]** Confirm **#94 numbering-collision** deconflict
- [ ] **[DAVID]** Settle the **Station-2 counterfeit-class name** (can resolve in drafting)
- [ ] **[DAVID]** Ch3 — 4 deliberate-voice WARN are recommended **keep** (Storyteller anaphora L103, Flint -ing run L129, Nate's terse "Then…" L199, Flint staccato L303). Closed unless you want any force-flattened.

---

## 3. Node design — open threads (creative)

- [ ] **[DRAFT]** **5b — what dungeon-mastery grants Nate** (respawn / layout / output control, a held "seat/heart"). *The next design beat — where the node's crunch attaches.*
- [ ] **[DRAFT]** **System metering of the node** — counterfeit claiming rent on clean-channel provision. Book 2+ hook; parked, not load-bearing for Book 1.
- [ ] **[DRAFT]** **Destination world** the node bridges to — flavors interior exotic palette + corridor aesthetic
- [ ] **[DRAFT]** **Node timing** in Book 1 — when it manifests, how it sequences vs. the Tutorial arc and cohort scatter

---

## 4. Canon propagation — progression bible → docs (parked, needs MCP + David's nod)

Propagate the 7 locked progression rulings (`research/progression-system-proposal.md`) outward:

- [ ] **[READY]** `research/skill-system-design.md` — single-number skill scale + named bands
- [ ] **[READY]** `characters/nate-hall.md` — leadership high-but-reluctant; experience figures
- [ ] **[MCP]** `REFERENCE.md` — PLAYER RANK (L91), Codex #109 dual-track (L88) — *but see §6: REFERENCE needs a full rebuild first*
- [ ] **[DAVID]** `magic_system.md` — LOCKED; gated on §2 approval

---

## 5. Codex sync — when forge MCP is back

- [ ] **[MCP]** Sync `research/labyrinth-node-on-nates-land.md` into the **Labyrinth / Cornerstone** Codex entries
- [ ] **[MCP]** Create the missing **Cornerstone Settlement** Codex entity (game_mechanic) from `research/cornerstone-settlement-design.md` — *real gap confirmed in handoff §2.* Remember: `tags` is a **comma-separated string**, not a list
- [ ] **[MCP]** Reconcile **#177 identity ambiguity** (named "Skill System Architecture" but #181 links it as "Labyrinth-as-pipeline")

---

## 6. REFERENCE / Codex audit (from `reports/HANDOFF-codex-audit-next-session.md`)

- [ ] **[MCP]** **Rebuild `REFERENCE.md` from the live Codex** (#1–#182 via `forge_codex_get`/`search` — never `_list`). Regenerate Quick Stats so per-category counts + total agree. Fold in working-tree edits (Judge→#135, Tutorial 2B→Ch12-15, #75 Phase 2→Ch9)
- [ ] **[MCP]** **Re-run the contradiction audit** with live Codex as authority (current `reports/codex-memory-contradiction-audit.md` is SUSPECT — judged against stale REFERENCE). Flip the workflow COMMON-block instruction that says "Codex is DOWN"
- [ ] **[MCP]** Restore **Ana Torres foil relationship** (#182 → Kyle Greene's real id; look Kyle up directly — search was flaky)
- [ ] **[READY]** Memory-side cleanups (independent of MCP): C15 retired "alpha" label; C20/C21/C31 stale "Camera"/"three-voice"/"3-4 Storyteller" refs; C41 over-retired "technique"
- [ ] **[VERIFY]** C30 Brigid omniscient style value (0.10 vs 0.15) vs `cast.json`; HUD green→blue retcon vs live Codex #11/#75

---

## 7. Drafting backlog (re-verify against current chapter status — Ch1-10 all unlocked for re-pass)

- [ ] **[VERIFY]** **Ch9–10** — await first editorial pass (per CLAUDE.md status)
- [ ] **[VERIFY]** **Ch5–8** — editorial pass under current system (HUD blue, Flint reframe, G1-G9 grafts)
- [x] **Heather/Voss class swap — DONE 2026-06-07** (David ruling, revised mid-task): instead of de-fanging Heather, **keep her prose and swap the label**. Heather Kim → **Pyromancer** (matches her Ch5-7 Fire Bolt + burned-dry Damage arc; no combat prose touched); the freed **Ward Mage** class → **Dr. Martin Voss** (floor-6 character, no combat presence yet). Synced: Ch4 L337 nameplate, `drafts/audiobook/scripts/cast.json` L113, `drafts/audiobook/VOICE-CAST.md` L25/L27, cohort memory `project_forge_tutorial_cohort.md`
- [ ] **[MCP]** **Codex sync the Heather/Voss class swap** when forge MCP is back: Heather Kim → Pyromancer, Dr. Martin Voss → Ward Mage. Also recheck `reports/codex-memory-contradiction-audit.md` (lists Heather as Ward Mage — now stale)
- [ ] **[VERIFY]** **Cohort class-vs-prose audit** (surfaced during the Heather retag): the cohort roster/cast list **Mack Turner** as Ranger/Scout but Ch6 prose has her a mace-**Warrior** (Power Strike); **Isabel Wu** as Alchemist but Ch5 prose has her a blade-**Warrior**. Reconcile label vs prose across the whole cohort
- [ ] **[VERIFY]** **Pete/Josh name collision** (Ch5↔Ch6): the "teenager who watches another fighter's milestone chime and nearly dies" is **Pete Bowman** in Ch5 L146 but **Josh Miller** in Ch6 L271/283/285. Same role, two names — pick one (Pete is the Ch4-seeded Oregon-hoodie teen)
- [ ] **[VERIFY]** Ch8 scatter-ending prose revision (older SESSIONS.md pending — confirm still needed)
- [ ] **[VERIFY]** Post-Tutorial beats: Ch11–13, Ch14+, Ch25/Ch33 (rune correction) — confirm against current outline

---

## 8. Standing / longer-term

- [ ] **[DRAFT]** **Voice exemplar bank** (`voice/exemplars.md`) — still an empty scaffold; curate gold-standard passages from locked/edited chapters (target ~12–15k words). Seed the 3 pre-nominated Ch4 passages first
- [ ] **[DRAFT]** **Ch1–4 re-narration** — audiobook locks cleared, narration flagged stale; re-narrate after the current re-pass settles
- [ ] **[READY]** When this backlog drifts, prune completed items and re-sync into forge **tasks** once that tool is reachable

---

*Maintenance: mark items done with `[x]`, add new items under the right section with a
status tag. Keep this the one place — don't restart per-session pending blocks in
`SESSIONS.md`.*
