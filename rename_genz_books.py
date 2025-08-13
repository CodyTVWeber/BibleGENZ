#!/usr/bin/env python3
from pathlib import Path

# Canonical 66-book order
OLD_TESTAMENT = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
]

NEW_TESTAMENT = [
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation",
]

BOOKS = OLD_TESTAMENT + NEW_TESTAMENT


def main() -> None:
    root = Path(__file__).resolve().parent
    genz = root / "genz_bible"
    # Build mapping for existing -> indexed names
    for idx, book in enumerate(BOOKS, start=1):
        src = genz / book
        if not src.exists():
            continue
        dst = genz / f"{idx:02d} {book}"
        if src == dst:
            continue
        if dst.exists():
            # Already renamed; skip
            continue
        print(f"Renaming {src.name} -> {dst.name}")
        src.rename(dst)


if __name__ == "__main__":
    main()


