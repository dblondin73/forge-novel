#!/usr/bin/env python3
"""recap - "Previously On" SOURCE PACK aggregator.

Zero LLM tokens. Assembles the raw continuity material for a recap across a
chapter range, then STOPS. It writes no prose: the recap itself ("Previously
on...") is a Storyteller-voice prose task and stays agent-side. This tool only
gathers the deterministic ground truth the agent turns into prose - exactly the
preflight/timeline/ledger division of labor.

It pulls three already-maintained stores (all via the kit binding) and merges
the slice that falls in the requested chapter range:

  * EVENTS         - what happened          (timeline.json, append-only log)
  * OPEN THREADS   - what's still promised   (promises.json, the payoff ledger)
  * KNOWLEDGE      - what the POV learned     (epistemic-states.json, per chapter)

STANDARDS-LAYER TOOL: it knows nothing of any specific novel. The Novel layer
binds it to its own files via a repo-root kit.config.json that this tool
DISCOVERS (walking up from CWD, then the script dir). Each source path resolves
explicit-flag > binding > built-in default; any missing source is skipped with a
note so a partly-wired project still gets a usable pack.

Usage:
    python kit/recap/recap.py --chapter 1-8
    python kit/recap/recap.py --chapter 6 --format md
    python kit/recap/recap.py --chapter 1-8 --format json
    python kit/recap/recap.py --chapter 1-8 --pov-character nate

Output is SOURCE MATERIAL, never the recap. Exit 0 always (it is a generator,
not a gate).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BINDING_FILENAME = "kit.config.json"
DEFAULTS = {
    "timeline": "timeline.json",
    "promises": "promises.json",
    "epistemic_states": "epistemic-states.json",
}


# --- kit binding discovery -------------------------------------------------


def find_binding() -> Path | None:
    """Locate kit.config.json by walking up from CWD, then from this script."""
    seen: set[Path] = set()
    for start in (Path.cwd(), SCRIPT_DIR):
        for d in (start, *start.parents):
            if d in seen:
                continue
            seen.add(d)
            cand = d / BINDING_FILENAME
            if cand.is_file():
                return cand
    return None


def load_binding() -> tuple[dict, Path | None]:
    """Return (binding-dict, binding-base-dir); ({}, None) when none found."""
    binding = find_binding()
    if binding is None:
        return {}, None
    try:
        data = json.loads(binding.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, None
    return data, binding.parent


def resolve_path(flag: str | None, key: str, base: Path | None,
                 repo: Path, paths: dict) -> Path:
    """explicit flag > binding paths[key] > built-in default (<repo>/<default>)."""
    if flag:
        return Path(flag)
    rel = paths.get(key)
    if rel and base is not None:
        return base / rel
    return repo / DEFAULTS[key]


# --- chapter range ---------------------------------------------------------


def parse_chapter_range(raw: str | None) -> set[int] | None:
    """Parse "8" or "1-6" or "1,3,5" into a set of chapter numbers (None = all)."""
    if not raw:
        return None
    out: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            out.update(range(int(lo), int(hi) + 1))
        elif part:
            out.add(int(part))
    return out or None


def _read_json(path: Path) -> tuple[dict | None, str | None]:
    """Return (data, None) or (None, reason) - never raises on a missing/bad file."""
    if not path.exists():
        return None, f"not found: {path}"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"unreadable ({exc})"
    if not isinstance(data, dict):
        return None, "root is not a JSON object"
    return data, None


# --- gather each source ----------------------------------------------------


def gather_events(path: Path, chapters: set[int] | None) -> tuple[list[dict], str | None]:
    data, err = _read_json(path)
    if err:
        return [], err
    events = data.get("events", [])
    if not isinstance(events, list):
        return [], "`events` is not a list"
    rows = [e for e in events if isinstance(e, dict)
            and (chapters is None or e.get("chapter") in chapters)]
    return sorted(rows, key=lambda e: (e.get("chapter") or 0, e.get("seq") or 0)), None


def gather_open_threads(path: Path, chapters: set[int] | None) -> tuple[list[dict], str | None]:
    """Open promises PLANTED within the range - the hooks a recap reminds the reader of."""
    data, err = _read_json(path)
    if err:
        return [], err
    promises = data.get("promises", [])
    if not isinstance(promises, list):
        return [], "`promises` is not a list"
    closed = {"paid", "abandoned", "subverted"}
    rows = [p for p in promises if isinstance(p, dict)
            and str(p.get("status", "")) not in closed
            and (chapters is None or p.get("planted_chapter") in chapters)]
    return sorted(rows, key=lambda p: (p.get("planted_chapter") or 0, str(p.get("id", "")))), None


def gather_knowledge(path: Path, pov: str | None,
                     chapters: set[int] | None) -> tuple[dict, str | None]:
    if not pov:
        return {}, "no pov_character bound (pass --pov-character)"
    data, err = _read_json(path)
    if err:
        return {}, err
    chars = data.get("characters", {})
    entry = chars.get(pov) if isinstance(chars, dict) else None
    if not isinstance(entry, dict):
        return {}, f"no epistemic entry for pov '{pov}'"
    out: dict[int, list] = {}
    selected = sorted(chapters) if chapters else range(1, 100)
    for n in selected:
        key = f"after_ch{n:02d}"
        rec = entry.get(key)
        if isinstance(rec, dict):
            learned = rec.get("learned_this_chapter")
            if learned:
                out[n] = learned
    return out, None


# --- render ----------------------------------------------------------------


def _span_label(chapters: set[int] | None) -> str:
    if not chapters:
        return "all chapters"
    lo, hi = min(chapters), max(chapters)
    return f"chapter {lo}" if lo == hi else f"chapters {lo}-{hi}"


def render_text(span: str, pov: str | None, events: list[dict], notes_e: str | None,
                threads: list[dict], notes_t: str | None,
                knowledge: dict, notes_k: str | None) -> str:
    out: list[str] = []
    out.append(f"RECAP SOURCE PACK - {span}")
    out.append("=" * (len(span) + 19))
    out.append("")
    out.append("This is SOURCE MATERIAL, not the recap. The Storyteller writes the")
    out.append("'Previously on...' in omniscient (Hiberno) voice from the beats below.")
    out.append("")

    out.append(f"WHAT HAPPENED ({len(events)} event(s))")
    if notes_e:
        out.append(f"  (timeline unavailable: {notes_e})")
    for e in events:
        chap = e.get("chapter", "?")
        who = (" [" + ", ".join(str(w) for w in e["who"]) + "]") if e.get("who") else ""
        where = (" @ " + str(e["where"])) if e.get("where") else ""
        out.append(f"  ch{chap}: {e.get('event', '')}{who}{where}")
    out.append("")

    out.append(f"WHAT'S STILL PROMISED ({len(threads)} open thread(s) planted in range)")
    if notes_t:
        out.append(f"  (ledger unavailable: {notes_t})")
    for p in threads:
        kind = p.get("kind", "?")
        due = (f" (due ch{p['due_by_chapter']})") if p.get("due_by_chapter") else ""
        out.append(f"  [{kind}] ch{p.get('planted_chapter', '?')}: "
                   f"{p.get('promise', '')}{due}")
    out.append("")

    pov_label = pov or "POV"
    out.append(f"WHAT {pov_label.upper()} LEARNED")
    if notes_k:
        out.append(f"  (epistemic unavailable: {notes_k})")
    for n in sorted(knowledge):
        for item in knowledge[n]:
            out.append(f"  ch{n}: {item}")
    out.append("")
    return "\n".join(out)


def render_md(span: str, pov: str | None, events: list[dict], notes_e: str | None,
              threads: list[dict], notes_t: str | None,
              knowledge: dict, notes_k: str | None) -> str:
    out: list[str] = []
    out.append(f"# Recap source pack — {span}")
    out.append("")
    out.append("_Source material, not the recap. The Storyteller writes the "
               "\"Previously on...\" from these beats._")
    out.append("")
    out.append("## What happened")
    if notes_e:
        out.append(f"_(timeline unavailable: {notes_e})_")
    for e in events:
        who = (" — " + ", ".join(str(w) for w in e["who"])) if e.get("who") else ""
        out.append(f"- **ch{e.get('chapter', '?')}:** {str(e.get('event', '')).rstrip('.')}.{who}")
    out.append("")
    out.append("## What's still promised")
    if notes_t:
        out.append(f"_(ledger unavailable: {notes_t})_")
    for p in threads:
        due = (f" _(due ch{p['due_by_chapter']})_") if p.get("due_by_chapter") else ""
        out.append(f"- **[{p.get('kind', '?')}] ch{p.get('planted_chapter', '?')}:** "
                   f"{str(p.get('promise', '')).rstrip('.')}.{due}")
    out.append("")
    out.append(f"## What {(pov or 'POV')} learned")
    if notes_k:
        out.append(f"_(epistemic unavailable: {notes_k})_")
    for n in sorted(knowledge):
        for item in knowledge[n]:
            out.append(f"- **ch{n}:** {item}")
    out.append("")
    return "\n".join(out)


# --- main ------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assemble a 'Previously On' recap SOURCE PACK (events + open "
                    "threads + knowledge) for a chapter range. Writes no prose.")
    parser.add_argument("--chapter", default=None,
                        help='chapter selector: "8", "1-6", or "1,3,5" (default: all)')
    parser.add_argument("--format", choices=("text", "json", "md"), default="text")
    parser.add_argument("--pov-character", default=None,
                        help="epistemic-states key for the POV (default: binding pov_character)")
    parser.add_argument("--timeline", default=None, help="override timeline.json path")
    parser.add_argument("--promises", default=None, help="override promises.json path")
    parser.add_argument("--epistemic", default=None, help="override epistemic-states.json path")
    args = parser.parse_args()

    binding, base = load_binding()
    paths = binding.get("paths", {})
    repo = base or Path.cwd()
    pov = args.pov_character or binding.get("pov_character")

    timeline_path = resolve_path(args.timeline, "timeline", base, repo, paths)
    promises_path = resolve_path(args.promises, "promises", base, repo, paths)
    epistemic_path = resolve_path(args.epistemic, "epistemic_states", base, repo, paths)

    chapters = parse_chapter_range(args.chapter)
    span = _span_label(chapters)

    events, notes_e = gather_events(timeline_path, chapters)
    threads, notes_t = gather_open_threads(promises_path, chapters)
    knowledge, notes_k = gather_knowledge(epistemic_path, pov, chapters)

    if args.format == "json":
        print(json.dumps({
            "span": span,
            "chapters": sorted(chapters) if chapters else None,
            "pov_character": pov,
            "events": events,
            "open_threads_planted_in_range": threads,
            "knowledge_gained": {str(k): v for k, v in sorted(knowledge.items())},
            "notes": {"events": notes_e, "threads": notes_t, "knowledge": notes_k},
        }, indent=2, ensure_ascii=False))
    elif args.format == "md":
        print(render_md(span, pov, events, notes_e, threads, notes_t, knowledge, notes_k))
    else:
        print(render_text(span, pov, events, notes_e, threads, notes_t, knowledge, notes_k))
    sys.exit(0)


if __name__ == "__main__":
    main()
