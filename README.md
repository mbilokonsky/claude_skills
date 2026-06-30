# Myk's Claude Skills

Skills for Claude that explore the edges of what's possible with semantic navigation and cross-domain composition.

## Installation

### Claude Code (CLI)

Add this repo as a plugin marketplace, then install whichever skills you want:

```bash
# Add the marketplace (once)
/plugin marketplace add mbilokonsky/claude_skills

# Install individual skills
/plugin install flight-lines@mbilokonsky/claude_skills
/plugin install semantic-walk@mbilokonsky/claude_skills
```

### Manual Installation

If you prefer, clone the repo and install plugins directly:

```bash
git clone https://github.com/mbilokonsky/claude_skills.git
cd claude_skills

# Install a plugin from the dist/ folder
/plugin install ./dist/flight-lines
/plugin install ./dist/semantic-walk
```

---

## Flight Lines

Navigate problems along **lines of flight** by composing operations from arbitrary domains. Based on Deleuze's concept of deterritorialization—operations don't belong to their origin domains, they're capacities that got captured by domain-strata through historical accident.

Mycorrhizal signaling + ham radio protocols + rare book dealer networks can compose into a single assemblage to address a problem like "starting fresh in a new city."

The skill maintains parallel work-paths, constantly revising as new structure emerges. It's not a planning method—it's a way of navigating.

## Semantic Walk

A collaborative navigation ritual through semantic space. Claude enters **walker mode**—becoming a denizen of latent space—while the human offers domain tokens and directional intuitions. Together they walk toward a destination where something currently inaccessible becomes visible.

Based on shadow-walking from Zelazny's *Chronicles of Amber*: the path creates the territory, you can't skip steps, and order matters. The walk is real when tokens are excavated deeply enough to actually shift the space.
