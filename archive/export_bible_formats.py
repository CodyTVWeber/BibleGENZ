#!/usr/bin/env python3
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
GENZ = ROOT / "genz_bible"
EXPORTS = ROOT / "exports"


# Base book name -> (OSIS code, eSword abbr)
BOOK_MAP: Dict[str, Tuple[str, str]] = {
    # OT
    "Genesis": ("Gen", "Gen"),
    "Exodus": ("Exod", "Exo"),
    "Leviticus": ("Lev", "Lev"),
    "Numbers": ("Num", "Num"),
    "Deuteronomy": ("Deut", "Deu"),
    "Joshua": ("Josh", "Jos"),
    "Judges": ("Judg", "Jdg"),
    "Ruth": ("Ruth", "Rut"),
    "1 Samuel": ("1Sam", "1Sa"),
    "2 Samuel": ("2Sam", "2Sa"),
    "1 Kings": ("1Kgs", "1Ki"),
    "2 Kings": ("2Kgs", "2Ki"),
    "1 Chronicles": ("1Chr", "1Ch"),
    "2 Chronicles": ("2Chr", "2Ch"),
    "Ezra": ("Ezra", "Ezr"),
    "Nehemiah": ("Neh", "Neh"),
    "Esther": ("Esth", "Est"),
    "Job": ("Job", "Job"),
    "Psalm": ("Ps", "Psa"),  # Folder uses singular; OSIS uses Ps, e-Sword uses Psa
    "Proverbs": ("Prov", "Pro"),
    "Ecclesiastes": ("Eccl", "Ecc"),
    "Song of Solomon": ("Song", "Son"),
    "Isaiah": ("Isa", "Isa"),
    "Jeremiah": ("Jer", "Jer"),
    "Lamentations": ("Lam", "Lam"),
    "Ezekiel": ("Ezek", "Eze"),
    "Daniel": ("Dan", "Dan"),
    "Hosea": ("Hos", "Hos"),
    "Joel": ("Joel", "Joe"),
    "Amos": ("Amos", "Amo"),
    "Obadiah": ("Obad", "Oba"),
    "Jonah": ("Jonah", "Jon"),
    "Micah": ("Mic", "Mic"),
    "Nahum": ("Nah", "Nah"),
    "Habakkuk": ("Hab", "Hab"),
    "Zephaniah": ("Zeph", "Zep"),
    "Haggai": ("Hag", "Hag"),
    "Zechariah": ("Zech", "Zec"),
    "Malachi": ("Mal", "Mal"),
    # NT
    "Matthew": ("Matt", "Mat"),
    "Mark": ("Mark", "Mar"),
    "Luke": ("Luke", "Luk"),
    "John": ("John", "Joh"),
    "Acts": ("Acts", "Act"),
    "Romans": ("Rom", "Rom"),
    "1 Corinthians": ("1Cor", "1Co"),
    "2 Corinthians": ("2Cor", "2Co"),
    "Galatians": ("Gal", "Gal"),
    "Ephesians": ("Eph", "Eph"),
    "Philippians": ("Phil", "Php"),
    "Colossians": ("Col", "Col"),
    "1 Thessalonians": ("1Thess", "1Th"),
    "2 Thessalonians": ("2Thess", "2Th"),
    "1 Timothy": ("1Tim", "1Ti"),
    "2 Timothy": ("2Tim", "2Ti"),
    "Titus": ("Titus", "Tit"),
    "Philemon": ("Phlm", "Phm"),
    "Hebrews": ("Heb", "Heb"),
    "James": ("Jas", "Jas"),
    "1 Peter": ("1Pet", "1Pe"),
    "2 Peter": ("2Pet", "2Pe"),
    "1 John": ("1John", "1Jo"),
    "2 John": ("2John", "2Jo"),
    "3 John": ("3John", "3Jo"),
    "Jude": ("Jude", "Jud"),
    "Revelation": ("Rev", "Rev"),
}


def iter_books() -> List[Path]:
    # Folders are named "NN Book Name"
    books = [p for p in GENZ.iterdir() if p.is_dir()]
    books.sort(key=lambda p: p.name[:2])
    return books


def parse_chapter(file_path: Path) -> List[Tuple[int, str]]:
    verses: List[Tuple[int, str]] = []
    text = file_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
        if m:
            v = int(m.group(1))
            t = m.group(2).strip()
            verses.append((v, t))
    return verses


def export_plaintext():
    EXPORTS.mkdir(parents=True, exist_ok=True)
    out = EXPORTS / "GENZ_Bible_plaintext.txt"
    with out.open("w", encoding="utf-8") as f:
        for book_dir in iter_books():
            base = book_dir.name.split(" ", 1)[1]
            f.write(f"\n\n{book_dir.name}\n")
            for ch in sorted(book_dir.glob("chapter_*.txt")):
                ch_num = int(re.search(r"(\d+)", ch.stem).group(1))
                f.write(f"\n# {base} {ch_num}\n")
                for v, t in parse_chapter(ch):
                    f.write(f"{ch_num}:{v} {t}\n")


def export_esword_imp():
    # SWORD/IMP-like format: "Book Chapter:Verse Text"
    out = EXPORTS / "GENZ_Bible_esword.imp"
    with out.open("w", encoding="utf-8") as f:
        for book_dir in iter_books():
            base = book_dir.name.split(" ", 1)[1]
            osis, esw = BOOK_MAP[base]
            for ch in sorted(book_dir.glob("chapter_*.txt")):
                ch_num = int(re.search(r"(\d+)", ch.stem).group(1))
                for v, t in parse_chapter(ch):
                    f.write(f"{base} {ch_num}:{v} {t}\n")


def _rtf_escape(s: str) -> str:
    return s.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")


def export_esword_rtf():
    # Tooltip Tool NT style tagging: [Abbr 1:1] Verse text
    out = EXPORTS / "GENZ_Bible_esword.rtf"
    lines = [r"{\rtf1\ansi\deff0", r"{\fonttbl{\f0 Arial;}}", r"\fs20"]
    for book_dir in iter_books():
        base = book_dir.name.split(" ", 1)[1]
        osis, esw = BOOK_MAP[base]
        lines.append(_rtf_escape(f"\par {book_dir.name}"))
        for ch in sorted(book_dir.glob("chapter_*.txt")):
            ch_num = int(re.search(r"(\d+)", ch.stem).group(1))
            for v, t in parse_chapter(ch):
                tag = f"[{esw} {ch_num}:{v}]"
                lines.append(_rtf_escape(f"\par {tag} {t}"))
    lines.append("}")
    out.write_text("\n".join(lines), encoding="utf-8")


def export_osis_xml():
    out = EXPORTS / "GENZ_Bible_osis.xml"
    osis = ET.Element("osis")
    osis_text = ET.SubElement(osis, "osisText", attrib={
        "osisIDWork": "GENZ",
        "xml:lang": "en",
    })
    header = ET.SubElement(osis_text, "header")
    work = ET.SubElement(header, "work", attrib={"osisWork": "GENZ"})
    ET.SubElement(work, "title").text = "GENZ Bible (based on WEB)"
    ET.SubElement(work, "identifier").text = "GENZ-WEB"

    for book_dir in iter_books():
        base = book_dir.name.split(" ", 1)[1]
        osis_code, _ = BOOK_MAP[base]
        div = ET.SubElement(osis_text, "div", attrib={"type": "book", "osisID": osis_code})
        ET.SubElement(div, "title").text = base
        for ch in sorted(book_dir.glob("chapter_*.txt")):
            ch_num = int(re.search(r"(\d+)", ch.stem).group(1))
            chap = ET.SubElement(div, "chapter", attrib={"osisID": f"{osis_code}.{ch_num}"})
            for v, t in parse_chapter(ch):
                ET.SubElement(chap, "verse", attrib={"osisID": f"{osis_code}.{ch_num}.{v}"}).text = t

    tree = ET.ElementTree(osis)
    ET.indent(tree, space="  ", level=0)  # Python 3.9+
    tree.write(out, encoding="utf-8", xml_declaration=True)


def main():
    EXPORTS.mkdir(parents=True, exist_ok=True)
    export_plaintext()
    export_esword_imp()
    export_esword_rtf()
    export_osis_xml()
    print(f"Exports written to: {EXPORTS}")


if __name__ == "__main__":
    main()


