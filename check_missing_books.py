#!/usr/bin/env python3

# Standard 66 books of the Bible
standard_books = [
    # Old Testament (39 books)
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    
    # New Testament (27 books)
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
]

import os

def check_missing_books():
    # Get existing books from both directories
    bible_books = set(os.listdir("bible_books"))
    genz_books = set(os.listdir("genz_bible"))
    
    print("=== BIBLE TRANSLATION COMPLETENESS CHECK ===\n")
    
    print(f"Standard Bible books: {len(standard_books)}")
    print(f"Books in bible_books/: {len(bible_books)}")
    print(f"Books in genz_bible/: {len(genz_books)}")
    
    print("\n=== MISSING BOOKS ANALYSIS ===")
    
    # Check what's in standard but not in our directories
    missing_from_bible_books = set(standard_books) - bible_books
    missing_from_genz = set(standard_books) - genz_books
    
    if missing_from_bible_books:
        print(f"\nMissing from bible_books/ ({len(missing_from_bible_books)}):")
        for book in sorted(missing_from_bible_books):
            print(f"  - {book}")
    
    if missing_from_genz:
        print(f"\nMissing from genz_bible/ ({len(missing_from_genz)}):")
        for book in sorted(missing_from_genz):
            print(f"  - {book}")
    
    # Check what's in our directories but not standard
    extra_in_bible_books = bible_books - set(standard_books)
    extra_in_genz = genz_books - set(standard_books)
    
    if extra_in_bible_books:
        print(f"\nExtra in bible_books/ ({len(extra_in_bible_books)}):")
        for book in sorted(extra_in_bible_books):
            print(f"  - {book}")
    
    if extra_in_genz:
        print(f"\nExtra in genz_bible/ ({len(extra_in_genz)}):")
        for book in sorted(extra_in_genz):
            print(f"  - {book}")
    
    # Check chapter counts
    print("\n=== CHAPTER COUNT ANALYSIS ===")
    total_bible_chapters = 0
    total_genz_chapters = 0
    
    for book in sorted(bible_books):
        bible_chapters = len([f for f in os.listdir(f"bible_books/{book}") if f.endswith('.txt')])
        genz_chapters = len([f for f in os.listdir(f"genz_bible/{book}") if f.endswith('.txt')])
        
        total_bible_chapters += bible_chapters
        total_genz_chapters += genz_chapters
        
        if bible_chapters != genz_chapters:
            print(f"  {book}: {bible_chapters} vs {genz_chapters} chapters")
    
    print(f"\nTotal chapters in bible_books/: {total_bible_chapters}")
    print(f"Total chapters in genz_bible/: {total_genz_chapters}")
    
    if total_bible_chapters == total_genz_chapters:
        print("✅ All chapters have been translated!")
    else:
        print("❌ Some chapters are missing translations")

if __name__ == "__main__":
    check_missing_books()