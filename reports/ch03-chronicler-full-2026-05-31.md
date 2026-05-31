# Ch03 — Chronicler → Codex Proposal Report (G2 FULL, 6 lenses)

> Generated 2026-05-31 by `chronicler-codex` (relationships + timeline increment):
> **6 agents** (entity + relationship + timeline + progression extractors →
> validate/dedup → synthesis), ~366K subagent tokens, ~9 min. **Proposals only —
> nothing was written to canon, the Codex, or any state file.** Dedup ran against
> `REFERENCE.md` (the 2026-04-09 prose Codex rebuild), so create-vs-update and
> add-vs-confirm should be sanity-checked against the live forge Codex before
> applying. This **supersedes** the MVP snapshot (`ch03-chronicler-2026-05-31.md`)
> for editorial action. Counts: 1 create · 4 update · 3 uncertain · 1 relationship
> add (+11 confirm) · 14 timeline events · 11 progression events · 6 drift flags
> (0 critical, 2 major).

## Proposed Codex changes

**Updates (extend existing locked entities — on-page payoff, no new canon):**

| Action | Type | Name | Codex# | Proposed entry / delta | Evidence |
|---|---|---|---|---|---|
| update | character | F.L.I.N.T. | #2 | Ch03 first-boot detail: wakes mid-diagnostic cataloguing corrupted state (directives scrambled, protocols rewritten in a language he can't read); outbound reporting "not disabled — gone... pulled out by the roots"; matrix flagged "unauthorized, origin unknown, non-standard"; one-way System access ("a radio that only receives"); two-way link operational from first contact ("the line ran both ways"); self-IDs as MSG companion, reads designation from build manifest, shortened to "Flint"; loyalty "points at you instead of where they're supposed to point"; detects unclassifiable subsystem "significantly larger... older... completely indifferent to my opinion" past his read access. Bob-the-Skull register confirmed. | l.63,69,71-79,89,101-107,121-129,181,197 |
| update | lore | Flint Name Reveal — Chapter 3 | #70 | Mark EXECUTED: Flint reads "Field Logic Interface, Network Tethered" from build manifest, Nate shortens to "Flint," Flint registers dry resistance. Locked reveal lands in scheduled chapter — no drift. | l.99-114 |
| update | ability | Structural Analysis (Rank 1, Low) | #98 / #109 | SA is Nate's SOLE pre-loaded skill, "Rank 1, Low tier." Verbatim desc: "Reveals material type, quality grade, and durability of targeted objects. Passive scan, focus-activated." First use on truck hood: low-carbon steel / Common / 72%. Rank-1 floor is the baseline the Bezalel amplification (#92/#87) later grows from. | l.135,151,163 |
| update | mechanic | HUD Interface System — Phase 1 (blue arcs) | #11 / #75 | DRIFT-RESOLUTION: Ch03 renders Phase 1 as TWO BLUE arcs (Health ~90%, Stamina ~80%), no numbers/labels, consistent with ch02. #11/#75 say "monochrome GREEN." Prose (ch02→ch03) internally consistent on BLUE; **REFERENCE's own "Magic Visibility & Color Split" section also says "blue wireframe," so the Codex is internally inconsistent.** Recommend David ratify BLUE and update #11/#75. Also lock: arcs "flare white" at transport (l.405). | l.121-123,129,205,335,405; xref ch02 l.235,283,327 |

**Creates (new canon):**

| Action | Type | Name | Codex# | Proposed entry / delta | Evidence |
|---|---|---|---|---|---|
| create | character | Congressman (steer) | — | Named bovine on Hall Ranch (sex/breed unspecified). Grazes south pasture through the Integration morning — "monument to bovine indifference." Among ~63 head NOT transported; left untended at chapter's end. **No named ranch livestock in REFERENCE.md; genuinely new there** — but note the MVP run read this as an already-established Ch01 detail. David's call: Codex entry vs worldbook note. | l.305-306,379,411 |

**Uncertain (confirm: new or existing? — David decides the entity threshold):**

| Action | Type | Name | Codex# | Proposed entry / delta | Evidence |
|---|---|---|---|---|---|
| uncertain | mechanic | Apprentice Pyromancer (starter class) | — | System starter class via Flint's network chatter (Henderson teen); recreational fireballs. Maps to skill-system Domain 2 (Martial—Magic / Pyromancy). REFERENCE enumerates only principal-cast classes (#98/#99/#103) — David to decide whether incidental NPC classes are catalogued. | l.235-239,293,351 |
| uncertain | character | Henderson teenager | — | Unnamed ~14yo, ¼ mi east. Got Apprentice Pyromancer; lobs fireballs ignoring his mother; his 6yo sister is extracted (children-first), he is left "spinning in the yard," tagged alive. Lean: worldbook "Henderson family" neighbor note unless he recurs. | l.235-243,293,351-357 |
| uncertain | item | Nate's 1998 Ford F-250 | — | Steel frame "built up twice." First SA target in the series; staging ground for the first Nate-Flint talk; left idling, door open, at transport. Lean: worldbook prop note tied to #29 (Pre-System Competencies) over a full Item entry. | l.145-146,151,159,219,411 |

---

## Proposed relationships

"confirm" rows are already-canon edges merely exercised on-page — **David can skip these.** Only the **add** row needs a write.

| Action | From | Type | To | Description | Evidence |
|---|---|---|---|---|---|
| **add** | Nate | ownership → | Congressman | Named steer/bull on the ranch; among cattle left untended at transport. **(Contingent on the Congressman entity being accepted; drop if demoted to worldbook note.)** | l.305-306,379,411 |
| confirm | Nate | pack-bond ↔ | Rex | Bond exercised: Rex reads Nate's "Enough," moves unprompted, at T-30 plants shoulder-to-shin sending "With you" heat. Transported with Nate. (#64/#72/#88) | l.17-19,59,65,371-372,395 |
| confirm | Nate | pack-bond ↔ | Judge | Holds perimeter as distinct role; at ~T-10 plants at Nate's right leg without command. Transported. (#135/#88) | l.21,67-68,207,397-398 |
| confirm | Rex | pack-co-membership ↔ | Judge | Coordinated unit bracketing Nate — Rex ground/contact, Judge perimeter; "same formation they'd hold on a herd." (#64/#135/#88) | l.17-21,207-209,395-399 |
| confirm | F.L.I.N.T. | companion-bond ↔ | Nate | Flint wakes installed, loyalty repointed, two-way link from first contact; they build "the scaffolding" of a partnership. (#2) | l.47-51,71-79,121-129,181,313-317 |
| confirm | F.L.I.N.T. | origin-severed → | Morningstar Group | MSG companion by manifest, but outbound reporting "pulled out by the roots," matrix "unauthorized"; delivers the pitch with contempt. Origin = MSG; allegiance = severed. (#2 + MSG brand) | l.63,89,101,129,181 |
| confirm | F.L.I.N.T. | one-way-access → | The System | Receives fragmentary System traffic, cannot transmit — "a radio that only receives." (#2/#56) | l.61-63,69,181,367 |
| confirm | The Creator | indwelling-presence → | Nate | "Something already there" pre-dating the System, pulsing warmth through Nate's chest. Anomaly on-page; never named (Narnia Principle). (#5/#6/#94) | l.49,187-199,401 |
| confirm | The Creator | author-rewrote → | F.L.I.N.T. | Unnamed presence implied as the rewriter ("This wasn't a glitch. This was a remodel"). Flint sees only "the edges," no self-diagnosis of divine source. (#2 + flint-divine-rewrite) | l.93-94,181,197-198 |
| confirm | Nate | unclassified-by → | The System | Class reads [PROCESSING] — System "either hasn't classified you or tried and choked." (#6/#11/#95/#32) | l.29,121-122,129 |
| confirm | Nate | ownership-and-lineage → | Hall Ranch | Works the Hall family ranch — "a thousand acres... three generations." (#1/#69; see lineage flag below) | l.203,379 |
| confirm | Nate | has-skill → | Structural Analysis | SA (Rank 1, Low) is Nate's sole pre-loaded skill, tested on the truck frame. (#98/#109) | l.135-136,151-155,163 |

---

## Timeline events

| When | Scope | Event | Consequence | Evidence |
|---|---|---|---|---|
| Ch03 opening (first minutes post-freeze, from ch02) | personal | Nate regains consciousness in the pasture | Anchors chapter immediately after ch02; stripped HUD (blue arcs) persisted | l.11-29 |
| Simultaneous with Nate waking | local | Neighbors receive full System install — character-creation "celebration" | Populace got standard installs; Nate is the outlier (#6 Anomaly) | l.25-27 |
| Shortly after Nate sits up | personal | Flint first boot — non-standard companion activates | Satisfies #70 (Flint names self Ch3); plants flint-divine-rewrite + flint-quantum-substrate; two-way link | l.35-114,181 |
| Moments later, running board | personal | Two-way link discovered — Nate's "Enough" thought | Confirms bidirectional comms (#2) | l.71-79 |
| On the running board | personal | HUD diagnostic — minimal display + [PROCESSING] class | Locks anomalous HUD as Book-1 fixture; COLOR FLAG (blue prose vs green Codex) | l.121-129 |
| Immediately after | personal | Structural Analysis first activation — truck scan | Canonizes SA as sole starting ability; 72% durability data point | l.135-163 |
| Extended running-board talk | personal | Flint detects the unclassifiable subsystem (Spirit-presence) | First on-page detection of Anomaly subsystem (#6) | l.187-199 |
| Mid-morning, ~1hr post-Integration | local | Fence-line patrol — regional chaos inventory | Regional chaos signature; Hall-ranch infrastructure intact; helicopter = institutional response | l.229-233 |
| Mid-morning, during patrol | local | Henderson teen manifests Apprentice Pyromancer | First named System class besides [PROCESSING]; teens get full installs | l.235-243,293 |
| Mid-morning, overlook | global | Radio scan — global institutional chaos confirmed | Anchors GLOBAL scope (China dark 40+min, EU suspended, President pending); REVEAL-TIMING FLAG (front-runs ch04) | l.265-285 |
| Mid-morning, after radio | regional | Flint network assessment — East Texas calmer; first mishaps | Hall ranch viable base; Mage-sneeze + ditch incidents first named county mishaps | l.289-297 |
| Mid-to-late morning; T-60 | global | Tutorial broadcast — planet-wide announcement + countdown | Locks synchronous global Tutorial trigger, 60s window; bone-conduction delivery | l.329-338 |
| During the 60-count (~T-45 to T-38) | local | Children taken first — Henderson girl (age 6) extracted | First on-page demo of #83 + pre-puberty rule; forced, instantaneous | l.351-363 |
| Ch03 close; T-0; arcs flare white | personal | Tutorial transport — Nate, Rex, Judge taken at zero | Locks Rex AND Judge as confirmed Tutorial companions (#88); empty-pasture close bookends opening; hands to ch04 | l.393-413 |

*Continuity note:* Events are in clean story order and hand off directly to ch04 (Safe Room), continuous with ch02's close (blue arcs under closed eyes, l.363-369), no gap. The only ordering concern is the **global-scope radio hints front-running the scheduled ch04 reader-learn** (see drift flags) — advancing, not blowing, the reveal.

---

## Progression ledger delta

| Character | Kind | Name | Change | Detail | Evidence |
|---|---|---|---|---|---|
| Nate | stat | Health | revealed | Longer blue arc; no number. Flint reads ~90% ("still recalibrating"). Atmosphere, not audit-grade. | l.121-123,129 |
| Nate | stat | Stamina | revealed | Shorter blue arc; no number. Flint reads "maybe eighty percent." | l.121-123,129 |
| Nate | class | [PROCESSING] | revealed | Class field reads "[PROCESSING]" (italic System-error register, #32). Nate does NOT yet know it's Engineer (correct per epistemic). | l.129 |
| Nate | skill | Structural Analysis | gained | Rank 1, Low. Sole pre-loaded skill. Three data points per read. Consistent with #109. | l.135 |
| Nate | ability | Structural Analysis — focus-activated scan | used | First use on F-250 hood: low-carbon steel, Common, 72%. No combat use yet (ch04). | l.146-155 |
| Nate | interface | HUD configuration (Phase 1) | revealed | Two blue arcs only; no numbers/labels/sheet/class/tree/inventory/map/quest log/compass. Arcs "flare white" at transport. Prose color = BLUE (drift flagged). | l.29,121-129,405 |
| Nate | companion | Companion bond — Flint | gained | Outbound reporting "gone," matrix "unauthorized," loyalty repointed to Nate, two-way link, receive-only System access. Matches #2. | l.53-114,79,89,181 |
| Nate | event | Tutorial commencement / transport | reached | Global "TUTORIAL PHASE — COMMENCING" + 60-count; at 0 arcs flare white, Nate + Rex + Judge extracted. Hands to ch04. | l.333-408 |
| Rex | companion | Pack-bond — Tutorial transport | confirmed | Transported with Nate (#88). Pre-transport bidirectional bond; at T-30 sets shoulder-to-shin, "With you" through contact. Present at left leg at 0. | l.59,371-372,395,405 |
| Judge | companion | Pack-bond — Tutorial transport | confirmed | Transported with Nate (#88). At ~T-10 plants at right leg, "perfectly still for the first time all morning," no command. | l.396-399,405 |
| Flint | self-diagnostic | Companion classification — non-standard | revealed | Designation F.L.I.N.T.; outbound gone; matrix unauthorized; receive-only; loyalty repointed; read-access "between limited and actively insulted." Does NOT self-diagnose the divine rewrite (only "the edges"). | l.89,101,129,181-182,197 |

---

## Drift & continuity flags

Leading with major severity.

| Kind | Severity | Issue | Location |
|---|---|---|---|
| continuity | **MAJOR** | HUD COLOR — Codex likely lagging, not the prose. Ch03 renders Phase-1 HUD BLUE throughout; #11/#75 say monochrome GREEN. Ch02 already locked BLUE (l.235/283/327), so prose is internally consistent ch02→ch03. **REFERENCE's own "Magic Visibility & Color Split" section ALSO says "Nate's HUD is blue wireframe" — so the Codex is internally inconsistent; prose sides with the newer blue decision.** Ratify BLUE and update #11/#75; do NOT auto-change prose. | ch03 l.13,29,121-123,205,335,405 vs REFERENCE #11/#75 (and the agreeing color-split section) |
| epistemic | **MAJOR** | epistemic-states.json STALE on Flint's loyalty, not the chapter. after_ch03 lists Nate falsely_believes "Flint is fully loyal... (Flint serves the System first)" and doesnt_know "Flint has network access." BOTH obsolete: revelation-schedule flint-divine-rewrite retired the dual-loyalty framing; ch03 shows loyalty repointed (l.181) and Flint openly reading HUD + hearing System chatter. Update epistemic-states.json (drop the dual-loyalty line; move "network access" to knows). No prose change. | epistemic-states.json nate.after_ch03 vs ch03 l.69,121-129,181,235 |
| reveal | minor | Integration global-scope hints arrive one chapter early. revelation-schedule integration-global-scope = reader_learns 4 / full_reveal 9; ch03's radio scan delivers concrete global signals. These are HINTS, not the full interlude, and strengthen the global-Tutorial beat. Keep (ch03 earns it) or trim the China/EU/President specifics for ch04. Low risk. | ch03 l.265-285,323 vs revelation-schedule |
| continuity | minor | Lineage note (not a contradiction). Ch03 l.203 "three generations... his father's land before that, his mother's after"; REFERENCE #1 "Louisiana origin, settled East Texas." Coexist, but if #1's "Louisiana origin" implies Nate himself relocated, the "three generations on THIS land" framing wants a quick reconcile. Flag only; #69 is canonical home. | ch03 l.203 vs REFERENCE #1/#69 |
| mechanical | info | No mechanical drift. SA Rank 1 Low matches #109; mundane-only use, no overflow/Bezalel (correctly deferred). Apprentice Pyromancer / Mage valid low-rank Domain-2. Clean. | ch03 l.135 vs skill-system-design + #109 |
| continuity | info | Cattle count specificity. "Sixty-three animals" (l.331). Per feedback_prose_numbers_are_atmosphere, do NOT start a running cattle tally; logged so a future chapter isn't held to "63 head." | ch03 l.331 |

---

## How to apply

These are **proposals only — nothing was written to canon, the Codex, or any state file.** The `forge_codex` create/update calls are pre-staged in the run transcript's `proposed_codex_calls`, and the one relationship write in `proposed_relationship_edges` (run when the forge MCP tools are session-live). The progression delta is in Appendix A (merge into `progression-state.json`) and the timeline delta in Appendix B (merge into `timeline-state.json`); both files are created on first confirmed run. Because REFERENCE.md dedup can lag the live Codex, **sanity-check create-vs-update and add-vs-confirm against the live Codex before applying** — in particular: the three "uncertain" rows need David's entity-threshold call; the Congressman create + its ownership edge are paired (drop both if demoted); and the two **MAJOR** flags (HUD color, stale epistemic-states) are **state-file fixes to ratify before the next chapter**, not prose changes.

---

## Appendix A — `progression-state.json` delta (merge target)

```json
{"book":1,"characters":{"Nate":{"by_chapter":{"ch03":[{"kind":"stat","name":"Health","change":"revealed","detail":"Longer of two blue arcs; no on-screen number. Flint reads ~90% ('still recalibrating'). Atmosphere, not audit-grade.","evidence":"l.121-123,129"},{"kind":"stat","name":"Stamina","change":"revealed","detail":"Shorter blue arc; no number. Flint reads 'maybe eighty percent.'","evidence":"l.121-123,129"},{"kind":"class","name":"[PROCESSING]","change":"revealed","detail":"Class field reads '[PROCESSING]' (italic System-error register, #32). Nate does NOT yet know it's Engineer (correct per epistemic).","evidence":"l.129"},{"kind":"skill","name":"Structural Analysis","change":"gained","detail":"Rank 1, Low. Sole pre-loaded skill. Verbatim: 'Reveals material type, quality grade, and durability... Passive scan, focus-activated.' Consistent with #109.","evidence":"l.135"},{"kind":"ability","name":"Structural Analysis — focus-activated scan","change":"used","detail":"First use on F-250 hood: low-carbon steel, Common, 72%. No combat application yet (ch04).","evidence":"l.146-155"},{"kind":"interface","name":"HUD configuration (Phase 1)","change":"revealed","detail":"Two blue arcs only; no numbers/labels/sheet/class/tree/inventory/map/quest log/compass. Arcs 'flare white' at transport. Prose color = BLUE (vs Codex green — drift flagged).","evidence":"l.29,121-129,405"},{"kind":"companion","name":"Companion bond — Flint","change":"gained","detail":"Outbound reporting severed ('gone'), matrix 'unauthorized,' loyalty repointed to Nate, two-way link from first contact, receive-only System access. Matches #2.","evidence":"l.53-114,79,89,181"},{"kind":"event","name":"Tutorial commencement / transport","change":"reached","detail":"Global broadcast + 60-count; at 0 arcs flare white, Nate + Rex + Judge extracted. Hands to ch04.","evidence":"l.333-408"}]}},"Rex":{"by_chapter":{"ch03":[{"kind":"companion","name":"Pack-bond — Tutorial transport","change":"confirmed","detail":"Transported with Nate (#88). Pre-transport bidirectional bond; at T-30 shoulder-to-shin, 'With you' through contact. Present at left leg at 0.","evidence":"l.59,371-372,395,405"}]}},"Judge":{"by_chapter":{"ch03":[{"kind":"companion","name":"Pack-bond — Tutorial transport","change":"confirmed","detail":"Transported with Nate (#88). At ~T-10 plants at right leg, 'perfectly still for the first time all morning,' no command.","evidence":"l.396-399,405"}]}},"Flint":{"by_chapter":{"ch03":[{"kind":"self-diagnostic","name":"Companion classification — non-standard","change":"revealed","detail":"F.L.I.N.T.; outbound gone; matrix unauthorized; receive-only; loyalty repointed; read-access 'between limited and actively insulted.' Does NOT self-diagnose the divine rewrite (only 'the edges').","evidence":"l.89,101,129,181-182,197"}]}}}}
```

## Appendix B — `timeline-state.json` delta (merge target)

The 14 ordered events above, as a merge fragment, are archived verbatim in the run transcript (`subagents/workflows/wf_22b52a45-a67`, `timeline_state_json`). Shape:
`{"book":1,"by_chapter":{"ch03":[{"event","when","scope","description","consequences","evidence"}, …]}}`

## Appendix C — proposed calls

The 8 verbatim `forge_codex` entry bodies and the 1 relationship edge are in the run transcript (`proposed_codex_calls`, `proposed_relationship_edges`). Each maps 1:1 to a row in the tables above.
