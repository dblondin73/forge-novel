"""AI-tell detectors for the forge-novel prose linter.

Each detector takes a ``Doc`` and returns a list of ``Finding``. To add a new
tell, write a ``check_*`` function and append it to ``DETECTORS`` at the bottom.

All detection is deterministic and stdlib-only — zero LLM tokens.
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field

from prose_lint_segment import Line, Sentence

FAIL = "FAIL"
WARN = "WARN"
INFO = "INFO"
_SEVERITY_ORDER = {FAIL: 0, WARN: 1, INFO: 2}

_EMDASH = "—"


@dataclass
class Finding:
    """One linter result, anchored to a physical line number."""

    lineno: int
    severity: str
    category: str
    message: str
    excerpt: str = ""

    def sort_key(self) -> tuple[int, int]:
        return (_SEVERITY_ORDER.get(self.severity, 9), self.lineno)


@dataclass
class Doc:
    """A segmented chapter plus everything the detectors need."""

    chapter_id: str
    lines: list[Line]
    prose_lines: list[Line]
    sentences: list[Sentence]
    word_count: int
    locked: bool
    thresholds: dict
    banned: dict
    burstiness_cv: float = 0.0
    _by_line: dict[int, list[Sentence]] = field(default_factory=dict)

    def sentences_for(self, lineno: int) -> list[Sentence]:
        if not self._by_line:
            for s in self.sentences:
                self._by_line.setdefault(s.lineno, []).append(s)
        return self._by_line.get(lineno, [])


# --- helpers ---------------------------------------------------------------

_MARKUP_RE = re.compile(r"[*_`]+")
_LEAD_RE = re.compile(r'^["\'“”‘’(\[]+')
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’\-]*")


def _plain(text: str) -> str:
    """Strip markdown emphasis markers so regexes match the words underneath."""
    return _MARKUP_RE.sub("", text)


def _excerpt(text: str, span: tuple[int, int], width: int = 64) -> str:
    """A short single-line snippet centred on a match span."""
    start = max(0, span[0] - width // 3)
    end = min(len(text), span[1] + width // 3)
    snippet = text[start:end].replace("\n", " ").strip()
    return ("…" if start > 0 else "") + snippet + ("…" if end < len(text) else "")


def _first_word(text: str) -> str:
    m = _WORD_RE.search(_LEAD_RE.sub("", _plain(text)))
    return m.group(0).lower() if m else ""


def _last_word(text: str) -> str:
    words = _WORD_RE.findall(_plain(text))
    return words[-1].lower() if words else ""


# --- detectors -------------------------------------------------------------


def check_emdash_density(doc: Doc) -> list[Finding]:
    """Em-dash (U+2014) density per 1000 words, with paragraph hotspots.

    On audiobook-locked chapters the chapter-level finding drops to INFO —
    high density there is expected from deliberate TTS stutter-fixes.
    """
    if doc.word_count == 0:
        return []
    t = doc.thresholds
    total = sum(ln.text.count(_EMDASH) for ln in doc.prose_lines)
    density = total / doc.word_count * 1000
    findings: list[Finding] = []
    anchor = doc.prose_lines[0].lineno if doc.prose_lines else 1

    if doc.locked:
        if density > t["emdash_per_1k_locked_warn"]:
            findings.append(Finding(
                anchor, INFO, "emdash-density",
                f"em-dash density {density:.1f}/1k ({total} total) — "
                "audiobook-locked chapter; expected from Brigid stutter-fixes. "
                "Human review only; never auto-strip.",
            ))
    elif density >= t["emdash_per_1k_warn"]:
        sev = FAIL if density >= t["emdash_per_1k_fail"] else WARN
        findings.append(Finding(
            anchor, sev, "emdash-density",
            f"em-dash density {density:.1f}/1k ({total} total); target "
            f"<= {t['emdash_per_1k_warn']:.0f}/1k. Prefer periods and commas; "
            "reserve the em-dash for a genuine interruption. Any deliberate "
            "audiobook stutter-fixes: leave them, flag for David, never auto-strip.",
        ))

    # Paragraph hotspots — informational, top 5 densest.
    hotspots: list[tuple[float, Line, int]] = []
    for ln in doc.prose_lines:
        count = ln.text.count(_EMDASH)
        words = len(_WORD_RE.findall(ln.text))
        if count >= 3 and words:
            hotspots.append((count / words * 1000, ln, count))
    hotspots.sort(key=lambda h: h[0], reverse=True)
    for para_density, ln, count in hotspots[:5]:
        findings.append(Finding(
            ln.lineno, INFO, "emdash-hotspot",
            f"paragraph em-dash density {para_density:.0f}/1k ({count} in one "
            f"paragraph; chapter average {density:.1f}/1k)",
        ))
    return findings


def _regex_detector(doc: Doc, pattern: re.Pattern, severity: str,
                    category: str, message: str) -> list[Finding]:
    findings: list[Finding] = []
    for ln in doc.prose_lines:
        plain = _plain(ln.text)
        for m in pattern.finditer(plain):
            findings.append(Finding(
                ln.lineno, severity, category, message,
                _excerpt(plain, m.span()),
            ))
    return findings


_NOT_JUST_RE = re.compile(
    r"\bnot\s+(?:just|only|merely|simply)\b[^.?!]{1,80}?\bbut\b", re.I
)
_IT_WASNT_RE = re.compile(
    r"\b(?:it|that|this|he|she|they)\s+"
    r"(?:wasn['’]?t|was\s+not|isn['’]?t|is\s+not)\b"
    r"[^.?!]{1,60}?[,:;—]\s*"
    r"(?:it|that|this|he|she|they)?\s*(?:was|is)\b",
    re.I,
)


def check_not_just_construction(doc: Doc) -> list[Finding]:
    """The 'not just X but Y' rhetorical crutch — the #1 LLM tell."""
    return _regex_detector(
        doc, _NOT_JUST_RE, FAIL, "not-just-construction",
        "'not just X but Y' construction — state the thing directly.",
    )


def check_it_wasnt_x_construction(doc: Doc) -> list[Finding]:
    """The 'it wasn't X, it was Y' antithesis crutch."""
    return _regex_detector(
        doc, _IT_WASNT_RE, FAIL, "it-wasnt-construction",
        "'it wasn't X, it was Y' antithesis — assert Y on its own.",
    )


def check_banned_vocab(doc: Doc) -> list[Finding]:
    """Tier 1 banned words (FAIL each) and Tier 2 clusters (WARN per paragraph)."""
    findings: list[Finding] = []
    tier1: dict[str, str] = doc.banned.get("tier1", {})
    tier2: set[str] = doc.banned.get("tier2", set())
    cluster_min = doc.thresholds["tier2_cluster_min"]

    for ln in doc.prose_lines:
        plain = _plain(ln.text)
        lower = plain.lower()
        for term, suggestion in tier1.items():
            term_re = re.compile(
                r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b", re.I
            )
            for m in term_re.finditer(plain):
                hint = f" — write instead: {suggestion}" if suggestion else ""
                findings.append(Finding(
                    ln.lineno, FAIL, "banned-vocab-tier1",
                    f"Tier 1 slop word '{term}'{hint}.",
                    _excerpt(plain, m.span()),
                ))
        hits = sorted({w for w in tier2 if re.search(rf"\b{re.escape(w)}\b", lower)})
        if len(hits) >= cluster_min:
            findings.append(Finding(
                ln.lineno, WARN, "banned-vocab-tier2",
                f"Tier 2 cluster — {len(hits)} suspicious words in one "
                f"paragraph: {', '.join(hits)}. Rewrite to thin them out.",
            ))
    return findings


_FICTION_TELLS = [
    (re.compile(r"\ba sense of\b", re.I), "'a sense of …' — telling, not showing"),
    (re.compile(r"\bcouldn['’]?t help but\b", re.I),
     "'couldn't help but' — passive hedging"),
    (re.compile(r"\bthe weight of\b", re.I), "'the weight of …' — cliche metaphor"),
    (re.compile(r"\bthe air was thick with\b", re.I),
     "'the air was thick with …' — dead metaphor"),
    (re.compile(r"\beyes widened\b", re.I), "'eyes widened' — lazy body language"),
    (re.compile(r"\ba wave of\b[^.?!]{0,40}?\bwashed over\b", re.I),
     "'a wave of … washed over' — AI's favourite emotion delivery"),
    (re.compile(r"\ba pang of\b", re.I), "'a pang of …' — cliche emotion delivery"),
    (re.compile(r"\bheart (?:pounded|hammered) in (?:his|her|their) chest\b", re.I),
     "'heart pounded in his chest' — where else?"),
    (re.compile(r"\ba knowing smile\b", re.I), "'a knowing smile' — says nothing"),
    (re.compile(r"\blittle did (?:he|she|they|i)\b", re.I),
     "'little did …' — forbidden narrative shortcut"),
    (re.compile(r"\bunbeknownst to\b", re.I), "'unbeknownst to' — narrative shortcut"),
    (re.compile(r"\b(?:he|she|they) felt (?:a|an|the)?\s*\w+", re.I),
     "'[character] felt …' — show the emotion through action"),
]


def check_fiction_tells(doc: Doc) -> list[Finding]:
    """Cliche fiction phrasings from the anti-slop reference."""
    findings: list[Finding] = []
    for ln in doc.prose_lines:
        plain = _plain(ln.text)
        for pattern, message in _FICTION_TELLS:
            for m in pattern.finditer(plain):
                findings.append(Finding(
                    ln.lineno, WARN, "fiction-tell", message,
                    _excerpt(plain, m.span()),
                ))
    return findings


def check_burstiness(doc: Doc) -> list[Finding]:
    """Sentence-length coefficient of variation — the systemic uniformity tell."""
    lengths = [s.words for s in doc.sentences if s.words]
    if len(lengths) < 8:
        return []
    mean = statistics.fmean(lengths)
    if mean == 0:
        return []
    cv = statistics.pstdev(lengths) / mean
    doc.burstiness_cv = cv
    if cv >= doc.thresholds["burstiness_cv_min"]:
        return []
    anchor = doc.prose_lines[0].lineno if doc.prose_lines else 1
    return [Finding(
        anchor, WARN, "burstiness",
        f"sentence-length coefficient of variation {cv:.2f} is below "
        f"{doc.thresholds['burstiness_cv_min']:.2f} (human band 0.7-1.2). "
        "Prose is flattening — vary sentence length deliberately: follow a "
        "long clause-rich sentence with a short punch.",
    )]


_PARTICIPIAL_RE = re.compile(r",\s+([A-Za-z]+ing)\b")


def check_participial_stacks(doc: Doc) -> list[Finding]:
    """Two-plus comma + '-ing' clauses stacked in one sentence."""
    findings: list[Finding] = []
    limit = doc.thresholds["participial_stack_max"]
    for s in doc.sentences:
        hits = _PARTICIPIAL_RE.findall(_plain(s.text))
        if len(hits) > limit:
            findings.append(Finding(
                s.lineno, WARN, "participial-stack",
                f"{len(hits)} stacked '-ing' clauses in one sentence "
                f"({', '.join(hits)}). Break the chain into separate sentences.",
                _excerpt(_plain(s.text), (0, min(len(s.text), 70))),
            ))
    return findings


_TRANSITIONS = {
    "however", "then", "but", "and", "so", "yet", "still", "meanwhile",
    "suddenly", "now", "instead", "later", "finally", "furthermore",
    "moreover", "additionally",
}


def check_transition_clustering(doc: Doc) -> list[Finding]:
    """Transition-word sentence-openers clustered in a sliding window."""
    findings: list[Finding] = []
    window = doc.thresholds["transition_cluster_window"]
    limit = doc.thresholds["transition_cluster_max"]
    sents = doc.sentences
    flagged: set[int] = set()
    for i in range(len(sents)):
        chunk = sents[i:i + window]
        if len(chunk) < window:
            break
        openers = [s for s in chunk if _first_word(s.text) in _TRANSITIONS]
        if len(openers) > limit and chunk[0].lineno not in flagged:
            flagged.add(chunk[0].lineno)
            words = sorted({_first_word(s.text) for s in openers})
            findings.append(Finding(
                chunk[0].lineno, WARN, "transition-cluster",
                f"{len(openers)} of {window} consecutive sentences open with a "
                f"transition word ({', '.join(words)}). Vary the openings.",
            ))
    return findings


def check_consecutive_same_ending(doc: Doc) -> list[Finding]:
    """Runs of sentences ending the same way (same word, or same -ing/-ed/-ly)."""
    findings: list[Finding] = []
    limit = doc.thresholds["consecutive_same_ending_max"]
    sents = doc.sentences

    def suffix(word: str) -> str:
        for suf in ("ing", "ed", "ly"):
            if word.endswith(suf) and len(word) > len(suf) + 1:
                return suf
        return ""

    def scan(key_fn) -> None:
        run_start = 0
        for i in range(1, len(sents) + 1):
            same = (
                i < len(sents)
                and key_fn(sents[i]) != ""
                and key_fn(sents[i]) == key_fn(sents[run_start])
            )
            if not same:
                run = sents[run_start:i]
                if len(run) > limit:
                    key = key_fn(run[0])
                    findings.append(Finding(
                        run[0].lineno, WARN, "consecutive-same-ending",
                        f"{len(run)} consecutive sentences end the same way "
                        f"('{key}'). Break the pattern.",
                    ))
                run_start = i

    scan(lambda s: _last_word(s.text))
    scan(lambda s: suffix(_last_word(s.text)))
    # De-duplicate findings landing on the same line.
    seen: set[int] = set()
    unique: list[Finding] = []
    for f in findings:
        if f.lineno not in seen:
            seen.add(f.lineno)
            unique.append(f)
    return unique


_TRICOLON_RE = re.compile(
    r"\b[\w’'-]+,\s+[\w’'-]+,\s+(?:and|or)\s+[\w’'-]+", re.I
)


def check_tricolon_density(doc: Doc) -> list[Finding]:
    """Triadic-list ('X, Y, and Z') density against the per-1k cap."""
    if doc.word_count == 0:
        return []
    hits: list[Line] = []
    for ln in doc.prose_lines:
        for _ in _TRICOLON_RE.finditer(_plain(ln.text)):
            hits.append(ln)
    if not hits:
        return []
    rate = len(hits) / doc.word_count * 1000
    cap = doc.thresholds["tricolon_per_1k_max"]
    if rate <= cap:
        return []
    return [Finding(
        hits[0].lineno, WARN, "tricolon-density",
        f"triadic lists {rate:.1f}/1k ({len(hits)} total); cap {cap:.1f}/1k. "
        "Default to two parallel items — two often lands harder than three.",
    )]


def check_paragraph_uniformity(doc: Doc) -> list[Finding]:
    """Three-plus consecutive paragraphs of near-identical sentence count."""
    findings: list[Finding] = []
    counts = [(ln.lineno, len(doc.sentences_for(ln.lineno)))
              for ln in doc.prose_lines]
    run: list[tuple[int, int]] = []

    def flush() -> None:
        if len(run) >= 3:
            findings.append(Finding(
                run[0][0], INFO, "paragraph-uniformity",
                f"{len(run)} consecutive paragraphs of near-equal length "
                f"(~{run[0][1]} sentences each). Mix in a short or long one.",
            ))

    for lineno, count in counts:
        if count < 3:
            flush()
            run = []
            continue
        window = [c for _, c in run] + [count]
        if run and max(window) - min(window) <= 1:
            run.append((lineno, count))
        else:
            flush()
            run = [(lineno, count)]
    flush()
    return findings


def check_motif_overuse(doc: Doc) -> list[Finding]:
    """Configurable motif-word overuse.

    A word that is fine once or twice but clusters into a tic across a chapter
    (forge-novel's 'honest' is the seeded case). Counts stem matches across the
    prose and WARNs when a motif exceeds its per-chapter cap. Portable: a no-op
    unless ``motif_words`` is bound in config, so the Standards layer stays
    genre-agnostic.
    """
    motifs = doc.thresholds.get("motif_words", [])
    if not motifs:
        return []
    cap = doc.thresholds.get("motif_word_max", 2)
    findings: list[Finding] = []
    for motif in motifs:
        stem = str(motif).strip().lower()
        if not stem:
            continue
        pattern = re.compile(r"\b" + re.escape(stem) + r"\w*", re.I)
        hits: list[tuple[int, str]] = []
        for ln in doc.prose_lines:
            for m in pattern.finditer(_plain(ln.text)):
                hits.append((ln.lineno, m.group(0)))
        if len(hits) > cap:
            forms = ", ".join(sorted({h[1].lower() for h in hits}))
            locs = ", ".join(f"L{n}" for n, _ in hits[:8])
            more = "" if len(hits) <= 8 else f" (+{len(hits) - 8} more)"
            findings.append(Finding(
                hits[0][0], WARN, "motif-overuse",
                f"'{stem}' motif used {len(hits)}x (cap {cap}); forms: {forms}. "
                "Clustering into a tic. Vary the wording (e.g. real / true / "
                f"sound / genuine). At: {locs}{more}.",
            ))
    return findings


DETECTORS = [
    check_emdash_density,
    check_not_just_construction,
    check_it_wasnt_x_construction,
    check_banned_vocab,
    check_fiction_tells,
    check_burstiness,
    check_participial_stacks,
    check_transition_clustering,
    check_consecutive_same_ending,
    check_tricolon_density,
    check_paragraph_uniformity,
    check_motif_overuse,
]
