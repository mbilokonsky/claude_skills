---
name: custom-tarot-designer
description: Design thematically coherent custom tarot decks by identifying dialectics, creating suits through dialectic cross-products, developing archetypal stories for Major Arcana, and projecting abstract narrative frameworks through suits for Minor Arcana. Includes interactive viewer with p5.js visual generation, customizable reading prompts, dynamic spread configuration, and redesigned card browser with badge-style UI (v6.0). Use this skill when the user requests a custom tarot deck based on a specific theme (e.g., "Design a cyberpunk tarot deck" or "Create tarot for the theme of ocean mythology").
---

# Custom Tarot Designer v6.1

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
- **Description**: A detailed paragraph explaining what this theme encompasses, its key qualities, and what makes it compelling
- **Salient Concepts** (optional): 3-6 specific aspects of the theme that are most interesting or important for this deck

**Example for "Cyberpunk":**
```
Name: "Cyberpunk"
Description: "A near-future dystopian aesthetic exploring the intersection of high technology and societal breakdown. Cyberpunk examines how digital enhancement, corporate power, and street-level survival create new forms of humanity, identity, and resistance. It asks what we gain and lose when technology becomes inseparable from consciousness itself."
Salient Concepts: ["digital consciousness", "corporate control", "body modification", "information as currency", "street-level resistance", "technological inequality"]
```

This rich foundation will inform suit generation and Major Arcana story development.

#### 1b: Identifying Dialectics

Given the articulated theme, identify 4-6 possible dialectics that capture important dimensions of tension. Present these as individual axes, not as pre-paired combinations.

**Dialectic Structure:**
- **Thesis**: First pole (e.g., "Individual")
- **Antithesis**: Opposing pole (e.g., "Collective")
- **Tensions** (optional): 2-4 ways this dialectic specifically informs the chosen theme

**Dialectic selection criteria:**
- Each pole should represent a genuine axis of tension or difference within the theme
- Dialectics should cover different facets of the theme
- When combined in pairs, they should suggest natural, distinct quadrants

**Example for "Cyberpunk" theme:**

Possible dialectics:
1. **Individual ⟷ Collective**
   - Tensions: ["personal agency vs social systems", "lone hacker vs networked collectives", "identity vs assimilation"]

2. **Technology ⟷ Human**
   - Tensions: ["enhancement vs authenticity", "digital vs organic", "upgraded vs obsolete"]

3. **Control ⟷ Chaos**
   - Tensions: ["corporate order vs street anarchy", "planned obsolescence vs improvised survival", "surveillance vs freedom"]

4. **Flesh ⟷ Digital**
   - Tensions: ["physical body vs uploaded consciousness", "meat space vs cyberspace", "mortality vs transcendence"]

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
   - Think of traditional tarot suits or playing card suits: instantly recognizable from a flat shape
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
4. **Tags (3-6)**: Core meanings, themes, and concepts associated with this suit
5. **Inverted Tags (3-6)**: Chiral reflections or subtle antitheses of the suit meanings - not simple negations, but the shadow side, excess, or misdirected form of the suit's energy
6. **Visual Style**: Description of the aesthetic approach for cards in this suit (color palette, imagery style, compositional approach)

**Example for "Individual+Technology" in Cyberpunk:**
- Name: "Programs" or "Code" or "Daemons"
- Symbol: "A circuit node with radiating connections"
- Symbol SVG: `<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="12" fill="#667eea"/><line x1="50" y1="38" x2="50" y2="20" stroke="#667eea" stroke-width="4"/><line x1="62" y1="50" x2="80" y2="50" stroke="#667eea" stroke-width="4"/><line x1="50" y1="62" x2="50" y2="80" stroke="#667eea" stroke-width="4"/><line x1="38" y1="50" x2="20" y2="50" stroke="#667eea" stroke-width="4"/><circle cx="50" cy="20" r="4" fill="#667eea"/><circle cx="80" cy="50" r="4" fill="#667eea"/><circle cx="50" cy="80" r="4" fill="#667eea"/><circle cx="20" cy="50" r="4" fill="#667eea"/></svg>`
- Tags: ["individual agency", "technical mastery", "digital tools", "personal power", "crafted solutions"]
- Inverted Tags: ["isolated expertise", "over-optimization", "technical tunnel vision", "tools become chains", "solution seeking problems"]
- Visual Style: "Neon wireframe aesthetics on dark backgrounds; close-up views of interfaces and code; angular, precise compositions"


### Stage 3: Developing Major Arcana

The Major Arcana is structured around an archetypal story that serves as the thematic equivalent of the Fool's Journey. This stage has three substages:

#### 3a: Creating the Story

Develop an archetypal narrative that:
- Reflects the central themes and tensions of the deck's theme
- Spans enough narrative territory to support 22 distinct aspects/cards
- Makes evenly distributed use (directly or indirectly) of all four suits
- Follows a recognizable pattern rather than a completely novel structure

The story should be archetypal—not unique or surprising, but rather a canonical or emblematic version of narratives within this theme. Think of it as the "Hero's Journey" of this particular domain.

**Structural guidance:**
- Consider a three-act structure (similar to traditional tarot: Awareness → Integration → Transcendence)
- Identify key moments, turning points, characters, settings, and states of being
- Ensure the story has sufficient texture to generate 22 meaningfully distinct aspects

Be sure to present the story to the user and request feedback before proceeding to 3b. Allow revision of plot points, character roles, or thematic emphasis.

#### 3b: Identifying Visual Style

Determine the visual style for Major Arcana cards. This may be:
- A synthesis of the four suit styles
- A distinct style that encompasses all suits
- Something that specifically emphasizes the story's narrative qualities

Describe the style in terms of compositional approach, color theory, symbolic density, and overall aesthetic direction. Note that this visual style string may be encountered in isolation from the suit style strings, so don't reference suits - instead, if you choose to draw from suit styles, be explicit about the actual integrated style.

#### 3c: Defining the 22 Aspects

Step through the story sequentially to identify 22 distinct aspects that will become the Major Arcana cards, numbered 0-21. Each aspect should:

- Represent a specific moment, character, state, setting, or turning point in the story
- Have its own thematic weight beyond just advancing the plot
- Specify a `role` (e.g., "protagonist", "threshold", "crisis moment", "setting", "antagonist force")
- Include 3-6 `tags` that capture the card's meanings and themes
- Include 3-6 `inverted_tags` representing chiral reflections or subtle antitheses - the shadow side, excess, or misdirection of the upright meaning
- Include a descriptive `name`

Present the 22 aspects to the user for feedback. Allow reordering, renaming, or thematic adjustment.

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
- **Tags (3-6)**: Abstract themes and meanings at this stage
- **Inverted Tags (3-6)**: Chiral reflections or subtle antitheses of this stage
- **Visual content description**: Abstract imagery that represents this phase (e.g., "two paths diverging" or "a structure under construction")
- **Role**: Brief description of what narrative function this rank serves (e.g., "initiation", "choice point", "first manifestation")

Present the ten numbered ranks to the user for feedback.

#### 4b: Projecting Numbered Ranks Through Suits

For each of the 40 numbered minor arcana cards (4 suits × 10 ranks), generate:

1. **Tags**: Either merge the suit and rank tags, or create integrated tags that specifically describe how this rank manifests through this suit
2. **Inverted Tags**: Either merge the suit and rank inverted tags, or create integrated inverted tags specific to this combination
3. **Image content**: Combine the rank's abstract visual content with the suit's specific aesthetic and thematic context

**Example: Five of Programs (Suit: Programs, Rank: Five = "Glitch/Conflict")**
- Rank tags: ["conflict", "instability", "challenge"]
- Suit tags: ["individual agency", "technical mastery", "code"]
- Integrated tags: ["debugging crisis", "breaking changes", "system vulnerability", "technical debt"]
- Image: "Cascading error messages in neon red against the suit's typical dark wireframe background; fractured code syntax"

This substage typically does not require explicit user review unless they request it, as the framework has already been approved.

#### 4c: Defining Face Ranks (11-14)

Identify four face ranks that represent archetypal characters or roles within the Major Arcana story. These should:
- Progress according to some meaningful semantic structure (hierarchy, cycle, composition, etc.)
- Each represent a distinct character archetype or role that could be filled by different individuals
- NOT simply copy traditional Page/Knight/Queen/King unless that structure genuinely fits the theme

For each face rank, define:
- **Name**: What this rank is called (e.g., "Novice", "Agent", "Architect", "System")
- **Tags (3-6)**: Meanings and characteristics of this archetype
- **Inverted Tags (3-6)**: Chiral reflections or subtle antitheses of this archetype
- **Visual content description**: How this rank typically appears in imagery
- **Role**: What narrative function or character type this represents

The progression from rank 11 to 14 should itself encode meaning. Consider:
- Traditional hierarchy: Student → Warrior → Nurturing Ruler → Commanding Ruler
- Cyclical: Spring → Summer → Autumn → Winter
- Compositional: Element → Compound → Mixture → Synthesis
- Developmental: Observation → Experimentation → Integration → Mastery

Present the four face ranks and their progression logic to the user for feedback.

#### 4d: Projecting Face Ranks Through Suits

As with numbered ranks, generate each of the 16 face cards (4 suits × 4 face ranks) by combining:
- Face rank tags + suit tags → integrated card tags
- Face rank inverted tags + suit inverted tags → integrated card inverted tags
- Face rank visual content + suit visual style → card imagery description

This substage typically does not require explicit user review unless requested.

### Stage 5: Generating Final JSON

After all stages are complete and approved, generate the complete deck as a JSON object conforming to the optimized schema defined in:

```bash
view references/schema.md
```

The optimized schema minimizes duplication for context efficiency:
- Major arcana cards are embedded directly in `major_arcana.cards` (no separate aspects array)
- Major arcana visual style is stored once at `major_arcana.visual_style` (not repeated in each card)
- Minor arcana cards reference suits and ranks by index (no duplication of definitions)
- Every card has a computed name:
  - Major: Uses aspect name (e.g., "The Summoning")
  - Minor numbered: "Ace of [Suit]", "Two of [Suit]", etc.
  - Minor face: "[Face Name] of [Suit]" (e.g., "The Visitor of Gifts")

The JSON should include:
- Theme and dialectics
- All Major Arcana data (story, visual style, 22 cards with names)
- All Minor Arcana data (4 suits, numbered ranks 1-10, face ranks 11-14, 56 cards)

**CRITICAL: Save the JSON to outputs directory**
```bash
# Save deck JSON to outputs with descriptive filename
cat > /mnt/user-data/outputs/[theme-name]-deck.json << 'EOF'
[paste the complete JSON here]
EOF
```

Present the file path to the user and confirm the save was successful. They may request revisions to specific elements, which can be made by editing the JSON file directly.

### Stage 6: Creating the Deck Viewer Artifact

After the JSON is complete and saved to outputs, use the CLI merge tool to combine the deck with the viewer template.

**Merge deck with template using CLI:**

```bash
cd /mnt/skills/user/custom-tarot-designer
python3 merge_deck.py /mnt/user-data/outputs/[theme-name]-deck.json
```

This tool will:
1. Load your deck JSON
2. Load the TarotDeckViewer.jsx template
3. Replace the `$$REPLACE_ME_WITH_JSON$$` placeholder with your deck data
4. Save the merged file to `/mnt/user-data/outputs/DeckViewer.jsx`

**Create the artifact:**

Once merged, create a React artifact from the output file:

```bash
view /mnt/user-data/outputs/DeckViewer.jsx
```

Then create the artifact from this complete component.

**Visual Generation Workflow:**

1. User browses cards and clicks "Generate Visual" on any card
2. Component calls Claude API with card data and theme context
3. Claude generates a custom p5.js sketch (abstract, animated, thematic)
4. Visual saves to localStorage automatically (key: `tarot-visuals-{theme-name}`)
5. Visual appears in Card Browser and Readings views
6. User can click "Download Backup" to export all visuals as DeckVisualsLoader.jsx
7. To restore: upload .jsx file, ask Claude to convert to artifact, open it to auto-load visuals

**CLI Tool Reference:**

The `merge_deck.py` tool accepts these arguments:
```
python3 merge_deck.py <deck.json> [output_dir]

Arguments:
  deck.json    - Path to the deck JSON file
  output_dir   - Output directory (default: /mnt/user-data/outputs)
```

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
- **Tag diversity**: Do cards within the same suit/rank family have meaningful variation?

## References and Assets

This skill includes reference documents and template assets:

**References:**
- `references/tarot_structure.md`: Detailed breakdown of traditional tarot structure, including dialectics, suits, the Fool's Journey, numbered rank abstractions, and face card hierarchies
- `references/schema.md`: Optimized TypeScript interface definitions for the final JSON output format (minimizes duplication for context efficiency)

**Assets:**
- `assets/TarotDeckViewer.jsx`: Unified React component for deck viewing and readings (5 integrated views)
