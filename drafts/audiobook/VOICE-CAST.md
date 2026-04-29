# Audiobook Voice Cast — v1 (Apr 24 2026)

Generated for the Ch1-10 travel draft. Canonical voices (Storyteller, Nate) are locked per `project_narrator_voice.md`. Everything else is a **library pick** from the ElevenLabs voice catalog — easily swapped via `scripts/cast.json`.

## Locked canonical voices

| Role | Voice | Voice ID | Settings |
|------|-------|----------|----------|
| **Storyteller** | Brigid | `6962rZHcjwkuvYx439zm` | v3, stability 0.50, style 0.10, similarity 0.75, speed 0.85, ellipsis prefix |
| **Nate Hall** | Nate | `10KeNBezdmUZLupy2IWN` | v3, stability 0.50, style 0.10, similarity 0.75, speed 0.90, timed profanity |

## v1 library picks (swap freely)

| Character | Library voice | Voice ID | Why picked |
|-----------|---------------|----------|-----------|
| **F.L.I.N.T.** | Callum - Husky Trickster | `N2lVS1w4EtoT3dr4eOWO` | "Trickster" register is the closest library match to Bob-the-Skull / Marsters |
| **Marcus Webb** | Brian - Deep, Resonant and Comforting | `nPczCjzI2devNBz1zQrb` | Deep rumble, Clarke-Duncan proximity |
| **Josie Pickett** | Matilda - Knowledgable, Professional | `XrExE9yKIg1WjnnlVkGX` | Fast cataloging professional |
| **Sam Hargrove** | Chuck Miller - Deep, Raspy, American | `HIGUfNOdjuWQwwapnTRW` | Construction worker register |
| **Ana Torres** | Sarah - Mature, Reassuring, Confident | `EXAVITQu4vr4xnSDxMaL` | Triage / medical register |
| **Walt Keane** | Cowboy Chris - Deep and Supportive | `o3VpiaQ9JcGIFpOrkHHf` | Rural trades, patient |
| **Pete Bowman** | Will - Relaxed Optimist | `bIHbv24MWmeRgasZH58o` | Oregon outdoorsy young |
| **Kyle Greene** | Liam - Energetic Social Media Creator | `TX3LPaxmHKxFdv7VOQHJ` | Contract-signer foil, too-confident |
| **Mack Turner** | Chris - Charming, Down-to-Earth | `iP95p4xoKVk53GoZ742B` | Ranger / Scout floor-4 anchor |
| **Heather Kim** | Bella - Professional, Bright, Warm | `hpp4J3VqNfWAUOO0d1Us` | Ward Mage, mother-on-knees |
| **Isabel Wu** | Laura - Enthusiast, Quirky Attitude | `FGY2WhTYpPnrIDTdsKH5` | Alchemist rest-area 2 |
| **Dr. Martin Voss** | George - Warm British Storyteller | `JBFqnCBsd6RMkjVDRZzb` | Scholar, floor-6 witness |
| **Tyler Sorensen** | Harry - Fierce Warrior | `SOYHLrjzK2X1ezoPC6cr` | 17-year-old, Ch6 casualty |
| **Unknown male** | Adam - Dominant, Firm | `pNInz6obpgDQGcFmaJgB` | Fallback for unnamed males |
| **Unknown female** | Alice - Clear, Engaging Educator | `Xb7hH8MSUJpSbSDYk0k2` | Fallback for unnamed females |

## Unresolved choices

- **Rex** (Scots burr) — no pure Scots voice in the 34-voice library. Book 1 memory rule says pack-bond translations ride in Nate's voice channel anyway. All Rex passages routed to Nate voice.
- **Judge** (Australian female) — no Aussie female in library (Charlie is Aussie male). Same treatment: routed to Nate voice.
- **Congressman** — bull, no dialogue.

Both resolvable on a later pass via ElevenLabs' custom-voice cloning or a wider library pull.

## Swapping a voice

1. Open `scripts/cast.json`, change the `voice_id` for the role.
2. Delete cached paragraph MP3s that used the old voice:
   `rm .cache/segments/<voice_key>-*.mp3`
3. Delete the routing cache for the chapter if the voice_key mapping itself moved: `rm .cache/routing/<chapter>-*.json`
4. Re-run: `python scripts/audiobook_builder.py --chapter ../chXX-*.md`

Unchanged paragraphs won't be re-synthesized — cache by text + voice + settings hash.

## Verifying a pick before committing

1. Edit the line for a character in `scripts/generate_samples.py`.
2. Run: `python scripts/generate_samples.py`
3. Open `voice-samples/<voice_key>-sample.mp3`.
