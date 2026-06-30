# Custom Tarot Designer v6.0

# DEPRECATION NOTICE: this is considered a legacy version of this skill, and is not exported by this plugin. Maintaining for historical context.
For an up-to-date version of this skill with cleaner schema, richer semantics etc, see this [repo](https://github.com/mbilokonsky/generative-arcana) or this [github pages site](https://mbilokonsky.github.io/generative-arcana).


A skill for designing thematically coherent custom tarot decks with integrated viewer, readings, and visual generation.

## Quick Start

1. **Design your deck** - Follow the guided workflow in `SKILL.md`
2. **Save JSON** - Save your complete deck to `/mnt/user-data/outputs/{deck-slug}.json`
3. **Expose Artifact** - Give the user a way to view or download the generated JSON.

## How To Generate Data
This tool will have you generating copious amounts of text data - a full deck generation may well exceed context window and cause crashes. So you should diligently create an initial JSON document with theme information, and then update it by writing new information between each step of the Skill. When generating the cards at the end, checkpoint after the major arcana cards are written and again after each suit's cards are written. **always** make sure that what you are writing confirms to `references/schema.md`, as the skill flow may have you generating ephemeral values that you need to do your work but which do not get persisted (eg the dialectics).

## Directory Structure

```
/mnt/skills/user/custom-tarot-designer/
├── SKILL.md                    # Main skill instructions
├── README.md              # This file
├── assets/
│   └── tarot-deck-loader.jsx   # allows the user to view and edit their deck
└── references/
    ├── schema.md               # JSON schema documentation
    └── tarot_structure.md      # Traditional tarot reference

/mnt/user-data/outputs/
├── [deck-slug].json       # Your deck JSON files
└── [exported visuals, etc]     # Other generated files
```

## Support

- Read `SKILL.md` for detailed instructions
- Check `references/schema.md` for JSON structure
- Review `references/tarot_structure.md` for tarot concepts

