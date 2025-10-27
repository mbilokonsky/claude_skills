---
name: custom-tarot-designer
description: Design thematically coherent custom tarot decks by identifying dialectics, creating suits through dialectic cross-products, developing archetypal stories for Major Arcana, and projecting abstract narrative frameworks through suits for Minor Arcana. Use this skill when the user requests a custom tarot deck based on a specific theme (e.g., "Design a cyberpunk tarot deck" or "Create tarot for the theme of ocean mythology"). This tool generates a large JSON file representing a completed deck.
---

# Custom Tarot Designer v7

## Overview

This skill guides the creation of structurally sound, thematically rich custom tarot decks. It maintains the 78-card structure of traditional tarot while reimagining dialectics, suits, Major Arcana story, and Minor Arcana meanings to fit any given theme. The process is collaborative and iterative, with user feedback solicited at each major stage.

**CRITICAL: Output Directory Policy**
- ALL generated files (JSON decks, merged viewers, exports) MUST be written to `/mnt/user-data/outputs/`
- NEVER modify files in `/mnt/skills/user/custom-tarot-designer/` unless explicitly instructed
- The skill directory contains immutable templates and tools
- The outputs directory is the user's workspace for all generated content

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
- Each pole should represent a genuine axis of tension or difference within the theme
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
       - Good: `<mask id="m"><rect fill="white"/><circle fill="black"/></mask>` applied to main shape
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
- Symbol SVG: '<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><!-- Central node --><circle cx="50" cy="50" r="8" fill="black"/><!-- Radiating connection lines --><line x1="50" y1="50" x2="50" y2="15" stroke="black" stroke-width="3"/><line x1="50" y1="50" x2="85" y2="50" stroke="black" stroke-width="3"/><line x1="50" y1="50" x2="50" y2="85" stroke="black" stroke-width="3"/><line x1="50" y1="50" x2="15" y2="50" stroke="black" stroke-width="3"/><!-- Diagonal connections --><line x1="50" y1="50" x2="75" y2="25" stroke="black" stroke-width="3"/><line x1="50" y1="50" x2="75" y2="75" stroke="black" stroke-width="3"/><line x1="50" y1="50" x2="25" y2="75" stroke="black" stroke-width="3"/><line x1="50" y1="50" x2="25" y2="25" stroke="black" stroke-width="3"/><!-- Endpoint nodes --><circle cx="50" cy="15" r="4" fill="black"/><circle cx="85" cy="50" r="4" fill="black"/><circle cx="50" cy="85" r="4" fill="black"/><circle cx="15" cy="50" r="4" fill="black"/><circle cx="75" cy="25" r="4" fill="black"/><circle cx="75" cy="75" r="4" fill="black"/><circle cx="25" cy="75" r="4" fill="black"/><circle cx="25" cy="25" r="4" fill="black"/></svg>'
- Upright Meanings: ["individual agency", "technical mastery", "composable specialization", "personal power", "crafted solutions"]
- Inverted Meanings: ["isolated expertise", "over-optimization", "inadequacy to the task", "tools become chains", "solution seeking problems"]
- Visual Style: "Neon wireframes (pink, green, blue, red for errors) over dark backgrounds; close-up views of interfaces; angular, precise compositions"


### Stage 3: Developing Major Arcana

The Major Arcana is structured around an archetypal story that serves as the thematic equivalent of the Fool's Journey. The Major Arcana itself functions as a sort of suit for Major Arcana cards, and thus defines visual style, but each card within the Arcana functions as its own Rank.

#### 3a: Creating the Story

Develop an archetypal narrative that:
- Reflects the central concepts and tensions of the deck's theme
- Spans enough narrative territory to support 22 distinct aspects/cards
- Makes evenly distributed use (directly or indirectly) of all four suits
- Follows a recognizable pattern rather than a completely novel structure

The story should be archetypal—not unique or surprising, but rather a canonical or emblematic version of narratives within this theme. Think of it as the "Hero's Journey" of this particular domain.

**Structural guidance:**
- Consider a three-act structure (similar to traditional tarot: Awareness → Integration → Transcendence), but also consider tuning or replacing that based on the needs of the theme and the emergent properties of the chosen dialectics and suits.
- Identify key moments, turning points, characters, settings, and states of being
- Ensure the story has sufficient texture to generate 22 meaningfully distinct aspects

Be sure to present the story to the user and request feedback before proceeding to 3b. Allow revision of plot points, character roles, or thematic emphasis.

#### 3b: Identifying Visual Style

From the standpoint of `visual_style`, the major arcana functions as a sort of suit. Take a look at the visual style guidance from suit generation to figure out how to generate the visual style for the major arcana. If possible and appropriate, consider having the Major Arcana's visual style act as a sort of superset of suit styles - but not if doing so would lead to incoherence, or to a style that's hard to distinguish from the suits.

##### A note on symbols
Note that the Major Arcana may optionally define its own symbol, like any other suit. If you can come up with a symbol that feels appropriate, feel free to include one, but this may prove challenging and so feel free not to. If you do include one, adhere to the guidance above for suit symbol generation.

#### 3c: Defining the 22 Ranks

Step through the story sequentially to identify 22 distinct aspects that will become ranks behind the Major Arcana cards, numbered 0-21. Each aspect should:

- Include a descriptive `name`
- Should define a `description` which identifies which aspect of the story this rank represents
  - This could be a specific moment, character, state, setting, or subplot in the story
  - Have its own thematic weight beyond just advancing the plot
- Identify meanings (upright and inverted) as per rank, but remember that Major Arcana ranks are 1:1 with cards so the meanings you come up with will only be applied once and can be more specific.

Present the 22 ranks to the user for feedback. Allow reordering, renaming, or thematic adjustment.

#### 3d: Create the Major Arcana cards
For each rank of the major arcana, go ahead and generate the card. Take a look at the notes at the end of `schema.md` for information on how to integrate the meanings and visual guidance from the rank and the suit (in this case, the major arcana is the suit, and has no meanings of its own).

### Stage 4: Constructing Minor Arcana

The Minor Arcana is created by projecting abstract narrative frameworks through the four suits. This stage has three substages:

#### 4a: Defining Numbered Ranks (1-10)

First, consult the reference for the traditional numbered rank structure:

```bash
view references/tarot_structure.md
```

Identify ten sequential abstract "steps" or "phases" that capture the underlying structure of the Major Arcana story. These are NOT simply cards 0-9 of the Major Arcana; rather, they are an abstracted, cyclical framework that could be applied to any journey within this theme.

**Examples of abstraction:**
- Traditional tarot: Ace = Pure Potential, Two = Choice, Three = Growth, etc.
- Cyberpunk deck might have: 1 = Connection, 2 = Protocol, 3 = Exploit, 4 = System, 5 = Glitch, etc.

For each numbered rank (1-10), define:
- **Description**: Describe the chosen abstraction in general terms that can be broadly applied but which respect the specific narrative role this rank represents.
- **Meaning**: 3-6 upright and 3-6 inverted meanings for this rank. Consider the description, the theme in which we're operating, the nature of the major arcana story and the dialectical tensions we're drawing from to generate a list of creative, generative concepts. See the guidance for generating meaning for suits.
- **Visual content description**: Abstract imagery that represents this phase (e.g., "two paths diverging" or "a structure under construction"). This should be specific enough that a generated visual could be recognized as an instance of this rank, but also general enough that the card itself has room to interpret the guidance through the meaning of the suit and other context.

Present the ten numbered ranks to the user for feedback before advancing to the face cards.

#### 4b: Defining Face Ranks (11-14)

Identify four face ranks that represent archetypal characters or roles within the Major Arcana story. These should:
- Progress according to some meaningful semantic structure (hierarchy, cycle, composition, etc.)
- Each represent a distinct character archetype or role that could be filled by different individuals
- NOT simply copy traditional Page/Knight/Queen/King unless that structure genuinely fits the theme

See `schema.md` to understand the required properties of face ranks. One constraint to keep in mind is that each face rank's name should start with a different letter, because we need to be able to generate an abbreviate symbol (think "K" for "King", "Q" for Queen etc)

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