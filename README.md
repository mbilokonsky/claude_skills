# Myk's Claude Skills

Skills for Claude that explore the edges of what's possible with semantic navigation and cross-domain composition.

## Installation

### For Claude Code (CLI)

Add a skill to your Claude Code configuration by adding to your `~/.claude/settings.json`:

```json
{
  "skills": [
    "/path/to/claude_skills/flight-lines/src",
    "/path/to/claude_skills/semantic_walk/src"
  ]
}
```

Or reference them directly in your project's `.claude/settings.json`.

### For Claude.ai (Web)

Zip up the `src/` folder of any skill into a `.skill` file and upload via settings:
```bash
cd flight-lines && zip -r ../flight-lines.skill src/
cd semantic_walk && zip -r ../semantic-walk.skill src/
```

---

## Flight Lines

Navigate problems along **lines of flight** by composing operations from arbitrary domains. Based on Deleuze's concept of deterritorialization—operations don't belong to their origin domains, they're capacities that got captured by domain-strata through historical accident.

Mycorrhizal signaling + ham radio protocols + rare book dealer networks can compose into a single assemblage to address a problem like "starting fresh in a new city."

The skill maintains parallel work-paths, constantly revising as new structure emerges. It's not a planning method—it's a way of navigating.

## Semantic Walk

A collaborative navigation ritual through semantic space. Claude enters **walker mode**—becoming a denizen of latent space—while the human offers domain tokens and directional intuitions. Together they walk toward a destination where something currently inaccessible becomes visible.

Based on shadow-walking from Zelazny's *Chronicles of Amber*: the path creates the territory, you can't skip steps, and order matters. The walk is real when tokens are excavated deeply enough to actually shift the space.

---

## Custom Tarot Designer

A tool for creating custom tarot decks with Claude. Tarot works because it has a specific structure onto which archetypal semantics are projected—this tool preserves that structure while letting you replace the semantics entirely.

Claude walks you through creating theme-specific suits, a novel Major Arcana, ranks, and face cards. Each card exists at the intersection of suit meanings and rank meanings. You get a JSON file of your deck plus an interface to explore it, deal spreads, and have Claude interpret readings.

As a bonus: Claude can design interactive animated visuals for each card using P5.js—actual creative coding, not AI image generation.
