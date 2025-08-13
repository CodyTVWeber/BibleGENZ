#!/usr/bin/env python3
import subprocess
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_ROOT = ROOT / "bible_books"
DST_ROOT = ROOT / "genz_bible"
MAPPINGS = ROOT / "Enhanced_Slang_Mappings.json"


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    chapter_paths = sorted(SRC_ROOT.glob("**/chapter_*.txt"))
    for src in chapter_paths:
        # Translate single
        run([
            "python3", str(ROOT / "translate_single.py"), str(src),
            "--src-root", str(SRC_ROOT),
            "--dst-root", str(DST_ROOT),
            "--mappings", str(MAPPINGS),
            "--style", "extra",
        ])

        # Stage, log, commit, push
        dst = DST_ROOT / src.relative_to(SRC_ROOT)
        run(["git", "add", str(dst)])
        with open(ROOT / "translation_progress.log", "a", encoding="utf-8") as logf:
            logf.write(f"{src}\n")
        run(["git", "add", str(ROOT / "translation_progress.log")])
        run(["git", "commit", "-m", f"GENZ: translate {src.relative_to(SRC_ROOT)} (GENZ-maxx)" ] )
        run(["git", "push"]) 


if __name__ == "__main__":
    main()


