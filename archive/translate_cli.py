#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from genz_translator import translate_chapter_text, your_ai_enhance, TranslationStyle


def load_mappings(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def translate_book_dir(src_book_dir: Path, dst_book_dir: Path, mappings: dict, style: TranslationStyle) -> None:
    dst_book_dir.mkdir(parents=True, exist_ok=True)
    for chapter_file in sorted(src_book_dir.glob("chapter_*.txt")):
        chapter_text = chapter_file.read_text(encoding="utf-8")
        translated = translate_chapter_text(chapter_text, mappings, lambda t: your_ai_enhance(t, style))
        (dst_book_dir / chapter_file.name).write_text(translated, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Translate bible_books into genz_bible using local rules only.")
    parser.add_argument("--src", type=Path, default=Path("bible_books"), help="Source directory with books/chapters")
    parser.add_argument("--dst", type=Path, default=Path("genz_bible"), help="Destination directory for GENZ output")
    parser.add_argument("--mappings", type=Path, default=Path("Enhanced_Slang_Mappings.json"), help="JSON slang mappings file")
    parser.add_argument("--style", choices=[s.value for s in TranslationStyle], default=TranslationStyle.balanced.value, help="Translation style intensity")

    args = parser.parse_args()

    src: Path = args.src
    dst: Path = args.dst
    style = TranslationStyle(args.style)

    if not src.exists():
        raise SystemExit(f"Source directory not found: {src}")

    dst.mkdir(parents=True, exist_ok=True)
    mappings = load_mappings(args.mappings)

    books = [d for d in src.iterdir() if d.is_dir()]
    for book_dir in sorted(books, key=lambda p: p.name):
        print(f"Translating {book_dir.name}...")
        translate_book_dir(book_dir, dst / book_dir.name, mappings, style)
    print("Done.")


if __name__ == "__main__":
    main()


