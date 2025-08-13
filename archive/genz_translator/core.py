#!/usr/bin/env python3
import re
from typing import Dict, Mapping


def _compile_phrase_pattern(phrase: str) -> re.Pattern:
    # Word-boundary matching that tolerates capitalization
    return re.compile(r"\b" + re.escape(phrase) + r"\b", flags=re.IGNORECASE)


def apply_slang_mappings(text: str, mappings: Mapping[str, Dict[str, str]]) -> str:
    translated = text

    # Preserve replacement order for multi-word phrases first
    def apply_category(category: Dict[str, str]) -> None:
        nonlocal translated
        # Sort by length descending to replace longer phrases first
        items = sorted(category.items(), key=lambda kv: len(kv[0]), reverse=True)
        for original, slang in items:
            translated = _compile_phrase_pattern(original).sub(slang, translated)

    # Categories we expect in Enhanced_Slang_Mappings.json
    for cat_name in [
        "Biblical_Phrases",
        "Spiritual_Religious_Terms",
        "Emotional_Descriptive_Terms",
        "Action_Terms",
        "Modern_Expressions",
    ]:
        if cat_name in mappings:
            apply_category(mappings[cat_name])

    # Lightweight normalizations
    translated = re.sub(r"\s+", " ", translated).strip()
    return translated


def translate_chapter_text(chapter_text: str, mappings: Mapping[str, Dict[str, str]], enhancer) -> str:
    lines = chapter_text.split("\n")
    out_lines = []
    for line in lines:
        if not line:
            out_lines.append(line)
            continue

        if line.startswith('#'):
            out_lines.append(line)
            continue

        if re.match(r"^\s*\d+\.\s", line):
            # Keep verse number and dot alignment
            num, rest = line.split('.', 1)
            verse_text = rest.strip()

            # YourAI: heuristic enhancer, then apply mappings
            enhanced = enhancer(verse_text)
            mapped = apply_slang_mappings(enhanced, mappings)
            out_lines.append(f"{int(num):3d}. {mapped}")
        else:
            out_lines.append(line)
    return "\n".join(out_lines)


