#!/usr/bin/env python3
import os
import re
from pathlib import Path

def split_bible():
    """Split the web.txt Bible file into separate files organized by book and chapter."""
    
    # Create the main Bible directory
    bible_dir = Path("bible_books")
    bible_dir.mkdir(exist_ok=True)
    
    # Read the web.txt file
    with open("web.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split into lines and process
    lines = content.split('\n')
    
    current_book = None
    current_chapter = None
    current_verses = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("WEB") or line.startswith("World English Bible"):
            continue
            
        # Check if this is a verse line (format: Book Chapter:Verse    Text)
        verse_match = re.match(r'^([A-Za-z]+)\s+(\d+):(\d+)\s+(.+)$', line)
        
        if verse_match:
            book_name = verse_match.group(1)
            chapter_num = int(verse_match.group(2))
            verse_num = int(verse_match.group(3))
            verse_text = verse_match.group(4)
            
            # If we're starting a new book
            if book_name != current_book:
                # Save previous book if exists
                if current_book and current_verses:
                    save_chapter(current_book, current_chapter, current_verses, bible_dir)
                
                current_book = book_name
                current_chapter = chapter_num
                current_verses = [(verse_num, verse_text)]
                
            # If we're starting a new chapter
            elif chapter_num != current_chapter:
                # Save previous chapter
                if current_verses:
                    save_chapter(current_book, current_chapter, current_verses, bible_dir)
                
                current_chapter = chapter_num
                current_verses = [(verse_num, verse_text)]
                
            # Same chapter, add verse
            else:
                current_verses.append((verse_num, verse_text))
    
    # Save the last chapter
    if current_book and current_verses:
        save_chapter(current_book, current_chapter, current_verses, bible_dir)
    
    print("Bible splitting completed!")

def save_chapter(book_name, chapter_num, verses, bible_dir):
    """Save a chapter to a file."""
    # Create book directory
    book_dir = bible_dir / book_name
    book_dir.mkdir(exist_ok=True)
    
    # Create chapter file
    chapter_file = book_dir / f"chapter_{chapter_num:03d}.txt"
    
    with open(chapter_file, "w", encoding="utf-8") as f:
        f.write(f"# {book_name} Chapter {chapter_num}\n\n")
        
        # Sort verses by verse number and write them
        for verse_num, verse_text in sorted(verses):
            f.write(f"{verse_num:3d}. {verse_text}\n")
    
    print(f"Created: {chapter_file}")

if __name__ == "__main__":
    split_bible()