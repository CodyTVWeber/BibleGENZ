#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Dict, Mapping


ROOT = Path(__file__).resolve().parents[1]
GENZ = ROOT / "genz_bible"


def load_mappings(path: Path) -> Mapping[str, Dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _apply_category(text: str, mapping: Dict[str, str]) -> str:
    # Longer phrases first to avoid partial clobbering
    for original, slang in sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True):
        pattern = re.compile(r"\b" + re.escape(original) + r"\b", flags=re.IGNORECASE)
        text = pattern.sub(slang, text)
    return text


def apply_mappings_once(text: str, mappings: Mapping[str, Dict[str, str]]) -> str:
    out = text
    # Category order matters
    for cat in [
        "Biblical_Phrases",
        "Spiritual_Religious_Terms",
        "Emotional_Descriptive_Terms",
        "Action_Terms",
        "Modern_Expressions",
    ]:
        if cat in mappings:
            out = _apply_category(out, mappings[cat])

    # Light heuristics (YourAI-lite)
    out = re.sub(r"\bdo not\b", "don't", out, flags=re.IGNORECASE)
    out = re.sub(r"\bis not\b", "isn't", out, flags=re.IGNORECASE)
    out = re.sub(r"\bare not\b", "aren't", out, flags=re.IGNORECASE)
    out = re.sub(r"\bwill not\b|\bshall not\b", "won't", out, flags=re.IGNORECASE)

    # Reduce unnecessary 'the' per house style
    out = re.sub(r"\bthe\s+(Boss|big Holy|max Wise)\b", r"\1", out, flags=re.IGNORECASE)

    # Clean double punctuation/spaces
    out = re.sub(r",,", ",", out)
    out = re.sub(r"\s+([,.;:!?])", r"\1", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def rewrite_chapter(path: Path, mappings: Mapping[str, Dict[str, str]]) -> int:
    original = path.read_text(encoding="utf-8")
    changed = 0
    lines = []
    for line in original.splitlines():
        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if not line or line.startswith('#') or not m:
            lines.append(line)
            continue
        indent, vnum, vtext = m.group(1), m.group(2), m.group(3)
        new_text = apply_mappings_once(vtext, mappings)
        if new_text != vtext:
            changed += 1
        # Keep verse number right-aligned to width 3 like existing files
        num_fmt = f"{int(vnum):3d}."
        lines.append(f"{indent}{num_fmt} {new_text}")
    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def main():
    parser = argparse.ArgumentParser(description="Update existing GENZ chapters in-place using current slang mappings.")
    parser.add_argument("--books", nargs="*", help="Book names (as folder suffix after NN), e.g., 'Jude' 'Romans'. If omitted, update all.")
    parser.add_argument("--mappings", default=str(ROOT / "Enhanced_Slang_Mappings.json"), help="Path to slang mappings JSON")
    args = parser.parse_args()

    mappings = load_mappings(Path(args.mappings))

    # Discover target book folders like "65 Jude"
    book_dirs = [p for p in GENZ.iterdir() if p.is_dir()]
    if args.books:
        wanted = set(args.books)
        book_dirs = [p for p in book_dirs if p.name.split(" ", 1)[1] in wanted]

    total_changed = 0
    for bd in sorted(book_dirs, key=lambda p: p.name[:2]):
        chapter_files = sorted(bd.glob("chapter_*.txt"))
        book_changed = 0
        for ch in chapter_files:
            book_changed += rewrite_chapter(ch, mappings)
        print(f"{bd.name}: updated {book_changed} verses")
        total_changed += book_changed

    print(f"Total verses updated: {total_changed}")


if __name__ == "__main__":
    main()


