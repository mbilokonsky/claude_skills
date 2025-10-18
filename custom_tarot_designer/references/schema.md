# Custom Tarot Deck Schema

This document defines the TypeScript interfaces for the final JSON output of a custom tarot deck design.

## Optimized Schema (Avoids Duplication)

```typescript
// Core theme definition
interface Theme {
  name: string; // Simple canonical name (used in deck naming)
  description: string; // Detailed summary of the theme
  salient_concepts?: string[]; // Key aspects most interesting for this deck
}

// Dialectical structure for suit generation
interface Dialectic {
  thesis: string; // First pole of the dialectic
  antithesis: string; // Opposing pole
  tensions?: string[]; // How this dialectic informs the theme
}

interface Suit {
  name: string;
  symbol: string; // simple description suitable for SVG rendering
  symbol_svg?: string; // optional: pre-generated SVG code for the symbol
  tags: string[]; // core meanings of this suit
  inverted_tags: string[]; // chiral reflections / subtle antitheses of the suit meanings
  visual_style: string; // aesthetic approach for this suit's cards
}

interface MajorAspect {
  number: number; // 0-21
  name: string; // e.g., "The Summoning"
  role: string; // e.g., "Threshold/Beginning"
  tags: string[]; // meanings/themes for this card
  inverted_tags: string[]; // chiral reflections / subtle antitheses when card is inverted
  image_content: string; // specific visual content for this card
}

interface Rank {
  number: number;
  role: string;
  tags: string[]; // abstract meanings for this rank
  inverted_tags: string[]; // chiral reflections / subtle antitheses when rank is inverted
  image_content: string; // abstract visual description
}

interface MinorRank extends Rank {
  number: number; // 1-10
}

interface FaceRank extends Rank {
  number: number; // 11-14
  name: string; // e.g., "The Visitor"
}

interface MinorCard {
  suit_index: number; // index into minor_arcana.suits array (0-3)
  rank_index: number; // index into minor_arcana.ranks array (0-13)
  name: string; // computed: "Ace of Gifts", "Three of Boons", "The Visitor of Tricks"
  tags: string[]; // integrated from suit + rank
  inverted_tags: string[]; // integrated inverted meanings
  image_content: string; // combination of rank's content + suit's context
}

interface CustomTarotDeck {
  theme: Theme;
  dialectics: [Dialectic, Dialectic];
  
  major_arcana: {
    story: string;
    visual_style: string; // shared by all major arcana cards
    cards: MajorAspect[]; // 22 cards (0-21) - these ARE the cards, no separate array needed
  };
  
  minor_arcana: {
    suits: [Suit, Suit, Suit, Suit]; // 4 suits
    ranks: {
      numbered: MinorRank[]; // 10 ranks (1-10)
      face: FaceRank[]; // 4 ranks (11-14)
    };
    cards: MinorCard[]; // 56 cards - references suits and ranks by index
  };
}
```

## Schema Usage Guidelines

### Naming Conventions

**For numbered ranks (1-10):**
- Rank 1 → "Ace"
- Ranks 2-10 → "Two", "Three", "Four", etc.
- Pattern: `"${rankName} of ${suit.name}"`

**For face ranks (11-14):**
- Use the rank's name property
- Pattern: `"${rank.name} of ${suit.name}"`

**For major arcana:**
- Use the aspect's name property directly

### Tag Integration for Minor Cards

When creating minor_arcana.cards, integrate suit and rank tags:

**Option 1 - Merge:** Simply concatenate
- Suit: ["technology", "individual agency"]
- Rank: ["conflict", "challenge"]
- Result: ["technology", "individual agency", "conflict", "challenge"]

**Option 2 - Integrate:** Create specific interpretations
- Suit: ["technology", "individual agency", "code"]
- Rank 5: ["conflict", "challenge", "instability"]
- Result: ["debugging crisis", "system vulnerability", "breaking changes"]

### Inverted Tags Philosophy

Inverted tags represent **chiral reflections** or **subtle antitheses** rather than simple negations. Think of them as the shadow side, the excess, the misdirection, or the perverted form of the upright meaning.

**Examples of good inverted tags:**
- Upright: "growth", "expansion", "abundance" → Inverted: "overextension", "waste", "excess without purpose"
- Upright: "clarity", "truth", "revelation" → Inverted: "blinding certainty", "harsh truth", "revelation without compassion"
- Upright: "community", "connection", "togetherness" → Inverted: "loss of self", "enmeshment", "forced conformity"

**Not good inverted tags (too simple/negative):**
- Upright: "growth" → Inverted: "no growth", "stagnation" (too simple)
- Upright: "truth" → Inverted: "lies", "deception" (too binary)
- Upright: "love" → Inverted: "hate" (opposite, not chiral reflection)

The inverted meaning should feel like the same energy turned destructive, excessive, blocked, or misdirected - not simply its absence or opposite.

### Image Content for Minor Cards

Combine rank's abstract image_content with suit's image_style:
- Rank: "Two figures facing each other, moment of mutual acknowledgment"
- Suit (Gifts): "Warm golden light, smooth rounded forms"
- Result: "Two spirits in golden light, one extending a star-shaped gift toward a seeker, smooth harmonious composition"

### Accessing Cards

To access a specific card:

**Major Arcana:**
```typescript
const card = deck.major_arcana.cards[cardNumber]; // 0-21
const visualStyle = deck.major_arcana.visual_style;
```

**Minor Arcana:**
```typescript
const card = deck.minor_arcana.cards[cardIndex]; // 0-55
const suit = deck.minor_arcana.suits[card.suit_index];
const rank = card.rank_index < 10 
  ? deck.minor_arcana.ranks.numbered[card.rank_index]
  : deck.minor_arcana.ranks.face[card.rank_index - 10];
const visualStyle = suit.visual_style;
```

### Card Indexing for Spreads

For a flat 0-77 indexing system:
- 0-21: Major Arcana (direct index into major_arcana.cards)
- 22-77: Minor Arcana (index - 22 into minor_arcana.cards)

This makes random card selection simple while maintaining the optimized storage structure.
