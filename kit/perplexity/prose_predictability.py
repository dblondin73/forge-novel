#!/usr/bin/env python3
"""prose_predictability — local-model perplexity spot-checker for forge-novel.

The **G3 perplexity-gate graft**, built as a *teacher-forced* perplexity
spot-checker. For each word of a sentence it feeds the running prefix to a local
model on Nova and reads the model's top-K next-token distribution; the logprob
the model assigns to the word you *actually wrote* is the surprisal. Average
surprisal across the sentence -> perplexity. **Low perplexity = predictable =
"AI-flat"** (cliche openings and stock phrasing sit high in the model's
distribution); distinctive choices fall outside the top-K and score as
surprising.

This is the rigorous signal AI-text detectors use — the probabilistic cousin of
prose_lint's deterministic burstiness. It is a SPOT-CHECKER, not a bulk scanner:
teacher forcing costs one model call *per word*, so it defaults to a bounded
sample (`--max-sentences`). Use it on suspect passages, not whole books.

Why teacher-forced and not a cheap "agreement scan": a one-call-per-sentence
greedy-continuation scan was built and tested first — it did NOT discriminate
flat from distinctive prose (the model continues the story its own way and never
aligns with the next sentence), so it was replaced by this.

Constraints discovered (Ollama 0.17.x): no prompt/echo logprobs (so we teacher-
force token by token); `raw: true` is required so instruct models continue the
text instead of commenting on it; logprobs cover only generated tokens.

**Report only.** Never edits prose, never auto-strips — same contract as
prose_lint.py. Findings are advisory candidates for human review.

Stdlib only (urllib for HTTP). Needs Nova's Ollama reachable.

Usage:
    python tools/prose_predictability.py drafts/ch03-first-boot-draft01.md
    python tools/prose_predictability.py drafts/ch03-*.md --max-sentences 40
    python tools/prose_predictability.py drafts/ch03-*.md --model gemma3:4b   # faster
    python tools/prose_predictability.py drafts/ch03-*.md --longest --top 20
    python tools/prose_predictability.py drafts/ch03-*.md --format json --report-file reports/

Host: --host or $OLLAMA_HOST (default: Nova Tailscale, http://100.92.123.31:11434).
Cost: ~1 model call per word scored (a 15-word sentence = 15 calls). Bound it.
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from prose_lint_segment import HRULE, segment, split_sentences, word_count

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://100.92.123.31:11434")
DEFAULT_MODEL = "llama3:latest"
_CHAPTER_FILE_RE = re.compile(r"ch\d+.*\.md$", re.I)
_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")
_EMPHASIS_RE = re.compile(r"[*_`]")


# --- prose cleaning ---------------------------------------------------------


def clean_prose(text: str) -> str:
    """Strip markdown emphasis markers; collapse whitespace."""
    return _EMPHASIS_RE.sub("", text).strip()


def words_of(text: str) -> list[str]:
    return [w.lower() for w in _WORD_RE.findall(text)]


# --- ollama -----------------------------------------------------------------


def ollama_version(host: str, timeout: float = 8.0) -> str:
    req = urllib.request.Request(host.rstrip("/") + "/api/version")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read()).get("version", "?")


def ollama_next_topk(
    host: str, model: str, prompt: str, top_logprobs: int, timeout: float
) -> list:
    """Return the top-K next-token distribution after `prompt` (raw, greedy).

    raw=true bypasses the instruct template so the model treats `prompt` as text
    to continue (not a message to answer). We generate a single token and read
    its top_logprobs — the model's probability over what comes next.
    """
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "raw": True,
            "logprobs": True,
            "top_logprobs": max(
                1, min(top_logprobs, 20)
            ),  # Ollama caps top_logprobs at 20
            "options": {"temperature": 0, "num_predict": 1},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    lp = d.get("logprobs") or []
    return (lp[0].get("top_logprobs") or []) if lp else []


def word_surprisal(next_word: str, topk: list, floor: float) -> float:
    """Logprob the model assigns to `next_word`'s first token, or `floor`.

    Ollama emits English tokens with a leading space; we match case-insensitively
    on prefix overlap and take the best (highest) matching logprob. If the actual
    word is outside the model's top-K (a surprising / distinctive choice), it is
    floored — exactly the high-surprisal signal we want.
    """
    target = next_word.strip().lower()
    if not target:
        return 0.0
    best: Optional[float] = None
    for e in topk:
        tok = (e.get("token") or "").strip().lower()
        if not tok:
            continue
        if target.startswith(tok) or tok.startswith(target):
            lp = e.get("logprob")
            if lp is not None and (best is None or lp > best):
                best = lp
    return best if best is not None else floor


def sentence_perplexity(
    host: str, model: str, context: str, sentence: str, cfg: dict
) -> Optional[dict]:
    """Teacher-forced perplexity of `sentence` given preceding `context`."""
    toks = sentence.split()
    if not toks:
        return None
    logps: list[float] = []
    prefix = context
    for w in toks:
        topk = ollama_next_topk(
            host, model, prefix, cfg["top_logprobs"], cfg["timeout"]
        )
        logps.append(word_surprisal(w, topk, cfg["floor"]))
        prefix = (prefix + " " + w).strip() if prefix else w
    mean_lp = sum(logps) / len(logps)
    return {
        "ppl": round(math.exp(-mean_lp), 2),
        "mean_logprob": round(mean_lp, 3),
        "words": len(toks),
        "calls": len(toks),
    }


# --- scan -------------------------------------------------------------------


def _eligible_sentences(lines: list) -> list:
    """(context_words_before, lineno, clean_sentence) for each scorable sentence."""
    out = []
    context_words: list[str] = []
    for line in lines:
        if line.kind == HRULE:  # scene break resets the model's context
            context_words = []
            continue
        if not line.in_prose:
            continue
        for sent in split_sentences(line):
            clean = clean_prose(sent.text)
            out.append((list(context_words), sent.lineno, clean))
            context_words.extend(words_of(sent.text))
    return out


def scan_file(path: Path, cfg: dict) -> dict:
    raw = path.read_text(encoding="utf-8")
    lines = segment(raw)
    candidates = [
        (ctx, lineno, clean)
        for (ctx, lineno, clean) in _eligible_sentences(lines)
        if ctx and word_count(clean) >= cfg["min_words"]
    ]
    # Spot-checker: bound the work. --longest scores the meatiest sentences;
    # otherwise the first N (document order).
    if cfg["longest"]:
        candidates.sort(key=lambda c: word_count(c[2]), reverse=True)
    if cfg["max_sentences"] > 0:
        candidates = candidates[: cfg["max_sentences"]]

    findings: list[dict] = []
    errors = 0
    total_calls = 0
    t0 = time.time()
    for i, (ctx_words, lineno, clean) in enumerate(candidates, start=1):
        ctx = " ".join(ctx_words[-cfg["context_window"] :])
        try:
            r = sentence_perplexity(cfg["host"], cfg["model"], ctx, clean, cfg)
            if r:
                total_calls += r["calls"]
                findings.append({"lineno": lineno, "sentence": clean, **r})
        except (
            urllib.error.URLError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
        ) as e:
            errors += 1
            print(f"  [skip L{lineno}] {type(e).__name__}: {e}", file=sys.stderr)
        if i % 5 == 0:
            print(
                f"  ...{i}/{len(candidates)} sentences ({total_calls} calls)",
                file=sys.stderr,
            )

    ppls = sorted(f["ppl"] for f in findings)
    median = ppls[len(ppls) // 2] if ppls else None
    findings.sort(key=lambda f: f["ppl"])  # flattest (lowest ppl) first
    return {
        "file": str(path),
        "model": cfg["model"],
        "host": cfg["host"],
        "scanned": len(findings),
        "errors": errors,
        "total_calls": total_calls,
        "ppl_min": ppls[0] if ppls else None,
        "ppl_median": median,
        "ppl_max": ppls[-1] if ppls else None,
        "elapsed_s": round(time.time() - t0, 1),
        "findings": findings,
    }


# --- report -----------------------------------------------------------------


def format_text(result: dict, top: int) -> str:
    out: list[str] = []
    name = Path(result["file"]).name
    out.append(f"prose_predictability (perplexity) — {name}")
    out.append(
        f"  model={result['model']}  scanned={result['scanned']} sentences  "
        f"calls={result['total_calls']}  errors={result['errors']}  {result['elapsed_s']}s"
    )
    if result["ppl_median"] is not None:
        out.append(
            f"  perplexity: min {result['ppl_min']}  median {result['ppl_median']}  max {result['ppl_max']}"
        )
    out.append(
        "  (advisory: LOW perplexity = predictable / AI-flat — review, never auto-edit)"
    )
    out.append("")
    if not result["findings"]:
        out.append("  No sentences scored.")
        return "\n".join(out)
    out.append(
        f"  Flattest {min(top, len(result['findings']))} sentences (lowest perplexity):"
    )
    for f in result["findings"][:top]:
        out.append(f"  L{f['lineno']}  ppl {f['ppl']}  ({f['words']}w)")
        out.append(f"      {f['sentence'][:120]}")
    return "\n".join(out)


def discover(path_arg: str) -> list[Path]:
    matches = glob.glob(path_arg)
    paths: list[Path] = []
    for m in matches or [path_arg]:
        p = Path(m)
        if p.is_dir():
            paths.extend(
                sorted(c for c in p.glob("*.md") if _CHAPTER_FILE_RE.search(c.name))
            )
        elif p.is_file():
            paths.append(p)
    return paths


def main() -> int:
    for stream in (
        sys.stdout,
        sys.stderr,
    ):  # prose carries em-dashes; force utf-8 on Windows
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(
        description="Local-model perplexity spot-checker (G3, report-only)."
    )
    ap.add_argument("path", help="chapter file, glob, or drafts/ directory")
    ap.add_argument(
        "--host", default=DEFAULT_HOST, help=f"Ollama host (default: {DEFAULT_HOST})"
    )
    ap.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"model (default: {DEFAULT_MODEL}; gemma3:4b/qwen3.5:4b faster)",
    )
    ap.add_argument(
        "--max-sentences",
        type=int,
        default=25,
        help="cap sentences scored per file (0=all; teacher forcing is ~1 call/word)",
    )
    ap.add_argument(
        "--longest",
        action="store_true",
        help="score the longest sentences instead of the first N",
    )
    ap.add_argument(
        "--context-window",
        type=int,
        default=60,
        help="lead-in words fed to the model (default 60)",
    )
    ap.add_argument(
        "--top-logprobs",
        type=int,
        default=20,
        help="next-token distribution size to search (default/max 20; Ollama caps at 20)",
    )
    ap.add_argument(
        "--floor",
        type=float,
        default=-12.0,
        help="logprob assigned when the actual word is outside top-K (default -12)",
    )
    ap.add_argument(
        "--min-words",
        type=int,
        default=6,
        help="skip sentences shorter than this (default 6)",
    )
    ap.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="per-request timeout seconds (default 30)",
    )
    ap.add_argument(
        "--top",
        type=int,
        default=15,
        help="how many flattest sentences to print (default 15)",
    )
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument(
        "--report-file", metavar="DIR", help="also write the report into this directory"
    )
    args = ap.parse_args()

    cfg = {
        "host": args.host,
        "model": args.model,
        "max_sentences": args.max_sentences,
        "longest": args.longest,
        "context_window": args.context_window,
        "top_logprobs": args.top_logprobs,
        "floor": args.floor,
        "min_words": args.min_words,
        "timeout": args.timeout,
    }

    try:
        ver = ollama_version(args.host)
        print(f"Ollama {ver} @ {args.host}  (model: {args.model})", file=sys.stderr)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(
            f"ERROR: Ollama not reachable at {args.host} ({type(e).__name__}: {e}).",
            file=sys.stderr,
        )
        print(
            "Is Nova online and on the tailnet? Check `tailscale status`.",
            file=sys.stderr,
        )
        return 2

    paths = discover(args.path)
    if not paths:
        print(f"No chapter files matched: {args.path}", file=sys.stderr)
        return 2

    results = []
    for p in paths:
        print(f"Scanning {p.name} ...", file=sys.stderr)
        results.append(scan_file(p, cfg))

    if args.format == "json":
        payload = results[0] if len(results) == 1 else results
        rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    else:
        rendered = "\n\n".join(format_text(r, args.top) for r in results)
    print(rendered)

    if args.report_file:
        outdir = Path(args.report_file)
        outdir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.date.today().isoformat()
        for r in results:
            chid = (re.search(r"ch\d+", Path(r["file"]).name, re.I) or ["chapter"])[0]
            ext = "json" if args.format == "json" else "txt"
            body = (
                json.dumps(r, indent=2, ensure_ascii=False)
                if args.format == "json"
                else format_text(r, args.top)
            )
            (outdir / f"{chid}-predictability-{stamp}.{ext}").write_text(
                body, encoding="utf-8"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
