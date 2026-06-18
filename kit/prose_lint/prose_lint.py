#!/usr/bin/env python3
"""prose_lint — deterministic AI-tell linter for forge-novel chapter drafts.

Zero LLM tokens. Counts and measures the slop patterns that negative
prompting cannot reliably suppress (em-dash density, sentence-length
uniformity, tricolon overuse, banned vocabulary, AI-tell constructions),
then reports exact line numbers for the editor to act on.

Usage:
    python tools/prose_lint.py drafts/ch05-first-blood-draft01.md
    python tools/prose_lint.py drafts/                 # all chNN-*.md
    python tools/prose_lint.py drafts/ch04-*.md --format json
    python tools/prose_lint.py drafts/ch05-*.md --report-file reports/

Exit codes are governed by --fail-on (default: never -> always exit 0), so
the tool is safe to wire into an advisory PostToolUse hook.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

from prose_lint_rules import DETECTORS, FAIL, INFO, WARN, Doc, Finding
from prose_lint_segment import segment, split_sentences, word_count

SCRIPT_DIR = Path(__file__).resolve().parent
BUILTIN_ANTI_SLOP = SCRIPT_DIR / "anti-slop-base.md"  # portable fallback list
BINDING_FILENAME = "kit.config.json"
_CHAPTER_FILE_RE = re.compile(r"ch\d+.*\.md$", re.I)
_CHAPTER_ID_RE = re.compile(r"(ch\d+)", re.I)
_EMDASH = "—"


# --- kit binding discovery -------------------------------------------------
# This is a Standards-layer tool: it knows nothing of forge-novel. The Novel
# layer binds it to its own files via a repo-root kit.config.json that the tool
# DISCOVERS (walking up from CWD, then from the script dir). Resolution order
# for every path is: explicit CLI flag > kit.config.json binding > portable
# built-in. Absent a binding, the tool runs standalone on its built-in defaults.


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
    """Return (paths-dict, binding-base-dir); ({}, None) when no binding found."""
    binding = find_binding()
    if binding is None:
        return {}, None
    try:
        data = json.loads(binding.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, None
    return data.get("paths", {}), binding.parent


def resolve_path(cli_value: Path | None, paths: dict, base: Path | None,
                 key: str, fallback: Path | None) -> Path | None:
    """CLI flag > kit.config.json binding > portable fallback."""
    if cli_value is not None:
        return cli_value
    rel = paths.get(key)
    if rel and base is not None:
        return base / rel
    return fallback


# --- config + anti-slop loading -------------------------------------------


def load_config(path: Path | None) -> dict:
    """Load thresholds + per-chapter flags; fall back to built-in defaults."""
    builtin = {
        "defaults": {
            "emdash_per_1k_warn": 2.0,
            "emdash_per_1k_fail": 4.0,
            "emdash_per_1k_locked_warn": 12.0,
            "burstiness_cv_min": 0.55,
            "tricolon_per_1k_max": 1.5,
            "participial_stack_max": 1,
            "consecutive_same_ending_max": 2,
            "transition_cluster_window": 5,
            "transition_cluster_max": 2,
            "tier2_cluster_min": 3,
            "motif_word_max": 2,
            "motif_words": [],
        },
        "chapters": {},
    }
    if path is not None and path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8"))
        builtin["defaults"].update(loaded.get("defaults", {}))
        builtin["chapters"] = loaded.get("chapters", {})
    return builtin


def _strip_parens(text: str) -> str:
    return re.sub(r"\([^)]*\)", "", text).strip()


def load_banned_vocab(path: Path | None) -> dict:
    """Parse the Tier 1 table and Tier 2 word list out of anti-slop.md.

    Single source of truth — editing anti-slop.md updates the linter.
    """
    banned: dict = {"tier1": {}, "tier2": set()}
    if path is None or not path.exists():
        return banned
    text = path.read_text(encoding="utf-8")

    tier1_block = re.search(
        r"##\s*Tier 1.*?\n(.*?)(?=\n##\s)", text, re.S | re.I
    )
    if tier1_block:
        for row in tier1_block.group(1).splitlines():
            cells = [c.strip() for c in row.split("|")[1:-1]]
            if len(cells) != 2 or cells[0].lower() in ("slop word", ""):
                continue
            if set(cells[0]) <= set("-: "):
                continue
            suggestion = _strip_parens(cells[1])
            for term in _strip_parens(cells[0]).split("/"):
                term = term.strip().lower()
                if term:
                    banned["tier1"][term] = suggestion

    tier2_block = re.search(
        r"##\s*Tier 2.*?\n\n(.*?)(?=\n\n)", text, re.S | re.I
    )
    if tier2_block:
        for word in tier2_block.group(1).replace("\n", " ").split(","):
            word = _strip_parens(word).strip().lower()
            if word and " " not in word:
                banned["tier2"].add(word)
    return banned


# --- analysis --------------------------------------------------------------


def chapter_id(path: Path) -> str:
    m = _CHAPTER_ID_RE.search(path.name)
    return m.group(1).lower() if m else path.stem


def build_doc(path: Path, config: dict, banned: dict) -> Doc:
    """Segment a chapter file and assemble everything the detectors need."""
    text = path.read_text(encoding="utf-8")
    lines = segment(text)
    prose_lines = [ln for ln in lines if ln.in_prose]
    sentences = []
    for ln in prose_lines:
        sentences.extend(split_sentences(ln))
    chid = chapter_id(path)
    chapter_cfg = config["chapters"].get(chid, {})
    return Doc(
        chapter_id=chid,
        lines=lines,
        prose_lines=prose_lines,
        sentences=sentences,
        word_count=sum(word_count(ln.text) for ln in prose_lines),
        locked=bool(chapter_cfg.get("audiobook_locked", False)),
        thresholds=config["defaults"],
        banned=banned,
    )


def analyze(doc: Doc) -> list[Finding]:
    findings: list[Finding] = []
    for detector in DETECTORS:
        findings.extend(detector(doc))
    findings.sort(key=Finding.sort_key)
    return findings


# --- reporting -------------------------------------------------------------


def _emdash_density(doc: Doc) -> float:
    if doc.word_count == 0:
        return 0.0
    total = sum(ln.text.count(_EMDASH) for ln in doc.prose_lines)
    return total / doc.word_count * 1000


def render_text(path: Path, doc: Doc, findings: list[Finding],
                fail_on: str) -> str:
    """Human-readable line-numbered report."""
    cv = doc.burstiness_cv
    cv_note = "OK" if cv >= doc.thresholds["burstiness_cv_min"] else "LOW"
    out = [
        f"PROSE LINT — {path.name}",
        f"Chapter {doc.chapter_id}  |  audiobook-locked: "
        f"{'YES' if doc.locked else 'no'}  |  {doc.word_count} words",
        f"Burstiness CV: {cv:.2f} ({cv_note}; human band 0.7-1.2)  |  "
        f"Em-dash density: {_emdash_density(doc):.2f}/1k",
        "",
    ]
    buckets = {FAIL: [], WARN: [], INFO: []}
    for f in findings:
        buckets[f.severity].append(f)
    for sev in (FAIL, WARN, INFO):
        group = buckets[sev]
        if not group:
            continue
        out.append(f"== {sev} ({len(group)}) ==")
        for f in group:
            out.append(f"L{f.lineno:<5} {f.category:<24} {f.message}")
            if f.excerpt:
                out.append(f"        \"{f.excerpt}\"")
        out.append("")
    n_fail, n_warn, n_info = (len(buckets[s]) for s in (FAIL, WARN, INFO))
    exit_code = compute_exit_code(findings, fail_on)
    out.append(
        f"SUMMARY: {n_fail} FAIL, {n_warn} WARN, {n_info} INFO  |  "
        f"exit {exit_code} (--fail-on {fail_on})"
    )
    return "\n".join(out)


def render_json(path: Path, doc: Doc, findings: list[Finding]) -> dict:
    return {
        "file": path.name,
        "chapter": doc.chapter_id,
        "audiobook_locked": doc.locked,
        "word_count": doc.word_count,
        "burstiness_cv": round(doc.burstiness_cv, 3),
        "emdash_density_per_1k": round(_emdash_density(doc), 2),
        "summary": {
            "fail": sum(f.severity == FAIL for f in findings),
            "warn": sum(f.severity == WARN for f in findings),
            "info": sum(f.severity == INFO for f in findings),
        },
        "findings": [
            {
                "lineno": f.lineno,
                "severity": f.severity,
                "category": f.category,
                "message": f.message,
                "excerpt": f.excerpt,
            }
            for f in findings
        ],
    }


def compute_exit_code(findings: list[Finding], fail_on: str) -> int:
    if fail_on == "never":
        return 0
    if fail_on == "fail":
        return 1 if any(f.severity == FAIL for f in findings) else 0
    if fail_on == "warn":
        return 1 if any(f.severity in (FAIL, WARN) for f in findings) else 0
    return 0


# --- CLI -------------------------------------------------------------------


def collect_targets(path: Path) -> list[Path]:
    """Resolve a file or directory argument to a list of chapter files."""
    if path.is_dir():
        return sorted(p for p in path.glob("ch*.md")
                      if _CHAPTER_FILE_RE.search(p.name))
    if path.is_file():
        return [path] if _CHAPTER_FILE_RE.search(path.name) else []
    # Glob pattern (e.g. ch04-*.md) that the shell did not expand.
    parent = path.parent if str(path.parent) not in ("", ".") else Path(".")
    return sorted(p for p in parent.glob(path.name)
                  if _CHAPTER_FILE_RE.search(p.name))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic AI-tell linter for forge-novel drafts."
    )
    parser.add_argument("path", help="chapter file, directory, or glob")
    parser.add_argument(
        "--config", type=Path, default=None,
        help="thresholds + per-chapter flags JSON "
             "(default: kit.config.json binding, else built-in defaults)",
    )
    parser.add_argument(
        "--anti-slop", type=Path, default=None,
        help="banned-vocab source markdown "
             "(default: kit.config.json binding, else anti-slop-base.md)",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--report-file", type=Path, default=None,
        help="directory to write a dated markdown report into",
    )
    parser.add_argument(
        "--fail-on", choices=("fail", "warn", "never"), default="never",
        help="exit non-zero when findings reach this severity",
    )
    args = parser.parse_args(argv)

    # Chapter prose is full of em-dashes and ellipses; force UTF-8 stdout so
    # the report renders cleanly under the Windows console's cp1252 default.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    targets = collect_targets(Path(args.path))
    if not targets:
        # Path guard: not a chapter draft — stay silent so the hook is quiet.
        return 0

    # Resolve config + anti-slop: CLI flag > kit.config.json binding > built-in.
    paths, base = load_binding()
    config_path = resolve_path(args.config, paths, base, "prose_lint_config", None)
    anti_slop_path = resolve_path(
        args.anti_slop, paths, base, "anti_slop", BUILTIN_ANTI_SLOP)
    config = load_config(config_path)
    banned = load_banned_vocab(anti_slop_path)

    json_payloads: list[dict] = []
    text_blocks: list[str] = []
    worst_exit = 0
    for target in targets:
        doc = build_doc(target, config, banned)
        findings = analyze(doc)
        worst_exit = max(worst_exit, compute_exit_code(findings, args.fail_on))
        if args.format == "json":
            json_payloads.append(render_json(target, doc, findings))
        else:
            block = render_text(target, doc, findings, args.fail_on)
            text_blocks.append(block)
            if args.report_file:
                args.report_file.mkdir(parents=True, exist_ok=True)
                today = datetime.date.today().isoformat()
                report = args.report_file / f"prose-lint-{doc.chapter_id}-{today}.md"
                report.write_text(
                    f"# Prose Lint — {target.name}\n\n```\n{block}\n```\n",
                    encoding="utf-8",
                )

    if args.format == "json":
        payload = json_payloads[0] if len(json_payloads) == 1 else json_payloads
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print("\n\n".join(text_blocks))

    return worst_exit


if __name__ == "__main__":
    sys.exit(main())
