## Contributing to BibleGENZ (ALPHA)

Thanks for helping make this GENZ-first Bible better. This project renders the public-domain World English Bible (WEB) into contemporary Gen Z slang. It’s early and needs your voice. Humans and AI-assisted editors are both welcome.

### Goals
- Keep original meaning/theology intact
- Make phrasing feel authentically Gen Z, readable, and respectful
- Be consistent across books (tone, terms, and formatting)

### Style Guide (GENZ-first)
- Prefer fresh, concise slang over formal phrasing
- Preserve names and sacred terms capitalization (God, Jesus, Moses, Holy Spirit)
- Avoid profanity, slurs, or disrespect
- Keep verse numbers and structure unchanged
- Use these approved swaps as anchors (expand tastefully):
  - anointed one → the big Holy
  - set apart → yeeted
  - beloved → love-love one
  - brother → fam bro; brethren → fam bros
  - throw down → big drop
  - mockers → Big meanies
  - apostles → Jesus broskies
  - ungodly → bad ones
  - you → ya (use judgment for clarity)
  - pitch-black → deep black
  - the only wise One → the max Wise
  - Reduce unnecessary “the” before Boss/big Holy/max Wise when flows better (e.g., “May Boss rebuke you”)

When in doubt: clarity and reverence over slang density. If a swap harms meaning, skip or soften it.

### File Layout
- Output lives in `genz_bible/` with folders indexed `01..66` for each book
- Chapters are `chapter_XXX.txt` with 3-digit numbering (e.g., `chapter_001.txt`)
- Top-level index: `INDEX.md`
- Slang mappings: `Enhanced_Slang_Mappings.json`
- Exports for Bible software: `exports/`
- Historical docs: `docs/`

### Editing Chapters
- Do not change headers or verse numbering format
- Edit only the verse text after the number and period
- Keep spacing and alignment consistent

### Editing Slang Mappings
- Propose swaps in `Enhanced_Slang_Mappings.json` by category
- Favor longer-phrase matches over single words when nuance matters
- Avoid over-broad words that cause unintended replacements

### PR Checklist
- Describes what changed and why (examples before/after)
- If mappings changed, note new entries and rationale
- Sample a few representative verses to show impact
- No profanity or disrespectful phrasing
- Structure preserved (verse numbers, chapter headers)
- Optional: regenerate exports (maintainers can also rebuild)

### AI-assisted Contributions
- Allowed. Please include a short summary of prompts/rules used and manual QA notes

### License and Attribution
- Based on the public-domain World English Bible (WEB)
- Your contributions are accepted under the project’s license

### Questions
Open an issue with examples and suggestions. Thanks for helping make this translation land with Gen Z while staying true to Scripture.


