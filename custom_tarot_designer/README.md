# Custom Tarot Designer v6.0

A skill for designing thematically coherent custom tarot decks with integrated viewer, readings, and visual generation.

## Quick Start

1. **Design your deck** - Follow the guided workflow in `SKILL.md`
2. **Save JSON** - Save your complete deck to `/mnt/user-data/outputs/your-deck.json`
3. **Merge with template** - Run the CLI tool:
   ```bash
   python3 /mnt/skills/user/custom-tarot-designer/merge_deck.py /mnt/user-data/outputs/your-deck.json
   ```
4. **Create artifact** - Create a React artifact from `/mnt/user-data/outputs/DeckViewer.jsx`

## What's New in v6.0

### Template System
- Template no longer contains example deck data
- Uses `$$REPLACE_ME_WITH_JSON$$` placeholder
- CLI tool automates merging deck JSON with template
- Much smaller template size (3230 lines vs 5071)

### Output Directory Policy
- **All generated files go to `/mnt/user-data/outputs/`**
- Skill directory is immutable (templates and tools only)
- Clear separation between framework and user content

### Symbol Design
- New guidelines for monochrome, bold suit symbols
- Optimized for 14-18px rendering in card browser
- "Playing card suit" level of instant recognition

## Directory Structure

```
/mnt/skills/user/custom-tarot-designer/
├── SKILL.md                    # Main skill instructions
├── merge_deck.py               # CLI tool for merging decks
├── CHANGELOG-v6.0.md           # Version history
├── README-v6.0.md              # This file
├── assets/
│   ├── TarotDeckViewer.jsx     # Template (with placeholder)
│   └── [legacy HTML templates]
└── references/
    ├── schema.md               # JSON schema documentation
    └── tarot_structure.md      # Traditional tarot reference

/mnt/user-data/outputs/
├── [your-deck]-deck.json       # Your deck JSON files
├── DeckViewer.jsx              # Merged viewer (ready for artifact)
└── [exported visuals, etc]     # Other generated files
```

## CLI Tool Usage

### Basic Usage
```bash
python3 /mnt/skills/user/custom-tarot-designer/merge_deck.py <deck.json>
```

### With Custom Output Directory
```bash
python3 /mnt/skills/user/custom-tarot-designer/merge_deck.py <deck.json> /path/to/output
```

### Example
```bash
# Merge your deck
python3 /mnt/skills/user/custom-tarot-designer/merge_deck.py /mnt/user-data/outputs/cyberpunk-deck.json

# Output will be at /mnt/user-data/outputs/DeckViewer.jsx
```

## Example Deck

The "Hermes Chosen" deck is available as a reference:
- Location: `/mnt/user-data/outputs/hermes-chosen-deck.json`
- Use it to test the merge tool or as a structural reference

To create an artifact from it:
```bash
python3 /mnt/skills/user/custom-tarot-designer/merge_deck.py /mnt/user-data/outputs/hermes-chosen-deck.json
```

## Viewer Features

The DeckViewer artifact provides:

1. **Deck Summary** - Stats, dialectics, and visual backup management
2. **Major Arcana** - Complete story and all 22 cards
3. **Minor Arcana** - Split-view of suits and ranks
4. **Card Browser** - Searchable master-detail with visual generation
5. **Readings** - Interactive three-card spread with AI interpretations

Additional features:
- p5.js visual generation via Claude API
- localStorage persistence for generated visuals
- Export/import of visual collections
- Fully self-contained (shareable as single .jsx file)

## Workflow Summary

1. **Stage 1**: Define theme and identify dialectics
2. **Stage 2**: Create four suits from dialectic cross-product
3. **Stage 3**: Develop Major Arcana story and 22 cards
4. **Stage 4**: Design Minor Arcana ranks and project through suits
5. **Stage 5**: Generate final JSON → save to `/mnt/user-data/outputs/`
6. **Stage 6**: Merge with template → create artifact

## Support

- Read `SKILL.md` for detailed instructions
- Check `references/schema.md` for JSON structure
- Review `references/tarot_structure.md` for tarot concepts
- See `CHANGELOG-v6.0.md` for migration notes

## Version History

- **v6.0** - Template system redesign, CLI merge tool, output directory policy
- **v5.9** - Badge-style card browser UI
- **v5.7** - Dynamic spread configuration
- **v5.5** - Enhanced visual generation
- **v5.3** - Unified viewer with readings
- **v5.2** - localStorage persistence for visuals
