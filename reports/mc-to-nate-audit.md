# MC → Nate Rename Audit

*Generated: 2026-03-20*
*Scope: All `.md` files in forge-novel repo*
*Purpose: Identify every "MC" reference (main character placeholder) for rename to "Nate"*

---

## Summary

| File | Matches |
|------|---------|
| `CLAUDE.md` | 3 |
| `SESSIONS.md` | 6 |
| **Total** | **9** |

**Clean files (no MC references):**
`README.md`, `REFERENCE.md`, `characters/nate-hall.md`, `characters/flint.md`, `characters/sonja-lee.md`, `reports/session-2026-03-19-review.md`

---

## CLAUDE.md — 3 matches

All three reference the old filename `characters/MC.md` (now `characters/nate-hall.md`).

| Line | Full Line Text |
|------|---------------|
| 13 | `- Five files committed: \`README.md\`, \`REFERENCE.md\`, \`SESSIONS.md\`, \`characters/MC.md\`, \`CLAUDE.md\`` |
| 39 | `\`characters/MC.md\`, \`CLAUDE.md\`.` |
| 437 | `\| \`characters/MC.md\` \| Main character sheet (Codex ID: 1) \|` |

**Action needed:** Update all three to `characters/nate-hall.md`.

---

## SESSIONS.md — 6 matches

All six are in Session 1 (the pre-naming brainstorm). "MC" was the working placeholder before "Nate" was chosen.

| Line | Full Line Text |
|------|---------------|
| 54 | `**Focus:** MC background, inciting incident, tutorial design` |
| 58 | `**MC Background**` |
| 59 | `- Father died young; MC stepped up to help his mother run the ranch` |
| 66 | `- Opens with MC on horseback at **sunrise**, checking his cattle` |
| 70 | `- MC observes the stag before it notices him` |
| 88 | `- MC name still TBD` |

**Action needed:** Replace "MC" with "Nate" on lines 54, 58, 59, 66, 70. Line 88 (`MC name still TBD`) can be removed or replaced with a note that the name was resolved as "Nate."

---

## Excluded from this audit

References to **MCP** (Model Context Protocol server) appear throughout `CLAUDE.md`, `README.md`, `REFERENCE.md`, and `SESSIONS.md`. These are infrastructure references (e.g., `forge-mcp`, `FastMCP`, `git-forge-mcp`) and are NOT related to the main character rename. They were excluded from this report.

---

## Notes

- `characters/MC.md` no longer exists in the repo — it has already been renamed to `characters/nate-hall.md` with full content using "Nate."
- All character sheets (`nate-hall.md`, `flint.md`, `sonja-lee.md`) already use "Nate" consistently.
- The `reports/session-2026-03-19-review.md` file already uses "Nate" throughout.
- No outline directory or beat files exist in the repo yet, so no POV/beat-level matches to report.
