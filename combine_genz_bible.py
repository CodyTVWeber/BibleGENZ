#!/usr/bin/env python3
import os
from pathlib import Path

def combine_genz_bible():
    """Combine all translated chapters into a single GENZ Bible file."""
    
    genz_bible_dir = Path("genz_bible")
    output_file = "GENZ_Bible_Complete.txt"
    
    # Bible book order (standard order)
    old_testament_books = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "Samuel", "Kings", "Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
        "Ecclesiastes", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
        "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah",
        "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"
    ]
    
    new_testament_books = [
        "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
        "Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
        "Thessalonians", "Timothy", "Titus", "Philemon", "Hebrews",
        "James", "Peter", "John", "Jude", "Revelation"
    ]
    
    # Get actual book directories
    actual_books = sorted([d.name for d in genz_bible_dir.iterdir() if d.is_dir()])
    
    print("Creating complete GENZ Bible...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write("THE GENZ BIBLE TRANSLATION\n")
        f.write("Making the Bible lit for the new generation\n")
        f.write("=" * 80 + "\n\n")
        
        # Write Old Testament
        f.write("OLD TESTAMENT\n")
        f.write("=" * 50 + "\n\n")
        
        for book in actual_books:
            if book in ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
                       "Joshua", "Judges", "Ruth", "Samuel", "Kings", "Chronicles",
                       "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
                       "Ecclesiastes", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
                       "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah",
                       "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"]:
                
                book_dir = genz_bible_dir / book
                chapter_files = sorted(book_dir.glob("chapter_*.txt"))
                
                if chapter_files:
                    f.write(f"\n{book.upper()}\n")
                    f.write("-" * len(book) + "\n\n")
                    
                    for chapter_file in chapter_files:
                        with open(chapter_file, "r", encoding="utf-8") as cf:
                            content = cf.read()
                            f.write(content)
                            f.write("\n")
        
        # Write New Testament
        f.write("\n" + "=" * 80 + "\n")
        f.write("NEW TESTAMENT\n")
        f.write("=" * 50 + "\n\n")
        
        for book in actual_books:
            if book in ["Matthew", "Mark", "Luke", "John", "Acts", "Romans",
                       "Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians",
                       "Thessalonians", "Timothy", "Titus", "Philemon", "Hebrews",
                       "James", "Peter", "John", "Jude", "Revelation"]:
                
                book_dir = genz_bible_dir / book
                chapter_files = sorted(book_dir.glob("chapter_*.txt"))
                
                if chapter_files:
                    f.write(f"\n{book.upper()}\n")
                    f.write("-" * len(book) + "\n\n")
                    
                    for chapter_file in chapter_files:
                        with open(chapter_file, "r", encoding="utf-8") as cf:
                            content = cf.read()
                            f.write(content)
                            f.write("\n")
        
        # Write footer
        f.write("\n" + "=" * 80 + "\n")
        f.write("GENZ BIBLE TRANSLATION COMPLETE\n")
        f.write("=" * 80 + "\n")
        f.write("Translation completed using contemporary GenZ slang\n")
        f.write("while maintaining biblical accuracy and theological integrity.\n")
        f.write("=" * 80 + "\n")
    
    print(f"Complete GENZ Bible saved as: {output_file}")

if __name__ == "__main__":
    combine_genz_bible()