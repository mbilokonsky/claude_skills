---
name: custom-tarot-designer
description: Design thematically coherent custom tarot decks by identifying dialectics, creating suits through dialectic cross-products, developing archetypal stories for Major Arcana, and projecting abstract narrative frameworks through suits for Minor Arcana. Use this skill when the user requests a custom tarot deck based on a specific theme (e.g., "Design a cyberpunk tarot deck" or "Create tarot for the theme of ocean mythology"). This tool generates a large JSON file representing a completed deck.
---

# Custom Tarot Designer v7

## Overview

This skill guides the creation of structurally sound, thematically rich custom tarot decks. It maintains the 78-card structure of traditional tarot while reimagining dialectics, suits, Major Arcana story, and Minor Arcana meanings to fit any given theme. The process is collaborative and iterative, with user feedback solicited at each major stage.

## Design Philosophy

Custom tarot design is fundamentally about **structural transposition**: taking the deep architecture of traditional tarot and mapping it onto new thematic territory. The goal is not novelty for its own sake, but rather archetypal resonance—creating decks where the structure amplifies the theme and the theme illuminates the structure.

Key principles:

- **Dialectics drive coherence**: The two dialectics should capture maximum semantic surface area of the theme
- **Suits emerge from structure**: Suits are the natural cross-product of dialectics, interpreted through thematic lens
- **Story before cards**: The Major Arcana story should be archetypal and structurally support 22 aspects
- **Abstraction enables projection**: Minor Arcana ranks represent abstract frameworks that refract through suits
- **Creative judgment over rigid rules**: Theme needs should guide decisions; these are guidelines, not constraints

## Workflow

The design process follows five sequential stages, each building on the previous:

### Stage 1: Theme and Dialectics

Begin by reading the traditional tarot reference to understand how dialectics function:

```bash
view references/tarot_structure.md
```

#### 1a: Defining the Theme

Work with the user to articulate their theme with depth and specificity:

**Theme Structure:**
- **Name**: A simple, canonical name (e.g., "Cyberpunk", "Ocean Mythology", "Creative Process")
- **Description**: A detailed description explaining what this theme encompasses, its key qualities, and how it's intended to be used for the purposes of deck generation.

**Example for "Cyberpunk":**
```
Name: "Cyberpunk"
Description: "A near-future dystopian aesthetic exploring the intersection of high technology and societal breakdown. Cyberpunk examines how digital enhancement, corporate power, and street-level survival create new forms of humanity, identity, and resistance. It asks what we gain and lose when technology becomes inseparable from consciousness itself, inspiring cards that allow the querent to bring to bear an implicit interrogation of power dynamics, structural conflicts and productive tensions in whatever subject they're asking about"
```

This rich foundation will inform suit generation and Major Arcana story development.

#### 1b: Identifying Dialectics

Given the articulated theme, identify 4-6 possible dialectics that capture important dimensions of tension. Present these as individual axes, not as pre-paired combinations.

**Dialectic Structure:**
- **Thesis**: First pole (e.g., "Individual")
- **Antithesis**: Opposing pole (e.g., "Collective")
- **Context**: How specifically does this dialectic relate to the theme? How might it inform a tarot deck?

**Dialectic selection criteria:**
- Each dialectic should represent a genuine axis of tension or difference within the theme
- Dialectics should cover different facets of the theme
- When combined in pairs, they should suggest natural, distinct quadrants

**Example for "Cyberpunk" theme:**

Possible dialectics:
1. **Individual ⟷ Collective**
   - Tensions: "This dialectic explores concepts like personal agency vs social systems, which manifest in symbols like the lone hacker vs networked corporation. It might inspire a deck that asks us to consider the tensions between part and whole."

2. **Technology ⟷ Human**
   - Tensions: "At the core of cyberpunk literature is a sort of complex tension between humanity and technology - are these poles in irreconcilable conflict, or is integration possible? What does authenticity mean when technological enhancement is the norm? How might we think about the value of things that can be upgraded vs those which can't?"

3. **Control ⟷ Chaos**
   - Tensions: "Cyperpunk settings often include a backdrop where corporations and/or governments exert unilateral control over the infrastructure required for existence within society, and yet the protagonists frequently find clever if dangerous ways to subvert that control. This dialectic asks us to consider what can be controlled, and in what ways? It also invites speculation as to who gets to define chaos."

4. **Flesh ⟷ Digital**
   - Tensions: "A more visceral take on the Technology/Human dialectic, this asks us to consider the organic vs the digital directly. This dialectic is more concerned with embodiment, substrate and ontology."

After presenting options with their tensions, optionally suggest particularly generative combinations (e.g., "Individual/Collective + Technology/Human would create suits around personal tech, social tech, personal humanity, and communal humanity"), but allow the user to choose any two dialectics or propose their own.

The **tensions** will be particularly useful when:
- Generating suit meanings (each suit embodies specific tensions)
- Developing the Major Arcana story (narrative can explore these tensions)
- Creating card interpretations (tensions suggest reading depth)

Finalize two dialectics before proceeding.

### Stage 2: Creating Suits

Using the finalized dialectics, create four suits by taking the cross-product of the dialectic poles. Each suit represents one quadrant of the two-dimensional space defined by the dialectics.

For each suit, develop:

1. **Name**: Creative interpretation of the dialectic combination, reflecting the theme
2. **Symbol**: Brief description of a visual symbol that represents the suit
   - **CRITICAL**: Symbols must be simple, iconic shapes that can be rendered as clean vector graphics (SVG)
   - Consider how traditional tarot or playing card suits are instantly recognizable from a flat shape
   - Avoid: complex scenes, detailed illustrations, or anything requiring fine detail
3. **Symbol SVG**: Generate clean SVG code based on the symbol description and store in the `symbol_svg` field
   - Use simple paths and shapes
   - ViewBox should be "0 0 100 100" for consistency
   - **CRITICAL VISIBILITY REQUIREMENTS**:
     - **TRANSPARENCY VIA SVG MASKS ONLY**: Use SVG `<mask>` elements for cut-outs (eye holes, etc.), NOT white fills or multiple colors
       - Good: `<mask id="m"><rect fill="currentColor"/><circle fill="currentColor"/></mask>` applied to main shape
       - Bad: Using `fill="#fff"` for "holes" - these become solid white when symbol is recolored
     - **NO PARTIAL OPACITY**: Avoid opacity values between 0.1-0.9 on symbol elements
       - Partial opacity creates muddy, unclear symbols at small sizes
     - **SIZE CONSISTENCY & BALANCE**: All four suit symbols must be roughly balanced. Achieve this by ensuring that each image takes up the full ViewBox either in terms of height or in terms of width, or ideally both depending on the shape. If either dimension is not full, center the image within the view box on whatever axis has room.
     - **SHAPE DISTINCTIVENESS**: Symbols must be clearly different from each other at a glance
       - Each suit should have a distinctly different form language
       - Test: viewing at 16px, can you instantly identify which suit each symbol represents?
     - **BOLD WITH PERSONALITY**: Symbols should be both recognizable AND expressive
       - Favor thematic interpretations over generic geometric shapes
       - Use bold strokes (5px+) and filled shapes for visibility
       - Each symbol should feel like it belongs to its thematic concept
       - Think "icon" not "illustration" - simple but meaningful
     - **STROKE WIDTH**: If using strokes, use stroke-width of 4-5 minimum for primary elements
   - **DESIGN APPROACH**:
     - Think "playing card suit icon" or "road sign" - instant recognition from silhouette alone
     - A good test: if you blur your eyes, can you still identify the shape?
     - Prefer 1-3 distinct elements maximum (e.g., a circle with a triangle inside, not 10 small details)
     - Negative space should be used deliberately, not accidentally created by thin gaps
     - If combining shapes, ensure clear separation (minimum 5-8 units between elements)
   - Keep file size small (< 500 bytes typically)
4. **Meaning**:
  a. **Upright**: Consider what this suit *means* in the context of the theme and from the standpoint of a tarot deck. We're not trying to reduce the suit down to a specific thing, but rather to create a generative space by identifying 3-6 general "meanings" that this suit may represent.
  b. **Inverted**: Chiral reflections or subtle antitheses of the suit meanings - not simple negations, but the shadow side, excess, or misdirected form of the suit's energy. Come up with 3-6 inverted meanings.
6. **Visual Style**: Description of the aesthetic approach for cards in this suit. This should be a reflection of the identity of the suit within the context of the theme.
  a. **Details**: Be specific, and identify things like colors, perspective, any associated art movement, compositional approach, etc. All cards within this suit will have their imagery generated using this style.
  b. **Intra-Suit Coherence**: Consider the ways in which each suit may or may not represent a coherent set when compared to the other three. Some decks may have suit visuals that vary in small specific ways but remain otherwise similar; other decks may have suit styles that vary wildly, challenging the idea of a coherent identity. Play with this tension as you consider this.

**Example for "Individual+Technology" in Cyberpunk:**
- Name: "Programs"
- Symbol: "A circuit node with radiating connections"
- Symbol SVG: '<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><!-- Central node --><circle cx="50" cy="50" r="8" fill="currentColor"/><!-- Radiating connection lines --><line x1="50" y1="50" x2="50" y2="15" stroke="currentColor" stroke-width="3"/><line x1="50" y1="50" x2="85" y2="50" stroke="currentColor" stroke-width="3"/><line x1="50" y1="50" x2="50" y2="85" stroke="currentColor" stroke-width="3"/><line x1="50" y1="50" x2="15" y2="50" stroke="currentColor" stroke-width="3"/><!-- Diagonal connections --><line x1="50" y1="50" x2="75" y2="25" stroke="currentColor" stroke-width="3"/><line x1="50" y1="50" x2="75" y2="75" stroke="currentColor" stroke-width="3"/><line x1="50" y1="50" x2="25" y2="75" stroke="currentColor" stroke-width="3"/><line x1="50" y1="50" x2="25" y2="25" stroke="currentColor" stroke-width="3"/><!-- Endpoint nodes --><circle cx="50" cy="15" r="4" fill="currentColor"/><circle cx="85" cy="50" r="4" fill="currentColor"/><circle cx="50" cy="85" r="4" fill="currentColor"/><circle cx="15" cy="50" r="4" fill="currentColor"/><circle cx="75" cy="25" r="4" fill="currentColor"/><circle cx="75" cy="75" r="4" fill="currentColor"/><circle cx="25" cy="75" r="4" fill="currentColor"/><circle cx="25" cy="25" r="4" fill="currentColor"/></svg>'
- Upright Meanings: ["individual agency", "technical mastery", "composable specialization", "personal power", "crafted solutions"]
- Inverted Meanings: ["isolated expertise", "over-optimization", "inadequacy to the task", "tools become chains", "solution seeking problems"]
- Visual Style: "Neon wireframes (pink, green, blue, red for errors) over dark backgrounds; close-up views of interfaces; angular, precise compositions"


### Stage 3: Developing Major Arcana

The Major Arcana consists of 22 cards numbered 0-21. These are generated using a structured approach that ensures both narrative coherence and deep archetypal resonance. The Major Arcana itself functions as a sort of suit (defining visual style), while each card functions as its own rank.

#### 3a: Defining the Identities and Primes

The Major Arcana is built from irreducible archetypal energies. Begin by defining these atoms; the remaining cards will be derived from their combinations.

**The Identities (0 and 1):**
- **Card 0** — The additive identity. The void, the precondition, pure potential before differentiation. In traditional tarot, this is The Fool. Define what "nothing yet" or "before the journey" means in this theme.
- **Card 1** — The multiplicative identity. The unit of agency, the first act, the transparent operator that makes all further action possible. In traditional tarot, this is The Magician. Define what "becoming one who acts" means in this theme.

**The Eight Primes (2, 3, 5, 7, 11, 13, 17, 19):**

These are the irreducible archetypal energies of the deck. They cannot be "factored" into simpler components — they simply *are*. Each prime should:
- Represent a fundamental, atomic experience or energy within the theme
- Be capable of meaningful combination with other primes
- Scale meaningfully when raised to powers (especially 2 and 3, which appear in many composites)

Define each prime as an archetype:
- **2** — The first prime. Often represents duality, separation, or the fundamental binary within the theme. This is particularly load-bearing as it appears in many composites (4=2², 6=2×3, 8=2³, 10=2×5, 12=2²×3, 14=2×7, 16=2⁴, 18=2×3², 20=2²×5).
- **3** — The second prime. Often represents synthesis, generativity, or offering. Also heavily load-bearing (6=2×3, 9=3², 12=2²×3, 15=3×5, 18=2×3², 21=3×7).
- **5** — Third prime, appearing in composites 10, 15, 20.
- **7** — Fourth prime, appearing in composites 14, 21.
- **11** — Fifth prime. First prime in Act II. Represents something genuinely new that cannot be built from earlier primes.
- **13** — Sixth prime. Traditionally the Death position. An irreducible transformation.
- **17** — Seventh prime. First prime in Act III. Often represents hope or renewal after the composite-heavy middle journey.
- **19** — Eighth and final prime. Near the end of the journey, an irreducible illumination or clarity.

Present the identities and primes to the user for feedback. These are the foundation — get them right before proceeding.

**Note:** The mathematical structure (prime factorization) is scaffolding for generation. Present cards to the user by their names and meanings, not their numerical properties, unless the user specifically asks about the structure.

#### 3b: Deriving the Composites

Once the primes are defined, derive the eleven composite cards (4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21) by meaningfully combining their prime factors.

**Composite derivation:**
| Card | Factors | Meaning emerges from... |
|------|---------|------------------------|
| 4 | 2² | Prime 2 squared — stabilized, structured, or intensified |
| 6 | 2×3 | Prime 2 × Prime 3 — the combination of these energies |
| 8 | 2³ | Prime 2 cubed — deep mastery or extreme expression |
| 9 | 3² | Prime 3 squared — fulfillment or completion of this energy |
| 10 | 2×5 | Prime 2 × Prime 5 |
| 12 | 2²×3 | Structured Prime 2 × Prime 3 |
| 14 | 2×7 | Prime 2 × Prime 7 |
| 15 | 3×5 | Prime 3 × Prime 5 — often shadow territory |
| 16 | 2⁴ | Prime 2 to the fourth — often excess, collapse, breakthrough |
| 18 | 2×3² | Prime 2 × fulfilled Prime 3 |
| 20 | 2²×5 | Structured Prime 2 × Prime 5 |
| 21 | 3×7 | Prime 3 × Prime 7 — the final card, completion |

For each composite:
1. Consider what it means for these specific primes to combine in this theme
2. Consider what it means for a prime to be squared, cubed, or raised to higher powers
3. Name the card and define its meanings based on this combination

The composites should feel *derived* — like natural consequences of the primes meeting. If a composite doesn't make sense as a combination of its factors, revisit either the composite or the primes it's built from.

#### 3c: Verifying the Narrative Arc

Once all 22 cards are defined, verify that they form a coherent story when read in sequence (0→21). The traditional three-act structure provides useful scaffolding:

- **Act I (0-7)**: Contains four primes (2, 3, 5, 7) — prime-dense. The protagonist encounters fundamental, irreducible experiences.
- **Act II (8-14)**: Contains two primes (11, 13) — composite-heavy. The earlier energies combine; complexity emerges. The few primes that appear represent genuinely new, unfactorable experiences.
- **Act III (15-21)**: Contains two primes (17, 19) — composite-heavy. Culmination through combination, with late primes offering transcendent irreducibility.

The arc should feel like a journey where you encounter atoms early, experience their combinations in the middle, and reach synthesis at the end.

Present the complete 22-card sequence to the user. Allow reordering or renaming if the narrative doesn't flow, but note that changes to primes will cascade to their composite derivatives.

#### 3d: Identifying Visual Style

From the standpoint of `visual_style`, the major arcana functions as a sort of suit. Take a look at the visual style guidance from suit generation to figure out how to generate the visual style for the major arcana. If possible and appropriate, consider having the Major Arcana's visual style act as a sort of superset of suit styles — but not if doing so would lead to incoherence, or to a style that's hard to distinguish from the suits.

##### A note on symbols
The Major Arcana may optionally define its own symbol. If you can come up with a symbol that feels appropriate, include one, but this may prove challenging. If you do include one, adhere to the guidance above for suit symbol generation.

#### 3e: Create the Major Arcana cards
For each of the 22 cards, generate the card data. Take a look at the notes at the end of `schema.md` for information on how to integrate the meanings and visual guidance from the rank and the suit (in this case, the major arcana is the suit, and has no meanings of its own).

### Stage 4: Constructing Minor Arcana

The Minor Arcana is created by projecting each of the four suits through each of the 14 ranks (10 numbered ranks, 4 face ranks). It's helpful here to understand how a rank is defined. There are various ways to think about this, but what we want is deep structural interconnectivity such that all cards of rank X have some significant thing in common. There should be a thematic progression upward through the ranks, but there should also be a rich structural paralleax between cards of the same rank through suit space. The way in which ranks relate should generally be thematically-informed, but as a general principle you may consider the following guidance:

1. Numbered ranks (Ace through 10) each represent a specific *question* that is applied to the associated *suit* on a card. You don't have to reuse this list of ranks, but you may, and you may draw inspiration from it:
  - Ace: "Under what conditions does SUIT emerge?"
  - Two: "What is SUIT's relationship to duality?"
  - Three: "In what ways does SUIT relate to systemic complexity?"
  - Four: "What stabilizes SUIT?"
  - Five: "What may emerge from SUIT?"
  - Six: "What threatens SUIT?"
  - Seven: "How does SUIT factionalize or decompose?"
  - Eight: "What is a stable SUIT capable of?"
  - Nine: "What is the Teleology of SUIT?"
  - Ten: "What does it mean for SUIT to complete?"
2. Face Cards work a bit differently. These are intended to represent four archetypes from the major arcana but projected through suit space rather than generalized. Face cards may be hierarchical, rhizomatic, cyclic, distributed - the important thing is that between them you capture some important aspect of the major arcana and show how it applies on a suit-by-suit basis.

This stage has three substages:

#### 4a: Defining Numbered Ranks (1-10)

First, decide on a list of numbered ranks.

**Optional: Prime Scaffolding**

One approach to generating coherent numbered ranks is to use the same prime/composite structure from the Major Arcana, applied more lightly:

- **Ace (1)** = Multiplicative identity — pure suit potential
- **2, 3, 5, 7** = Prime ranks — irreducible questions or energies
- **4 (2²), 6 (2×3), 8 (2³), 9 (3²), 10 (2×5)** = Composite ranks — derived from prime combinations

If using this approach:
1. Define the Ace as pure potential
2. Define the four prime ranks (2, 3, 5, 7) as fundamental, irreducible questions the suit must answer
3. Derive the composite ranks by combining their factors (e.g., 6 = "what happens when the 2-question meets the 3-question?")

This is softer than the Major Arcana constraint — the suits are doing most of the structural work in the Minors, and the ranks provide a secondary axis of meaning. Use this approach if it helps generate coherent progressions, but don't force it if another structure fits the theme better.

**For each numbered rank (1-10), define:**
- **Description**: Name the question this rank asks. Describe the chosen abstraction in general terms that can be broadly applied but which respect the specific narrative role this rank represents.
- **Meaning**: 3-6 upright and 3-6 inverted meanings for this rank. Consider the description, the theme in which we're operating, the nature of the major arcana story and the dialectical tensions we're drawing from to generate a list of creative, generative concepts. See the guidance for generating meaning for suits.
- **Visual content description**: Abstract imagery that represents this phase (e.g., "two paths diverging" or "a structure under construction"). This should be specific enough that a generated visual could be recognized as an instance of this rank, but also general enough that the card itself has room to interpret the guidance through the meaning of the suit and other context.

Present the ten numbered ranks to the user for feedback before advancing to the face cards.

#### 4b: Defining Face Ranks (11-14)

Identify four face ranks that represent archetypal characters or roles within the Major Arcana story. These should:
- Progress according to some meaningful semantic structure (hierarchy, cycle, composition, etc.)
- Each represent a distinct character archetype or role that could be filled by different individuals
- NOT simply copy traditional Page/Knight/Queen/King unless that structure genuinely fits the theme

See `schema.md` to understand the required properties of face ranks. One constraint to keep in mind is that each face rank's name should start with a different letter, because we need to be able to generate an abbreviate symbol (think "K" for "King", "Q" for Queen etc)

*Note*: Due to the way we are structurally echoing and reflecting the same concepts through our little semantic space, it's easy to accidentally reuse terms and concepts. For instance, be careful to ensure that you aren't reusing suit names or cards from the Major Arcana as face card names, etc.

The progression from rank 11 to 14 should itself encode meaning. Consider the wide range of meanings available to you in this step. A non-exhaustive list might include things like:
- Traditional hierarchy: Student → Warrior → Nurturing Ruler → Commanding Ruler
- Cyclical: Spring → Summer → Autumn → Winter
- Compositional: Element → Compound → Mixture → Synthesis
- Developmental: Observation → Experimentation → Integration → Mastery

You should identify some proposed ideas that fit well with the existing concepts in the deck and propose them to the user for feedback.

#### 4c: Projecting Ranks Through Suits

For each of the 40 numbered minor arcana cards (4 suits × 10 ranks) and 16 face cards (4 suits x 4 ranks), generate what's required by `schema.md` here. This document gives you the shape of the required output, as well as describing how to generate meanings and image descriptions by drawing from the rank and suit.

```bash
view references/schema.md
```

### Stage 5: Generating Final JSON

After all stages are complete and approved, generate the complete deck as a JSON object conforming to the schema defined in `schema.md`.

The JSON should include:
- Theme
- Suits (x4)
- Major Arcana (including 22 nested Major Arcana Ranks)
- Minor Ranks (x14)
- Cards (x78)

**CRITICAL: Save the JSON to outputs directory**
```bash
# Save deck JSON to outputs with descriptive filename
cat > /mnt/user-data/outputs/[theme-name]-deck.json << 'EOF'
[paste the complete JSON here]
EOF
```

Present the file path to the user and confirm the save was successful.

### Stage 6: Serve the Deck Loader component
Finally, serve `assets/tarot-deck-loader.jsx` as an interactive artifact and invite the user to upload their finished JSON into that tool. Note: there's no need to copy the source from this component into the chat, no need to manually reassemble it - this wastes time and tokens. Instead just use your existing CLI tools to copy the component as-is into `outputs/` and give the user a reference to click into it.

## Working with Feedback

Throughout the workflow, maintain flexibility:

- Users may want to iterate on any stage before proceeding
- Some users may want to see all options before deciding; others may want to quickly move through
- If a user requests changes to an earlier stage after later stages are complete, be prepared to regenerate dependent content
- Creative judgment should always supersede rigid adherence to structure when the theme demands it

## Quality Checks

While these are guidelines rather than hard rules, consider these quality indicators:

- **Dialectics**: Do they genuinely create four distinct, meaningful quadrants?
- **Suit distribution**: Does the Major Arcana story make reasonably even use of all four suits?
- **Major Arcana**: Can you identify 22 meaningfully distinct aspects without padding?
- **Numbered ranks**: Do they form a coherent abstract progression that could apply to any suit?
- **Face ranks**: Does their progression encode meaning relevant to the theme?
- **Meaning diversity**: Do cards within the same suit/rank family have meaningful variation?

## References and Assets

This skill includes reference documents:

**References:**
- `references/tarot_structure.md`: Detailed breakdown of traditional tarot structure, including dialectics, suits, the Fool's Journey, numbered rank abstractions, and face card hierarchies
- `references/schema.md`: Optimized TypeScript interface definitions for the final JSON output format (minimizes duplication for context efficiency)

This skill includes the following assets:
- `assets/tarot-deck-loader.jsx`: An AI-Powered artifact capable of rendering a deck that conforms to this tool's schema requirements. With this tool the user may view and edit the deck, and can download updated JSON based on the changes they make. Once the deck has been created, this tool is the primary way the user should interact with it.