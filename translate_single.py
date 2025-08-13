#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from genz_translator import translate_chapter_text, your_ai_enhance, TranslationStyle


def load_mappings(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_dst_path(src_path: Path, src_root: Path, dst_root: Path) -> Path:
    rel = src_path.relative_to(src_root)
    return dst_root / rel


def main():
    parser = argparse.ArgumentParser(description="Translate a single chapter file into GENZ style and write to genz_bible.")
    parser.add_argument("src", type=Path, help="Source chapter file under bible_books/")
    parser.add_argument("--src-root", type=Path, default=Path("bible_books"))
    parser.add_argument("--dst-root", type=Path, default=Path("genz_bible"))
    parser.add_argument("--mappings", type=Path, default=Path("Enhanced_Slang_Mappings.json"))
    parser.add_argument("--style", choices=[s.value for s in TranslationStyle], default=TranslationStyle.extra.value)

    args = parser.parse_args()

    mappings = load_mappings(args.mappings)
    src_text = args.src.read_text(encoding="utf-8")
    style = TranslationStyle(args.style)

    translated = translate_chapter_text(src_text, mappings, lambda t: your_ai_enhance(t, style))

    dst_path = compute_dst_path(args.src, args.src_root, args.dst_root)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(translated, encoding="utf-8")
    print(f"Wrote: {dst_path}")


if __name__ == "__main__":
    main()


