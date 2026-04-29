"""
generate_samples.py — Produce one short sample MP3 per voice in the cast.

Run before producing full chapters so you can vet a voice choice quickly.
"""

from __future__ import annotations

from pathlib import Path

from audiobook_builder import synthesize_paragraph, VOICES, SAMPLES_OUT


SAMPLES = {
    "storyteller_omniscient": (
        "Some mornings arrive carrying more than they show. Most mornings are hiding something — a phone call, a flat tire, the slow realization that you've been out of coffee for two days. "
        "But there are mornings, rare ones, that arrive carrying the weight of what comes after them the way a river carries a flood — quietly, from a long way off, with no particular interest in whether you're ready."
    ),
    "storyteller_narrator": (
        "The water pump was dying — slowly, loudly, and at the worst possible time. "
        "Nate crouched beside the wellhead, boots sunk two inches into the sandy clay. Red subsoil showed through where the topsoil had long since washed away. "
        "He pressed his palm flat against the pump housing. Warm, not hot. The difference mattered."
    ),
    "storyteller": (
        "Nothing about it suggested it would be the last normal morning any of them would have. "
        "Steel sky, dew on the bermudagrass, and the quiet patience of a country road that knew something the man on it did not."
    ),
    "nate": (
        "Bearings, not motor. Well, shit. "
        "Twenty-two years of spinning in East Texas humidity — pump doesn't owe me a thing, but I need it to hold till Saturday."
    ),
    "flint": (
        "Well well WELL. Would you look at that. Hostile entities on the board, flag's lit up red-orange-emergency, and your skill bar is, forgive me, embarrassing. "
        "Standby for interpretation — I am going to need a minute with this."
    ),
    "marcus_webb": (
        "Everyone breathes. You with the crossbow — eyes up. Fire lane is that corridor. We hold here until the numbers change. "
        "Nobody dies tonight because they forgot to exhale."
    ),
    "josie_pickett": (
        "Herbs, herbs — that's vervain, that's yarrow, that's something I don't know yet but I'm writing it down. "
        "Hold up. Let me catalog this one."
    ),
    "sam_hargrove": (
        "Brace that door. No — lower. Put your shoulder in it. Good. You got shoulders, use 'em. "
        "Now hold. Don't be polite about it."
    ),
    "ana_torres": (
        "Pressure here. Both hands. Count to ten slow. You're alright — look at my eyes, not at it. "
        "Stay with me. Good. You're doing fine."
    ),
    "walt_keane": (
        "Heat's about right. See the color? That's working steel. "
        "Hammer it while the color holds. You'll feel when it's ready."
    ),
    "pete_bowman": (
        "Trail's fresh. Whatever went through here went through at a run. "
        "Tracks are deep in the heel — it's carrying weight. Give me a minute, I'll tell you what it was."
    ),
    "kyle_greene": (
        "Read the contract? Course I read it. Sort of. Point is — I'm in. "
        "You want the big numbers, you gotta sign the paper."
    ),
    "mack_turner": (
        "Keep your feet quiet. Breath through your nose. "
        "The woods will tell you what's out there if you don't fill 'em up with you."
    ),
    "heather_kim": (
        "Dear Lord, keep my boy safe. Keep him. Please. "
        "I'll do anything. Just keep him."
    ),
    "isabel_wu": (
        "Add it slow — slow — there. See the color change? That's the reaction starting. "
        "Don't stir yet. Let it find itself."
    ),
    "martin_voss": (
        "The philosophical implications are, of course, staggering. "
        "But we have a cohort to shepherd and a graduation floor to walk — so perhaps later."
    ),
    "tyler_sorensen": (
        "I got him. I got him! Did you see that? Seventeen meters, dead center. "
        "I got him."
    ),
    "unknown_male": (
        "First floor's clear. I think. You want me to check it again?"
    ),
    "unknown_female": (
        "Over here — I need a hand. Gently. Gently, I said."
    ),
}


def main() -> None:
    for voice_key, text in SAMPLES.items():
        if voice_key not in VOICES:
            print(f"[skip] {voice_key} not in cast")
            continue
        print(f"[sample] {voice_key}: {VOICES[voice_key]['library_name']}")
        mp3 = synthesize_paragraph(text, voice_key)
        out = SAMPLES_OUT / f"{voice_key}-sample.mp3"
        out.write_bytes(mp3.read_bytes())
    print(f"\nSamples written to {SAMPLES_OUT}")


if __name__ == "__main__":
    main()
