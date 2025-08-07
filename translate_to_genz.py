#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

# Load the enhanced slang mappings
def load_slang_mappings():
    """Load the enhanced slang mappings from JSON file."""
    with open("Enhanced_Slang_Mappings.json", "r", encoding="utf-8") as f:
        return json.load(f)

def translate_verse(verse_text, mappings):
    """Translate a single verse using the slang mappings."""
    translated = verse_text
    
    # Apply spiritual/religious terms
    for original, slang in mappings["Spiritual_Religious_Terms"].items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(original) + r'\b'
        translated = re.sub(pattern, slang, translated, flags=re.IGNORECASE)
    
    # Apply emotional/descriptive terms
    for original, slang in mappings["Emotional_Descriptive_Terms"].items():
        pattern = r'\b' + re.escape(original) + r'\b'
        translated = re.sub(pattern, slang, translated, flags=re.IGNORECASE)
    
    # Apply action terms
    for original, slang in mappings["Action_Terms"].items():
        pattern = r'\b' + re.escape(original) + r'\b'
        translated = re.sub(pattern, slang, translated, flags=re.IGNORECASE)
    
    # Apply modern expressions
    for original, slang in mappings["Modern_Expressions"].items():
        pattern = r'\b' + re.escape(original) + r'\b'
        translated = re.sub(pattern, slang, translated, flags=re.IGNORECASE)
    
    # Apply biblical phrases (longer phrases first)
    for original, slang in sorted(mappings["Biblical_Phrases"].items(), key=len, reverse=True):
        pattern = r'\b' + re.escape(original) + r'\b'
        translated = re.sub(pattern, slang, translated, flags=re.IGNORECASE)
    
    # Additional GenZ transformations
    # "God said" -> "God was like"
    translated = re.sub(r'\bGod said\b', 'God was like', translated, flags=re.IGNORECASE)
    
    # "it was so" -> "that\'s what happened"
    translated = re.sub(r'\bit was so\b', "that's what happened", translated, flags=re.IGNORECASE)
    
    # "In the beginning" -> "At the start"
    translated = re.sub(r'\bIn the beginning\b', 'At the start', translated, flags=re.IGNORECASE)
    
    # "saw" -> "checked out" (when it means "observed")
    translated = re.sub(r'\bsaw\b', 'checked out', translated, flags=re.IGNORECASE)
    
    # "good" -> "fire" (when it means "excellent")
    translated = re.sub(r'\bgood\b', 'fire', translated, flags=re.IGNORECASE)
    
    # "very good" -> "hella fire"
    translated = re.sub(r'\bvery good\b', 'hella fire', translated, flags=re.IGNORECASE)
    
    # "first day" -> "day one"
    translated = re.sub(r'\bfirst day\b', 'day one', translated, flags=re.IGNORECASE)
    
    # "second day" -> "day two"
    translated = re.sub(r'\bsecond day\b', 'day two', translated, flags=re.IGNORECASE)
    
    # "third day" -> "day three"
    translated = re.sub(r'\bthird day\b', 'day three', translated, flags=re.IGNORECASE)
    
    # "fourth day" -> "day four"
    translated = re.sub(r'\bfourth day\b', 'day four', translated, flags=re.IGNORECASE)
    
    # "fifth day" -> "day five"
    translated = re.sub(r'\bfifth day\b', 'day five', translated, flags=re.IGNORECASE)
    
    # "sixth day" -> "day six"
    translated = re.sub(r'\bsixth day\b', 'day six', translated, flags=re.IGNORECASE)
    
    # "seventh day" -> "day seven"
    translated = re.sub(r'\bseventh day\b', 'day seven', translated, flags=re.IGNORECASE)
    
    return translated

def translate_chapter(chapter_file, mappings):
    """Translate a single chapter file."""
    with open(chapter_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split('\n')
    translated_lines = []
    
    for line in lines:
        if line.startswith('#'):
            # Keep the header
            translated_lines.append(line)
        elif line.strip() and re.match(r'^\s*\d+\.', line):
            # This is a verse line
            parts = line.split('.', 1)
            if len(parts) == 2:
                verse_num = parts[0].strip()
                verse_text = parts[1].strip()
                translated_verse = translate_verse(verse_text, mappings)
                translated_lines.append(f"{verse_num:>3}. {translated_verse}")
        else:
            # Keep empty lines or other content
            translated_lines.append(line)
    
    return '\n'.join(translated_lines)

def translate_book(book_dir, mappings):
    """Translate all chapters in a book."""
    book_name = book_dir.name
    print(f"Translating {book_name}...")
    
    # Create GENZ translation directory
    genz_dir = Path("genz_bible") / book_name
    genz_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all chapter files
    chapter_files = sorted(book_dir.glob("chapter_*.txt"))
    
    for chapter_file in chapter_files:
        translated_content = translate_chapter(chapter_file, mappings)
        
        # Save to GENZ directory
        genz_chapter_file = genz_dir / chapter_file.name
        with open(genz_chapter_file, "w", encoding="utf-8") as f:
            f.write(translated_content)
        
        print(f"  Translated {chapter_file.name}")

def main():
    """Main function to translate the entire Bible."""
    print("Loading slang mappings...")
    mappings = load_slang_mappings()
    
    print("Starting Bible translation...")
    
    # Create main GENZ Bible directory
    genz_bible_dir = Path("genz_bible")
    genz_bible_dir.mkdir(exist_ok=True)
    
    # Get all book directories
    bible_books_dir = Path("bible_books")
    book_dirs = sorted([d for d in bible_books_dir.iterdir() if d.is_dir()])
    
    # Translate each book
    for book_dir in book_dirs:
        translate_book(book_dir, mappings)
    
    print("Bible translation completed!")
    print(f"GENZ translations saved in: {genz_bible_dir}")

if __name__ == "__main__":
    main()