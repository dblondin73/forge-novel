# Forge Novel — Audiobook Production

Draft audiobook of Book 1, Ch1-10. Full-cast delivery via ElevenLabs v3. Built as a listen-while-traveling deliverable, not a production master.

## Folder layout

```text
audiobook/
  ├── scripts/
  │   ├── audiobook_builder.py     # main pipeline: parse → route → TTS → stitch
  │   ├── generate_samples.py      # quick voice samples (one per cast member)
  │   ├── sync_to_onedrive.py      # copy finished MP3s to OneDrive for phone pickup
  │   └── cast.json                # voice IDs + production settings per role
  ├── chapters/                    # produced chapter MP3s (gitignored)
  ├── voice-samples/               # one short sample per voice (gitignored)
  ├── .cache/                      # per-paragraph MP3 + routing cache (gitignored)
  ├── VOICE-CAST.md                # human-readable cast documentation
  └── README.md                    # this file
```

## Prerequisites

- Python venv with `requests`, `anthropic` installed (uses `C:\Users\dblon\venvs\vscode-project\`)
- `ffmpeg` in PATH (chocolatey install)
- `ELEVENLABS_API_KEY` in environment (Bitwarden `elevenlabs-api` vault item)
- `ANTHROPIC_API_KEY` in environment (Bitwarden `Claude-Default-API-Key` vault item, notes field)

## One-liner to set both keys from Bitwarden and produce all chapters

```bash
export ELEVENLABS_API_KEY="$(bw get item 'elevenlabs-api' | jq -r '.fields[0].value')" && \
export ANTHROPIC_API_KEY="$(bw get item 'Claude-Default-API-Key' | jq -r '.notes')" && \
cd drafts/audiobook/scripts && \
python audiobook_builder.py --all
```

## Producing a single chapter

```bash
cd drafts/audiobook/scripts
python audiobook_builder.py --chapter ../../ch03-first-boot-draft01.md
```

## Producing voice samples only

```bash
python generate_samples.py
```

## Sync to OneDrive for phone pickup

```bash
python sync_to_onedrive.py
```

Copies chapters and samples to `C:\Users\dblon\OneDrive\Music\ForgeNovel\Book01\` — OneDrive app on phone will pull them down automatically.

## How voice routing works

1. Chapter markdown is split into paragraphs (between blank lines) and scene breaks (`---`).
2. All paragraphs are sent to Claude Haiku in a single call with the voice boundary rules.
3. Claude returns JSON mapping each paragraph idx to a voice key.
4. Routing is cached by chapter-file-content hash — identical chapter text = no re-routing.

## How caching works

- Each paragraph MP3 is cached by hash of (text + voice_id + settings).
- Rerunning a chapter skips any paragraph already synthesized.
- Edit the chapter text in one paragraph, only that paragraph re-synthesizes.
- Swap a voice_id in `cast.json`, only paragraphs using that voice re-synthesize.

## Swapping a voice

See `VOICE-CAST.md` section "Swapping a voice."

## Known limitations (v1)

- Rex (Scots) and Judge (Aussie female) ride Nate's voice channel — no accent-specific
  library voice available. Per Book 1 memory, this is accurate to the early-book design.
- No pronunciation dictionary — may mispronounce some world-specific terms.
- Claude Haiku routing is fast and cheap but not infallible. If a paragraph is misrouted,
  it's usually a storyteller/nate boundary call. Can be corrected by hand-editing the
  cached routing JSON at `.cache/routing/<chapter>-*.json` and re-running.
