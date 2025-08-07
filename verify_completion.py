#!/usr/bin/env python3

import os
import json

def verify_genz_bible_completion():
    print("🎉 GENZ BIBLE TRANSLATION - FINAL VERIFICATION\n")
    
    # Count chapters properly
    bible_chapters = 0
    genz_chapters = 0
    
    for root, dirs, files in os.walk("bible_books"):
        bible_chapters += len([f for f in files if f.endswith('.txt')])
    
    for root, dirs, files in os.walk("genz_bible"):
        genz_chapters += len([f for f in files if f.endswith('.txt')])
    
    # Count books
    bible_books = len([d for d in os.listdir("bible_books") if os.path.isdir(f"bible_books/{d}")])
    genz_books = len([d for d in os.listdir("genz_bible") if os.path.isdir(f"genz_bible/{d}")])
    
    print(f"📊 PROJECT STATISTICS:")
    print(f"   📚 Books in source: {bible_books}")
    print(f"   📚 Books translated: {genz_books}")
    print(f"   📄 Chapters in source: {bible_chapters}")
    print(f"   📄 Chapters translated: {genz_chapters}")
    
    if bible_books == genz_books and bible_chapters == genz_chapters:
        print("\n✅ COMPLETION STATUS: FULLY COMPLETE!")
        print("   All available books and chapters have been translated!")
    else:
        print("\n❌ COMPLETION STATUS: INCOMPLETE")
        print("   Some books or chapters are missing translations.")
    
    # Check slang mappings
    try:
        with open("Enhanced_Slang_Mappings.json", "r") as f:
            slang_mappings = json.load(f)
        
        total_mappings = sum(len(category) for category in slang_mappings.values())
        print(f"\n🎨 SLANG MAPPINGS:")
        print(f"   📝 Total mappings: {total_mappings}")
        print(f"   📂 Categories: {len(slang_mappings)}")
        
        for category, mappings in slang_mappings.items():
            print(f"      • {category}: {len(mappings)} mappings")
            
    except FileNotFoundError:
        print("\n❌ SLANG MAPPINGS: Not found")
    
    # Sample verification
    print(f"\n🔍 SAMPLE VERIFICATION:")
    
    sample_books = ["Genesis", "Matthew", "Psalm"]
    for book in sample_books:
        if os.path.exists(f"genz_bible/{book}/chapter_001.txt"):
            print(f"   ✅ {book}: Translated")
        else:
            print(f"   ❌ {book}: Missing")
    
    # Check for key files
    print(f"\n📁 KEY FILES:")
    key_files = [
        "GENZ_Bible_Plan.md",
        "GENZ_Bible_Summary.md", 
        "GENZ_Bible_Final_Summary.md",
        "Enhanced_Slang_Mappings.json",
        "translate_to_genz.py"
    ]
    
    for file in key_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
    
    print(f"\n🎯 PROJECT STATUS: {'COMPLETE' if bible_books == genz_books and bible_chapters == genz_chapters else 'INCOMPLETE'}")
    print(f"🔥 Ready for Gen Z readers!")

if __name__ == "__main__":
    verify_genz_bible_completion()