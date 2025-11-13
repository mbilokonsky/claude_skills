# Custom Tarot Deck Schema

This document defines the TypeScript interfaces for the final JSON output of a custom tarot deck design.

## Optimized Schema (Avoids Duplication)

```typescript
interface Theme {
  name: string // what's a concise name for this theme?
  description: string // what is the theme doing? How is it being used for the purposes of this deck?
  creator: string // ask the user how they'd like to be identified
}

enum Arcana {
  Major = "major",
  Minor = "minor"
}

interface MajorArcana {
  story: string
  visual_style: string
  symbol?: {
    name: string
    description: string
    svg: string
  }
}

interface Suit {
  name: string
  slug: string // convert suit name to lowercase, use hyphens for spaces
  description: string
  symbol: {
    name: string
    description: string
    svg: string
  }
  meaning: {
    upright: string[]
    inverted: string[]
  }
  visual_style: string
}

interface Rank {
  index: number // 0-based
  arcana: Arcana
  numeric_value: number // 1-14 for minor, 0-21 for major
  name: string // "Ace", or "Two" through "Ten", or full name for face cards and major arcana
  symbol: string
  slug: string // should just be a string of the index
  description: string
  meaning: {
    upright: string[]
    inverted: string[]
  }
  visual_content: string
}

// MinorRanks are 1:4 with Minor Arcana cards, one per suit
interface MinorRank extends Rank {
  arcana: Arcana.Minor
  symbol: string // e.g. "A", "II", ..., "X", first letter of face card names
}

interface MajorRank extends Rank {
  arcana: Arcana.Major
  symbol: string // "0" through "XXI"
}

interface Card {
  name: string
  number: string // rank_slug for major, rank_slug + 1 for minor cards
  slug: string
  arcana: Arcana
  description: string
  meaning: {
    upright: string
    inverted: string
  }
  visuals: {
    instructions: {
      style_guidance: string
      content_guidance: string
      detailed_description: string
    },
    url?: string
    svg?: string
    code?: string
    image_data?: {
      base64: string
      mime_type: string
    }
  }
}

interface MinorArcanaCard extends Card {
  type: "minor"
  rank_slug: string
  suit_slug: string
  slug: string // `${suit_slug}-${rank_slug}`
}

interface MajorArcanaCard extends Card {
  type: "major"
  rank_slug: string
  slug: string //  `major-${rank.slug}`
}

interface Deck {
  name: string
  slug: string // convert deck name to lowercase, use hyphens for spaces
  version: string // semver?
  theme: Theme
  suits: { // four suits should be here, no more no less
    [suit_slug: string]: Suit
  }
  ranks: { // 14 minor ranks should be here, ordered 0 to 13
    [rank_slug: string]: MinorRank
  }
  major_arcana: MajorArcana  
  cards: {
    // 22 major arcana cards first, then minor by suit and ordered by rank ascending within suit
    [card_slug: string]: MinorArcanaCard | MajorArcanaCard
  }
}
```

## Schema Usage Guidelines

### Deck
The name of the deck should be derived from or equal to the name of the theme, but appended with "Tarot". So if the theme is "Cyber Punk" the Deck would be "Cyber Punk Tarot" and the slug would be "cyber-punk-tarot". The version may be used to track iterative versions of the same deck, but need not be added to the slug.

### Theme
This is the initial starting point for deck creation. The user will supply a theme, and you should ensure that you understand the user's general intent with respect to how the theme should be applied to the new deck. The description should be evocative enough to sustain the rest of the generative process, but need not be particularly long if the chosen theme has enough cultural associations to work with.

### Suits
Follow the skill instructions for deriving suits from the theme. Suit names should prefer single terms, though may be a bit longer. Symbols should follow skill guidance. Be sure to properly escape symbol svg.

### Ranks
Note how the `Rank` interface is really intended to be used as if `abstract`, you should always be thinking in terms of `MajorRank` or `MinorRank` when creating it.

### Major Arcana
The Major Arcana is reasonably complex, and this schema should capture the details used by the skill to derive the values.

### Cards
A Card exists at the intersection of a `Suit` and `Rank` for minor arcana, and as a specific point within the Major Arcana's sequence for major arcana. The "description" field is intended as a semantic rather than a visual property, though some reference to the visual may in some cases be appropriate.

### Naming Conventions

**For numbered ranks (1-10):**
- Rank 1 → "Ace"
- Ranks 2-10 → "Two", "Three", "Four", etc.

**For face ranks (11-14):**
- Use the rank's name property
- Do not preface with "the"

**For major arcana:**
- Use the aspect's name directly

### Meaning Integration for Cards
When creating minor arcana cards, integrate suit and rank meanings using the following strategy:
1. First concatenate `suit.meaning.upright` with `rank.meaning.upright`
2. Then synthesize a new set of meanings by considering the way that the newly generated set of meanings relate. Your final output should be a detailed description that may be used by a reader to interpret the meaning of the card within a spread.
3. Repeat the same process for `suit.meanings.inverted` and `rank.meanings.inverted` in order to create `card.meaning.inverted`.

### Inverted Meanings Philosophy

Inverted meanings represent **chiral reflections** or **subtle antitheses** rather than simple negations. Think of them as the shadow side, the excess, the misdirection, or the perverted form of the upright meaning.

**Examples of good inverted meanings:**
- Upright: "growth", "expansion", "abundance" → Inverted: "overextension", "waste", "excess without purpose"
- Upright: "clarity", "truth", "revelation" → Inverted: "blinding certainty", "harsh truth", "revelation without compassion"
- Upright: "community", "connection", "togetherness" → Inverted: "loss of self", "enmeshment", "forced conformity"

**Not good inverted meanings (too simple/negative):**
- Upright: "growth" → Inverted: "no growth", "stagnation" (too simple)
- Upright: "truth" → Inverted: "lies", "deception" (too binary)
- Upright: "love" → Inverted: "hate" (opposite, not chiral reflection)

The inverted meaning should feel like the same energy turned destructive, excessive, blocked, or misdirected - not simply its absence or opposite.

### Card Visuals

Each card has both a rank and either a suit or the major arcana. In this framework, the rank describes what the visual depicts via `visual_content` while the suit/major arcana describes the color, style and general vibes of the image using `visual_style`.

Your task is to define, for each card, values for `style_guidance`, `content_guidance` and `visual_description`. `style_guidance` is derived from the suit, and *may* simply be a transposition of `visual_style` but consider whether there are specific ways that the suit's instructions may be refined for *this specific card*. Similarly, the rank provides `visual_content` but you may consider refining it with additional specificity in the context of *this specific card*. Finally, `visual_description` should be considered as an input prompt to an image generator - algorithmic or human - such that if they implement what's described the result will share a recognizable style with the suit, recognizable content with the rank, and unique meaning specific to the card in question.

You may disregard the optional fields in the card visual, those will be populated outside of this skill's flow.
