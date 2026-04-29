"""
audiobook_builder.py — Produce full-cast audiobook MP3 from forge-novel chapter drafts.

Pipeline:
  1. Parse the chapter markdown into ordered segments (paragraph, scene_break, heading).
  2. Route each paragraph to a voice via Claude Haiku (uses cast table).
  3. Synthesize each paragraph via ElevenLabs v3 with voice-specific settings.
  4. Stitch paragraph MP3s with inter-paragraph and scene-break silence via ffmpeg.

Caching:
  - Routing results cached by chapter file hash (saved to .cache/routing/).
  - Per-paragraph MP3s cached by (text + voice_id + settings) hash (saved to .cache/segments/).
  - If a run fails mid-chapter, the next run skips anything already produced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import requests
from anthropic import Anthropic


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
CHAPTERS_OUT = ROOT / "chapters"
SAMPLES_OUT = ROOT / "voice-samples"
CACHE = ROOT / ".cache"
ROUTING_CACHE = CACHE / "routing"
SEGMENT_CACHE = CACHE / "segments"
SILENCE_CACHE = CACHE / "silence"
for d in (CHAPTERS_OUT, SAMPLES_OUT, CACHE, ROUTING_CACHE, SEGMENT_CACHE, SILENCE_CACHE):
    d.mkdir(parents=True, exist_ok=True)

CAST_PATH = SCRIPTS_DIR / "cast.json"
CAST = json.loads(CAST_PATH.read_text(encoding="utf-8"))
VOICES = CAST["voices"]
ELEVEN_API_KEY = os.environ["ELEVENLABS_API_KEY"]
ANTHROPIC_CLIENT = Anthropic()

ELEVEN_BASE = "https://api.elevenlabs.io/v1"
ELEVEN_MODEL = CAST["_meta"]["model"]
ELEVEN_FORMAT = CAST["_meta"]["output_format"]

PROFANITY_TIMING_RE = re.compile(r",\s+(shit|hell|damn|christ|jesus|fuck)\b", re.IGNORECASE)
PURE_DIGITS_RE = re.compile(r"^\s*\d+\s*[.\s]*$")

_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
         "seventeen", "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def _num_to_words(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return _TENS[t] + ("-" + _ONES[o] if o else "")
    if n < 1000:
        h, r = divmod(n, 100)
        base = _ONES[h] + " hundred"
        return base + (" " + _num_to_words(r) if r else "")
    return str(n)  # fallback for larger numbers — TTS will still pronounce them


def _expand_digit_paragraph(text: str) -> str:
    """If a paragraph is purely a number (e.g., a countdown), spell it out so TTS accepts it."""
    m = PURE_DIGITS_RE.match(text)
    if not m:
        return text
    digits = re.findall(r"\d+", text)[0]
    n = int(digits)
    # Capitalize the spelled-out form and add a period for breath.
    spelled = _num_to_words(n)
    spelled = spelled[0].upper() + spelled[1:]
    return spelled + "."


_BRACKET_RE = re.compile(r"\[([^\[\]]+)\]")
_SPEAKER_TAG_RE = re.compile(r"^[A-Z_][A-Z0-9_\s]{0,18}$")


def _unwrap_system_brackets(text: str) -> str:
    """Unwrap [bracketed content] unless it looks like an ElevenLabs speaker tag.

    Speaker tags are short, all-caps, no punctuation (e.g., [NATHAN]). Forge-novel
    System screen readouts like [Structural Analysis - Target: Ford F-250, ...] use
    brackets as a visual convention; ElevenLabs strips them as speaker tags and the
    input becomes empty. Unwrap those so TTS reads the contents.
    """
    def replace(m: re.Match) -> str:
        content = m.group(1).strip()
        if _SPEAKER_TAG_RE.match(content):
            return m.group(0)
        return content
    return _BRACKET_RE.sub(replace, text)


# ---------- Markdown parsing ----------

MD_BOLD = re.compile(r"\*\*(.+?)\*\*")
MD_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
MD_UNDERSCORE_ITALIC = re.compile(r"_([^_]+)_")
MD_LINK = re.compile(r"\[([^\]]+)\]\([^\)]+\)")


def strip_markdown(text: str) -> str:
    """Strip markdown formatting for TTS; preserve the words."""
    text = MD_BOLD.sub(r"\1", text)
    text = MD_UNDERSCORE_ITALIC.sub(r"\1", text)
    text = MD_ITALIC.sub(r"\1", text)
    text = MD_LINK.sub(r"\1", text)
    text = text.replace("&mdash;", "—").replace("&ndash;", "–")
    return text.strip()


def parse_chapter(md_path: Path) -> list[dict]:
    """Split chapter into ordered segments.

    Returns a list of dicts: {type, text, idx} where type is 'heading', 'paragraph',
    or 'scene_break'.
    """
    raw = md_path.read_text(encoding="utf-8")
    segments: list[dict] = []
    idx = 0
    for block in re.split(r"\n\s*\n", raw):
        block = block.strip()
        if not block:
            continue
        if re.fullmatch(r"-{3,}", block):
            segments.append({"type": "scene_break", "text": "", "idx": idx})
            idx += 1
            continue
        if block.startswith("#"):
            heading = block.lstrip("#").strip()
            segments.append({"type": "heading", "text": strip_markdown(heading), "idx": idx})
            idx += 1
            continue
        clean = strip_markdown(block)
        if not clean:
            continue
        segments.append({"type": "paragraph", "text": clean, "idx": idx})
        idx += 1
    return segments


# ---------- Routing (Claude) ----------

def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


ROUTING_SYSTEM = """You are routing paragraphs of a fantasy LitRPG novel to voice actors for an audiobook.

## THE MASTER RULE

**Brigid (Irish-warmth female) is the DEFAULT voice for almost every paragraph.** She \
has TWO registers — same voice actor, different energy — and the router picks which one.

- **storyteller_omniscient** — slow, literary, wry. Use for:
  - Chapter OPENS and CLOSES (the "last normal morning" frames, the retrospective-wisdom summations).
  - Interludes that pull out to the wider world.
  - Dramatic irony and philosophical asides ("Some mornings arrive carrying more than they show").
  - Anything that reads as the narrator pulling back, knowing more than the characters.

- **storyteller_narrator** — faster, more dynamic range, close. Use for:
  - In-scene description and sensory detail.
  - Physical zoom into Nate (the former "Camera" mode) — what he sees, what his hands do, what the pump sounds like.
  - Action, combat, movement.
  - Most of the chapter.

If you're unsure which Brigid register, pick `storyteller_narrator` — it's the workhorse.

**Other voices are exceptions, used ONLY when:**
- A paragraph is quoted dialogue attributed to a named speaker → route to that speaker.
- A paragraph is an entirely-italicized direct interior monologue from Nate \
  (explicitly framed as his thinking voice) → route to `nate`.
- A paragraph is a dialogue exchange where the speaker attribution is unambiguous from \
  context (e.g., "Helpful." right after Flint was speaking in the prior paragraph).

Do NOT route tight-third prose that describes what Nate sees/feels/thinks TO `nate`. \
That is Storyteller-zoom. The Nate voice is for his MOUTH and his explicit inner \
voice, nothing else.

## Voices available

- **storyteller_omniscient** / **storyteller_narrator** — Brigid's two registers; see above.
- **nate** — Nate Hall's spoken dialogue and explicit italicized direct thoughts.
- **flint** — F.L.I.N.T.'s spoken dialogue (theatrical, fast, witty).
- **marcus_webb, josie_pickett, sam_hargrove, ana_torres, walt_keane, pete_bowman, \
kyle_greene, mack_turner, heather_kim, isabel_wu, martin_voss, tyler_sorensen** — \
other named speakers; use when their dialogue is attributed to them.
- **unknown_male / unknown_female** — for unattributed minor speakers.

## What counts as dialogue

- Text in double quotes `"..."` that has a clear speaker (attributed in-paragraph or \
  in the prior/next sentence).
- A paragraph that opens with `"..."` from a named speaker, even if the same paragraph \
  contains narrator-y description afterward, is still their dialogue line — the \
  speaker's voice.

If a paragraph mixes dialogue from two speakers, pick the dominant one. If ambiguous, \
pick storyteller.

## Output

Return a single JSON object (no prose, no markdown fences):
{"routing": [{"idx": 0, "voice": "storyteller_omniscient"}, {"idx": 1, "voice": "storyteller_narrator"}, ...]}

Include one entry per paragraph passed in. If unsure, default to storyteller_narrator.
"""


def route_chapter(segments: list[dict], md_path: Path) -> dict[int, str]:
    """Return mapping of paragraph idx -> voice_key."""
    paragraphs = [s for s in segments if s["type"] == "paragraph"]
    if not paragraphs:
        return {}

    cache_file = ROUTING_CACHE / f"{md_path.stem}-{_file_hash(md_path)}.json"
    if cache_file.exists():
        print(f"[route] cache hit: {cache_file.name}")
        return {int(k): v for k, v in json.loads(cache_file.read_text(encoding="utf-8")).items()}

    # Build user content with numbered paragraphs.
    lines = [
        "Here is the chapter. Route each paragraph to a voice. "
        "Return JSON with a 'routing' array.\n",
    ]
    for p in paragraphs:
        lines.append(f"[{p['idx']}] {p['text']}")
        lines.append("")
    user_content = "\n".join(lines)

    print(f"[route] calling Claude on {len(paragraphs)} paragraphs...")
    resp = ANTHROPIC_CLIENT.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8192,
        system=ROUTING_SYSTEM,
        messages=[{"role": "user", "content": user_content}],
    )
    raw = resp.content[0].text.strip()
    # Strip markdown fences if present.
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    parsed = json.loads(raw)
    routing = {int(e["idx"]): e["voice"] for e in parsed["routing"]}
    # Ensure every paragraph has an assignment.
    for p in paragraphs:
        routing.setdefault(p["idx"], "storyteller")
    cache_file.write_text(json.dumps({str(k): v for k, v in routing.items()}, indent=2), encoding="utf-8")
    print(f"[route] saved: {cache_file.name}")
    return routing


# ---------- TTS ----------

def _apply_voice_preprocessing(voice_key: str, text: str) -> str:
    """Apply per-voice pipeline rules (ellipsis prefix, timed profanity, digit-spellout, bracket-unwrap)."""
    text = _unwrap_system_brackets(text)
    text = _expand_digit_paragraph(text)
    voice = VOICES[voice_key]
    if voice.get("prefix"):
        text = voice["prefix"] + text
    if voice.get("timed_profanity"):
        text = PROFANITY_TIMING_RE.sub(lambda m: f"... {m.group(1)}", text)
    return text


def synthesize_paragraph(text: str, voice_key: str) -> Path:
    """TTS a single paragraph; return path to cached MP3."""
    voice = VOICES[voice_key]
    processed = _apply_voice_preprocessing(voice_key, text)
    settings = voice["settings"]
    # Cache key includes text, voice_id, and settings — invalidates if any change.
    cache_key_material = json.dumps({
        "t": processed,
        "v": voice["voice_id"],
        "s": settings,
        "m": ELEVEN_MODEL,
        "f": ELEVEN_FORMAT,
    }, sort_keys=True)
    h = hashlib.sha256(cache_key_material.encode("utf-8")).hexdigest()[:24]
    out_path = SEGMENT_CACHE / f"{voice_key}-{h}.mp3"
    if out_path.exists() and out_path.stat().st_size > 0:
        return out_path

    url = f"{ELEVEN_BASE}/text-to-speech/{voice['voice_id']}"
    payload = {
        "text": processed,
        "model_id": ELEVEN_MODEL,
        "voice_settings": {
            "stability": settings["stability"],
            "style": settings["style"],
            "similarity_boost": settings["similarity_boost"],
            "use_speaker_boost": settings["use_speaker_boost"],
            "speed": settings["speed"],
        },
        "output_format": ELEVEN_FORMAT,
    }
    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}

    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=180)
            if r.status_code == 200:
                out_path.write_bytes(r.content)
                return out_path
            if r.status_code in (429, 502, 503, 504):
                wait = 2 ** attempt * 5
                print(f"[tts] {r.status_code} — retry in {wait}s (attempt {attempt + 1}/3)")
                time.sleep(wait)
                continue
            raise RuntimeError(f"ElevenLabs {r.status_code}: {r.text[:400]}")
        except requests.RequestException as e:
            print(f"[tts] request error: {e} — retry in 5s")
            time.sleep(5)
    raise RuntimeError(f"TTS failed after 3 attempts for voice={voice_key}, text={text[:80]}")


# ---------- Stitching ----------

def generate_silence(seconds: float) -> Path:
    """Generate (and cache) an MP3 of silence."""
    out = SILENCE_CACHE / f"silence-{int(seconds * 1000)}ms.mp3"
    if out.exists():
        return out
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(seconds), "-q:a", "9", "-acodec", "libmp3lame", str(out),
        ],
        check=True, capture_output=True,
    )
    return out


def stitch_chapter(segments: list[dict], routing: dict[int, str], output_mp3: Path) -> None:
    """Build the full-chapter MP3 by concatenating paragraph MP3s + silence segments."""
    # Silences
    para_silence = generate_silence(0.6)     # between paragraphs in same scene
    scene_silence = generate_silence(2.0)    # between scenes
    heading_silence = generate_silence(1.0)  # after chapter heading

    parts: list[Path] = []
    for seg in segments:
        if seg["type"] == "scene_break":
            parts.append(scene_silence)
            continue
        if seg["type"] == "heading":
            mp3 = synthesize_paragraph(seg["text"], "storyteller")
            parts.append(mp3)
            parts.append(heading_silence)
            continue
        if seg["type"] == "paragraph":
            voice_key = routing.get(seg["idx"], "storyteller")
            if voice_key not in VOICES:
                print(f"[stitch] WARN: unknown voice_key '{voice_key}' for idx {seg['idx']}; defaulting to storyteller")
                voice_key = "storyteller"
            mp3 = synthesize_paragraph(seg["text"], voice_key)
            parts.append(mp3)
            parts.append(para_silence)

    # ffmpeg concat via a list file
    list_file = CACHE / f"concat-{output_mp3.stem}.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for p in parts:
            posix = str(p).replace("\\", "/")
            f.write(f"file '{posix}'\n")

    print(f"[stitch] concatenating {len(parts)} pieces -> {output_mp3.name}")
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c:a", "libmp3lame", "-q:a", "3", str(output_mp3),
        ],
        check=True, capture_output=True,
    )


# ---------- Main ----------

def produce_chapter(md_path: Path, output_dir: Path) -> Path:
    print(f"\n=== {md_path.name} ===")
    segments = parse_chapter(md_path)
    paragraphs_count = sum(1 for s in segments if s["type"] == "paragraph")
    print(f"[parse] {len(segments)} segments ({paragraphs_count} paragraphs)")
    routing = route_chapter(segments, md_path)
    out_mp3 = output_dir / f"{md_path.stem}.mp3"
    stitch_chapter(segments, routing, out_mp3)
    print(f"[done] {out_mp3} ({out_mp3.stat().st_size / 1024 / 1024:.1f} MB)")
    return out_mp3


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", help="path to a single chapter markdown")
    ap.add_argument("--all", action="store_true", help="produce Ch1-10")
    ap.add_argument("--drafts-dir", default=str((ROOT / ".." / "..").resolve() / "drafts"))
    ap.add_argument("--output-dir", default=str(CHAPTERS_OUT))
    args = ap.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.chapter:
        produce_chapter(Path(args.chapter).resolve(), output_dir)
        return

    if args.all:
        drafts_dir = Path(args.drafts_dir)
        chapters = sorted(drafts_dir.glob("ch[01][0-9]-*-draft01.md"))
        # Keep numeric order
        def _num(p: Path) -> int:
            m = re.match(r"ch(\d+)", p.name)
            return int(m.group(1)) if m else 999
        chapters.sort(key=_num)
        print(f"Found {len(chapters)} chapters: {[c.name for c in chapters]}")
        for ch in chapters:
            produce_chapter(ch, output_dir)
        return

    ap.error("must pass --chapter <path> or --all")


if __name__ == "__main__":
    main()
