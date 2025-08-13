#!/usr/bin/env python3
import re
from enum import Enum


class TranslationStyle(Enum):
    minimal = "minimal"      # only safe swaps
    balanced = "balanced"    # tasteful slang
    extra = "extra"          # more expressive slang


def _smart_case_replacement(original: str, replacement: str, src: str) -> str:
    if original.isupper():
        return replacement.upper()
    if original.istitle():
        return replacement.title()
    return replacement


def your_ai_enhance(text: str, style: TranslationStyle = TranslationStyle.balanced) -> str:
    enhanced = text

    # 1) Light contractions and flow
    enhanced = re.sub(r"\bdo not\b", "don't", enhanced, flags=re.IGNORECASE)
    enhanced = re.sub(r"\bis not\b", "isn't", enhanced, flags=re.IGNORECASE)
    enhanced = re.sub(r"\bare not\b", "aren't", enhanced, flags=re.IGNORECASE)
    enhanced = re.sub(r"\bshall not\b", "won't", enhanced, flags=re.IGNORECASE)
    enhanced = re.sub(r"\bwill not\b", "won't", enhanced, flags=re.IGNORECASE)

    # 2) Tone polish by style
    if style != TranslationStyle.minimal:
        # Add light discourse markers sparingly
        enhanced = re.sub(r"\btruly,?\b", "deadass,", enhanced, flags=re.IGNORECASE)
        enhanced = re.sub(r"\bbehold,?\b", "check this out,", enhanced, flags=re.IGNORECASE)

    if style == TranslationStyle.extra:
        # Emphasizers
        enhanced = re.sub(r"\bverily,?\b", "fr fr,", enhanced, flags=re.IGNORECASE)
        # Replace generic intensifiers
        enhanced = re.sub(r"\bvery\b", "hella", enhanced, flags=re.IGNORECASE)

    # 3) Guard sacred names from accidental slangification
    # Ensure 'Lord' and 'God' capitalization is preserved
    enhanced = re.sub(r"\bthe lord\b", "the Lord", enhanced, flags=re.IGNORECASE)
    enhanced = re.sub(r"\bgod\b", "God", enhanced, flags=re.IGNORECASE)

    # 4) Smooth punctuation spacing
    enhanced = re.sub(r"\s+([,.;:!?])", r"\1", enhanced)
    enhanced = re.sub(r"\s+", " ", enhanced).strip()
    return enhanced


