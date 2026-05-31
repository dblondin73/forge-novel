# Anti-Slop — Portable Base List (Standards)

Generic AI-tell vocabulary for the `prose_lint` engine when it runs **standalone**
(no `kit.config.json` binding pointing at a project-specific anti-slop file).
A bound project (e.g. forge-novel's `references/anti-slop.md`) **overrides** this
file entirely via the binding's `anti_slop` path — this base is the fallback, not
a merge.

`prose_lint` parses the **Tier 1** table (slop word → suggestion) and the
**Tier 2** comma list out of this file at runtime. Keep the formats below;
add your own genre/voice-specific bans in the bound project's file, not here.

## Tier 1 — banned outright (slop word | suggestion)

| Slop word | Suggestion |
|---|---|
| delve | dig into / go into |
| tapestry | (cut — concrete image) |
| testament to | shows / proves |
| navigate (figurative) | handle / work through |
| realm (figurative) | area / world |
| boasts (a feature) | has |
| nestled | sits / set |
| bustling | busy / crowded |
| myriad | many |
| plethora | plenty / too many |
| underscore | stress / show |
| pivotal | key / central |
| intricate | detailed / complex |
| seamless | smooth |
| vibrant | (cut — concrete detail) |
| meticulous | careful |
| ever-evolving | changing |
| treasure trove | (cut — concrete image) |

## Tier 2 — flag on clustering (3+ in a window)

These are not banned outright but signal AI flatness when they cluster. The
linter flags a run of three or more in a short window.

moreover, furthermore, additionally, notably, importantly, essentially, ultimately, crucially, indeed, arguably, certainly, particularly, significantly, however, nonetheless, thus, hence, therefore, consequently, subsequently
