# Ch3 — Editorial Fan-out Report (G1 MVP validation run)

> Generated 2026-05-30 by the `editors-hat-fanout` Workflow (G1 Step-1 MVP):
> 10 agents (0a linter + 8 parallel reviewers + synthesis), 78 findings from 9
> sources, ~4.5 min, ~778k subagent tokens. **Detection only — no prose edited.**
> Continuity read against Ch2 + Ch4. This is a tool-validation run; David
> approves any action.

## Scores (1-5, 5 = clean) · critical: 0

| slop | length | continuity | rule-compliance | prose-voice |
|---|---|---|---|---|
| 3 | 3 | **5** | 4 | 4 |

## Summary

Ch3 is **clean theology/cosmology and clean continuity** (every cross-chapter,
taxonomy, and banned-term check passed), but carries one real craft problem: a
**POV break at L353-355** where the Henderson six-year-old's erasure is narrated
as a witnessed VISUAL event with UI-grade certainty ("a line deleted from a
spreadsheet"), even though the chapter twice establishes Nate can only HEAR the
Henderson place a quarter mile off. The recurring weakness is
**over-explain/restating-shown stacking** — Flint dialogue shows it, then prose
re-glosses it (L91-93, L123, L181-183, L275-279) — plus a third near-identical
Rex search-loop at L77. A structural concern flagged by two reviewers
independently: **three consecutive chapters (Ch2/Ch3/Ch4) close on the identical
Storyteller-pullaway-plus-button cadence**, which the audiobook ear may register
as formulaic; varying one (likely Ch3) is recommended. No critical findings; all
em-dash hotspots are audiobook-locked INFO and must never be auto-stripped.

---

## Actionable findings (major / minor)

| Category | Issue | Severity | Location | Source |
|---|---|---|---|---|
| POV discipline | Henderson child's vanishing narrated as a witnessed VISUAL event inside Nate's close-third, but the chapter twice establishes he can only HEAR the Henderson place a quarter mile off (L25, L233). Show-the-effect rule broken by rendering UI-grade certainty as direct observation. | major | L353-355 | 3b-pov-voice |
| POV / show-effects-not-UI | "a line deleted from a spreadsheet" asserts HOW the System acted as witnessed fact from a quarter mile away. Route through Flint's network read or soften to inference. | minor | L355 | 3b-pov-voice |
| Restating-shown / over-explain | Flint's L89 performs the rewritten-from-a-template joke; L91 narrates it; L93 restates it a third time. Cut L91; salvage the label-thread clause in L93. | major | L91-93 | 1-length; 0b-slop |
| Restating-shown / list-redundancy | THIRD near-identical Rex search-loop in 18 lines (L59 establishes, L87 repeats). L77 is the flattest. Cut Rex sentences from L77; keep "Silence. Three seconds of it." | major | L77 | 1-length |
| Restating-shown | Two-curves-no-numbers HUD described a THIRD time; "That tracked" is pure epistemic-reassurance. Keep only the fresh aphorism. | major | L123 | 1-length |
| Over-explain / epistemic-reassurance | Rapture-preacher's certainty stated three times (L275 prose, L277 triple-negation restatement, L279 italic). Keep L279; cut/compress L277. | major | L275-279 | 0b-slop; 1-length |
| Repetitive chapter endings (vs adjacent) | Ch2/Ch3/Ch4 all close on "---" → Storyteller pullaway → dry button. Ch3 also bookends its own open/close. Vary one (Ch3 could close in-scene on the white-flare L405-407). David's call. | major | L409-413 (cf. Ch2 L367-372, Ch4 L503-505) | 0b-slop; 2-continuity |
| Restating-shown / epistemic-reassurance | Flint's L181 states the redirected-loyalty mechanic; L183 re-derives it. Keep the engineer-compression seed; trim the restatement. | minor | L181-183 | 1-length; 0b-slop |
| Voice-redundancy (Rex) | L87's itemized search sweep is a structural echo of L59. Only one beat should itemize the dog's arc. | minor | L87 | 1-length |
| Restating-shown (re-deciphering) | Flint spells out the acronym at L101; L103 re-parses each token. Keep "except the tether was cut" + the guide-NPC tag; cut the middle re-glossing. (Trimming relieves the L103 em-dash hotspot — do NOT strip mechanically.) | minor | L103 | 1-length |
| Restating-shown (diagnosis twice) | Pump inner-race failure diagnosed at L249, then re-revealed by Flint at L259, softening Flint's beat. Consider vaguing L249 to a sensory cue. Borderline — David's call. | minor | L249-251 vs L257/L259 | 1-length |
| Voice-redundancy / placement (fireball) | Fireball gag escalates (six→nine) so it earns its place, but the L293 check-in is buried in a status paragraph with two car-accident vignettes. Placement note. | minor | L293 | 1-length |
| Too-polished dialogue | No voice lands a genuinely imperfect line (stumble, unfinished thought) in the long two-hander. Pass-0b wants ≥1 per scene. | minor | whole chapter | 0b-slop |
| Stability trap | Two tension beats pay off with no cost (L71-79 the "Enough" silence; L197-201 the unclassified-subsystem dread filed away cleanly). Let one resolution cost something. | minor | L71-79, L197-201 | 0b-slop |
| System-intent (human-emotion) | "someone at System HQ has a sense of humor" edges toward emotion; survives as Flint Dial-5 at a hypothetical human designer, but make it a conscious keep. | minor | L239 | 3d-system-intent |
| Voice-transition (grounding) | Return from the L39-43 interlude opens on "The voice…" whose antecedent is on the far side; no physical re-root for audio. Add a re-anchor (other three returns have one). | minor | L47 | 5-prose-voice |
| Pack-bond delivery | Storyteller weave line uses the pack as an external simile for Nate/Flint — legal, but leans explanatory. Awareness only. | minor | L315 | 3b-pov-voice |
| Inventory / prop (thermos) | Thermos last placed at the Ch1 wellhead (Ch1 L56); never shown carried back. A prop reader may snag. Optional half-clause fix or leave it. | minor | L329 (cf. Ch1 L56) | 2-continuity |
| Callback consistency | Radio says "class assignment"; Ch2 bystanders say "the class thing." Plausible (uniform System UI), already softened. Likely leave. | minor | L269 (cf. Ch2 L281/293) | 2-continuity |
| Linter: transition-cluster | 3/5 consecutive sentences open with a transition word. | minor | L117, L213, L313 | linter |
| Linter: fiction-tell | "the weight of …" cliché metaphor (L121); "a sense of …" telling-not-showing (L239, also flagged by 3d). | minor | L121, L239 | linter |

## Verifications & protected beats (INFO — recorded so later passes don't "fix" them)

- **Em-dashes (146 total, 18.9/1k; hotspots L103/L193/L197/L269/L315):** audiobook-locked, deliberate Brigid stutter-fixes — INFO only, **never auto-strip.**
- **Linter false-positives overridden by 5-prose-voice:** consecutive-same-ending runs at L143 (Flint parallelism), L153 (deliberate comic rhyming callback), L317 (staccato Storyteller triplet) — **keep, load-bearing.**
- **Protect from comedy punch-up:** the L351-355 child-erasure surprise beat (cold register); the true-name soul-presence at L187-191 (correct un-named register — do NOT name the presence).
- **Counterweight KEEP-affirmed:** Flint Dial-5 stacks + Storyteller omniscient + quiet-room beats are voice-dense, not cuttable length.
- **All PASS:** theology/substrate, true-names/labels, skill taxonomy, banned-term scan, Conduit-effect-only, soul-DNA permission-not-protection, lens-labels, System-data routing, bold-on-terms, SA cadence, Storyteller weave, Hiberno register, Flint throttle, System-as-corruption contrasts, all cross-chapter continuity (Ch2→Ch3 handoff, timeline, Henderson thread, dog-formation Ch3→Ch4, crossbow foreshadow), language/rating (no findings), burstiness CV 0.93 (human band).

---

*Source labels: `linter` = deterministic Pass 0a; the rest are judgement
reviewers (lens key in the Source column). Full machine output archived in the
run transcript.*
