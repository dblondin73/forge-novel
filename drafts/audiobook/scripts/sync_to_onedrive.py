"""
sync_to_onedrive.py — Copy produced chapter MP3s from the repo to OneDrive.

OneDrive target: C:\\Users\\dblon\\OneDrive\\Music\\ForgeNovel\\Book01\\

Run after audiobook_builder.py finishes each chapter (or at the end).
"""

from __future__ import annotations

import shutil
from pathlib import Path

SOURCE = Path(r"C:\Workbench\dev\forge-novel\drafts\audiobook\chapters")
TARGET = Path(r"C:\Users\dblon\OneDrive\Music\ForgeNovel\Book01")
SAMPLES_SOURCE = Path(r"C:\Workbench\dev\forge-novel\drafts\audiobook\voice-samples")
SAMPLES_TARGET = TARGET / "voice-samples"


def mirror(src_dir: Path, dst_dir: Path) -> int:
    dst_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src in sorted(src_dir.glob("*.mp3")):
        dst = dst_dir / src.name
        if dst.exists() and dst.stat().st_size == src.stat().st_size:
            continue
        shutil.copy2(src, dst)
        copied += 1
        print(f"[sync] {src.name} -> {dst}")
    return copied


def main() -> None:
    c = mirror(SOURCE, TARGET)
    s = mirror(SAMPLES_SOURCE, SAMPLES_TARGET)
    print(f"\nDone. {c} chapter(s) and {s} sample(s) copied to OneDrive.")


if __name__ == "__main__":
    main()
