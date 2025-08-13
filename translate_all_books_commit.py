#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    books = sorted([d.name for d in (ROOT / "bible_books").iterdir() if d.is_dir()])
    for book in books:
        run(["python3", str(ROOT / "translate_book_commit.py"), book, "--style", "extra"])  # GENZ-maxx


if __name__ == "__main__":
    main()


