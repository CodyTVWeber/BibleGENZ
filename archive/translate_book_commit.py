#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Translate one book (all chapters) and commit/push once per book.")
    parser.add_argument("book", help="Book name exactly as directory under bible_books/")
    parser.add_argument("--style", default="extra", choices=["minimal","balanced","extra"], help="Translation intensity")
    args = parser.parse_args()

    src_book_dir = ROOT / "bible_books" / args.book
    dst_book_dir = ROOT / "genz_bible" / args.book
    mappings = ROOT / "Enhanced_Slang_Mappings.json"

    if not src_book_dir.is_dir():
        raise SystemExit(f"Book not found: {src_book_dir}")

    # Translate all chapters in the book
    chapter_files = sorted(src_book_dir.glob("chapter_*.txt"))
    for ch in chapter_files:
        run([
            "python3", str(ROOT / "translate_single.py"), str(ch),
            "--src-root", str(ROOT / "bible_books"),
            "--dst-root", str(ROOT / "genz_bible"),
            "--mappings", str(mappings),
            "--style", args.style,
        ])

    # Stage the whole book, log, commit, push
    run(["git", "add", str(dst_book_dir)])
    with open(ROOT / "translation_progress.log", "a", encoding="utf-8") as logf:
        logf.write(f"BOOK_DONE: {args.book}\n")
    run(["git", "add", str(ROOT / "translation_progress.log")])
    run(["git", "commit", "-m", f"GENZ: translate book {args.book} (GENZ-maxx per mappings)" ])
    run(["git", "push"]) 


if __name__ == "__main__":
    main()


