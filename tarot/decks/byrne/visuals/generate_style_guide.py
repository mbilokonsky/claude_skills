#!/usr/bin/env python3
"""
Generate visual style guide for the Byrne Journey Tarot

This creates reference images showing:
- Color palette progressions
- Suit-specific palettes
- Example visual elements
- Suit symbols

The output is meant to establish visual identity before card creation.
"""

from PIL import Image, ImageDraw, ImageFont
import byrne_visual_toolkit as bvt
import os

OUTPUT_DIR = '/home/user/claude_skills/tarot/decks/byrne/visuals'


def create_palette_swatch(palette, name, width=400, height=100):
    """Create a visual swatch showing a color palette"""
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Get palette keys in a consistent order
    keys = ['primary', 'secondary', 'accent', 'highlight', 'shadow', 'ground']
    available_keys = [k for k in keys if k in palette]

    # Add any extra keys not in the standard list
    for k in palette:
        if k not in available_keys:
            available_keys.append(k)

    swatch_width = width // len(available_keys)

    for i, key in enumerate(available_keys):
        x = i * swatch_width
        color = palette[key]
        draw.rectangle([x, 0, x + swatch_width, height - 30], fill=color)

        # Label
        label = key
        # Simple text positioning (PIL font handling can be tricky)
        text_x = x + swatch_width // 2 - len(label) * 3
        draw.text((text_x, height - 20), label, fill=(0, 0, 0))

    # Title at bottom
    draw.text((10, height - 20), name, fill=(0, 0, 0))

    return img


def generate_major_arcana_progression():
    """Show the color progression across major arcana"""
    # Create a gradient showing all 22 cards
    width = 1100
    height = 200
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    card_width = width // 22

    for i in range(22):
        palette = bvt.MajorArcanaColors.interpolate_palette(i)
        x = i * card_width

        # Draw a column showing this card's palette
        draw.rectangle([x, 30, x + card_width - 2, 70],
                       fill=palette['primary'])
        draw.rectangle([x, 70, x + card_width - 2, 110],
                       fill=palette['secondary'])
        draw.rectangle([x, 110, x + card_width - 2, 150],
                       fill=palette['accent'])

        # Card number
        if i % 3 == 0:  # Label every 3rd card
            draw.text((x + 5, 155), str(i), fill=(0, 0, 0))

    # Title
    draw.text((10, 10), "Major Arcana Color Progression (0-21)", fill=(0, 0, 0))
    draw.text((10, 165), "Cool/Static → Warm/Dynamic", fill=(100, 100, 100))

    return img


def generate_suit_examples():
    """Generate example scenes for each suit"""
    examples = {}

    # STRUCTURES - geometric, architectural
    canvas = bvt.create_canvas(bvt.SuitColors.STRUCTURES['primary'])
    draw = ImageDraw.Draw(canvas)

    # Grid background
    bvt.draw_grid_pattern(draw, (40, 40, bvt.CARD_WIDTH - 40, bvt.CARD_HEIGHT - 40),
                          30, bvt.SuitColors.STRUCTURES['grid'])

    # A simple building
    bvt.example_building(canvas, 80, 100, 120, 200, bvt.SuitColors.STRUCTURES)

    # Frame
    draw.rectangle([20, 20, bvt.CARD_WIDTH - 20, bvt.CARD_HEIGHT - 20],
                   outline=bvt.SuitColors.STRUCTURES['frame'], width=3)

    examples['structures'] = canvas

    # RIVERS - organic, flowing
    canvas = bvt.create_canvas(bvt.SuitColors.RIVERS['primary'])
    draw = ImageDraw.Draw(canvas)

    # Flow patterns
    for i in range(5):
        y_offset = i * 80
        bvt.draw_flow_pattern(draw,
                              (20, 40 + y_offset, bvt.CARD_WIDTH - 20, 80 + y_offset),
                              60 + i * 10, 15 - i * 2,
                              bvt.SuitColors.RIVERS['flow'])

    examples['rivers'] = canvas

    # CURIOSITY - bright, open, conversational
    canvas = bvt.create_canvas(bvt.SuitColors.CURIOSITY['dialogue'])
    draw = ImageDraw.Draw(canvas)

    # Bright optimistic gradient
    for y in range(bvt.CARD_HEIGHT):
        t = y / bvt.CARD_HEIGHT
        r = int(bvt.SuitColors.CURIOSITY['secondary'][0] +
                (bvt.SuitColors.CURIOSITY['primary'][0] - bvt.SuitColors.CURIOSITY['secondary'][0]) * t)
        g = int(bvt.SuitColors.CURIOSITY['secondary'][1] +
                (bvt.SuitColors.CURIOSITY['primary'][1] - bvt.SuitColors.CURIOSITY['secondary'][1]) * t)
        b = int(bvt.SuitColors.CURIOSITY['secondary'][2] +
                (bvt.SuitColors.CURIOSITY['primary'][2] - bvt.SuitColors.CURIOSITY['secondary'][2]) * t)
        draw.line([(0, y), (bvt.CARD_WIDTH, y)], fill=(r, g, b))

    # Some geometric shapes suggesting dialogue/open space
    draw.rectangle([40, 80, 120, 140], fill=bvt.SuitColors.CURIOSITY['accent'])
    draw.rectangle([160, 120, 240, 180], fill=bvt.SuitColors.CURIOSITY['accent'])
    draw.rectangle([80, 200, 200, 260], fill=bvt.SuitColors.CURIOSITY['accent'])

    examples['curiosity'] = canvas

    # DANCE - warm, dynamic, embodied
    canvas = bvt.create_canvas(bvt.SuitColors.DANCE['shadow'])
    draw = ImageDraw.Draw(canvas)

    # Radial energy bursts
    bvt.radial_gradient(draw, bvt.CARD_WIDTH // 2, bvt.CARD_HEIGHT // 2, 180,
                        bvt.SuitColors.DANCE['heat'],
                        bvt.SuitColors.DANCE['shadow'])

    # A figure in motion
    bvt.example_figure_simple(canvas, bvt.CARD_WIDTH // 2, bvt.CARD_HEIGHT - 60,
                              bvt.SuitColors.DANCE, posture='moving', scale=1.2)

    examples['dance'] = canvas

    return examples


def generate_figure_examples():
    """Show figure variations"""
    width = 1000
    height = 420
    img = Image.new('RGB', (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    # Draw title
    draw.text((10, 10), "Figure Examples (showing posture variations)", fill=(0, 0, 0))

    # Show 3 different postures
    postures = ['neutral', 'awkward', 'moving']
    for i, posture in enumerate(postures):
        x = 150 + i * 300

        # Create a small scene
        canvas_section = (x - 100, 50, x + 100, 400)

        # Background
        draw.rectangle(canvas_section, fill=(200, 210, 220))

        # Figure using early palette as example
        bvt.example_figure_simple(img, x, 380, bvt.MajorArcanaColors.EARLY,
                                  posture=posture, scale=1.3)

        # Label
        draw.text((x - 30, 400), posture, fill=(0, 0, 0))

    return img


def main():
    """Generate all style guide images"""
    print("Generating Byrne Journey Tarot Style Guide...")

    # 1. Major Arcana Color Progression
    print("  - Major Arcana color progression...")
    progression = generate_major_arcana_progression()
    progression.save(os.path.join(OUTPUT_DIR, 'major_arcana_progression.png'))

    # 2. Individual era palettes
    print("  - Era palette swatches...")
    early = create_palette_swatch(bvt.MajorArcanaColors.EARLY,
                                  "Early Era (0-7): Cool, Static, Documentary")
    early.save(os.path.join(OUTPUT_DIR, 'palette_early.png'))

    middle = create_palette_swatch(bvt.MajorArcanaColors.MIDDLE,
                                   "Middle Era (8-14): Transition, Discovery")
    middle.save(os.path.join(OUTPUT_DIR, 'palette_middle.png'))

    late = create_palette_swatch(bvt.MajorArcanaColors.LATE,
                                 "Late Era (15-21): Warm, Dynamic, Embodied")
    late.save(os.path.join(OUTPUT_DIR, 'palette_late.png'))

    # 3. Suit palettes
    print("  - Suit palette swatches...")
    structures = create_palette_swatch(bvt.SuitColors.STRUCTURES,
                                       "Structures: Observation, Analysis, Containment")
    structures.save(os.path.join(OUTPUT_DIR, 'palette_structures.png'))

    rivers = create_palette_swatch(bvt.SuitColors.RIVERS,
                                   "Rivers: Cycles, Patterns, Natural Systems")
    rivers.save(os.path.join(OUTPUT_DIR, 'palette_rivers.png'))

    curiosity = create_palette_swatch(bvt.SuitColors.CURIOSITY,
                                      "Curiosity: Inquiry, Dialogue, Civic Engagement")
    curiosity.save(os.path.join(OUTPUT_DIR, 'palette_curiosity.png'))

    dance = create_palette_swatch(bvt.SuitColors.DANCE,
                                  "Dance: Embodied Joy, Movement, Presence")
    dance.save(os.path.join(OUTPUT_DIR, 'palette_dance.png'))

    # 4. Suit example scenes
    print("  - Suit visual examples...")
    suit_examples = generate_suit_examples()
    for suit_name, img in suit_examples.items():
        img.save(os.path.join(OUTPUT_DIR, f'example_{suit_name}.png'))

    # 5. Suit symbols
    print("  - Suit symbols...")
    symbols = {
        'structures': bvt.render_suit_symbol_structures(128),
        'rivers': bvt.render_suit_symbol_rivers(128),
        'curiosity': bvt.render_suit_symbol_curiosity(128),
        'dance': bvt.render_suit_symbol_dance(128),
    }
    for suit_name, img in symbols.items():
        img.save(os.path.join(OUTPUT_DIR, f'symbol_{suit_name}.png'))

    # 6. Figure examples
    print("  - Figure variations...")
    figures = generate_figure_examples()
    figures.save(os.path.join(OUTPUT_DIR, 'figure_examples.png'))

    print("Style guide images generated!")
    print(f"Output directory: {OUTPUT_DIR}")

    # Generate HTML
    print("  - Creating HTML page...")
    generate_html()
    print(f"\nStyle guide complete!")
    print(f"Open: {OUTPUT_DIR}/style_guide.html")


def generate_html():
    """Generate HTML page presenting the style guide"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Byrne Journey Tarot - Visual Style Guide</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
            color: #333;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 0.2em;
            color: #2c3e50;
        }
        h2 {
            font-size: 1.8em;
            margin-top: 2em;
            margin-bottom: 0.5em;
            color: #34495e;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
        }
        h3 {
            font-size: 1.3em;
            margin-top: 1.5em;
            color: #555;
        }
        .intro {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .section {
            background: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin: 20px 0;
            display: block;
        }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }
        .card-item {
            text-align: center;
        }
        .card-item h4 {
            margin-top: 10px;
            color: #555;
        }
        .note {
            background: #fff8dc;
            border-left: 4px solid #f39c12;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .symbols {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
            margin: 30px 0;
        }
        .symbol-item {
            text-align: center;
            flex: 0 1 200px;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <h1>The Byrne Journey Tarot</h1>
    <div class="intro">
        <h2>Visual Style Guide</h2>
        <p>
            This style guide establishes the visual identity for the Byrne Journey Tarot deck.
            It documents color palettes, visual approaches, and reusable elements while allowing
            each card to be uniquely interpreted.
        </p>
        <p>
            <strong>Theme:</strong> David Byrne's evolution from anxious observation (early Talking Heads)
            to embodied joy and civic participation (American Utopia era). The visual language
            progresses from cool/static/geometric to warm/dynamic/organic.
        </p>
    </div>

    <div class="section">
        <h2>Major Arcana: Color Progression</h2>
        <p>
            The Major Arcana (22 cards, numbered 0-21) follows a color journey from cool documentary
            grays and blues to warm, vibrant oranges and reds. This mirrors Byrne's artistic evolution.
        </p>
        <img src="major_arcana_progression.png" alt="Major Arcana Color Progression">

        <h3>Early Era (Cards 0-7)</h3>
        <p>
            <strong>Aesthetic:</strong> Cool palettes, static compositions, documentary feel<br>
            <strong>Reference:</strong> Talking Heads 77, Fear of Music, Remain in Light (early)<br>
            <strong>Themes:</strong> Observation, alienation, anxious self-awareness, systems as comfort
        </p>
        <img src="palette_early.png" alt="Early Era Palette">

        <h3>Middle Era (Cards 8-14)</h3>
        <p>
            <strong>Aesthetic:</strong> Transitional, warmer tones emerging, more complexity<br>
            <strong>Reference:</strong> Remain in Light (late), Speaking in Tongues, world music collaborations<br>
            <strong>Themes:</strong> Discovery, polyrhythm, beginning to connect, systems observed in motion
        </p>
        <img src="palette_middle.png" alt="Middle Era Palette">

        <h3>Late Era (Cards 15-21)</h3>
        <p>
            <strong>Aesthetic:</strong> Warm, vibrant, dynamic, embodied<br>
            <strong>Reference:</strong> American Utopia, civic engagement, optimistic collaboration<br>
            <strong>Themes:</strong> Joy, presence, collective movement, sincere participation
        </p>
        <img src="palette_late.png" alt="Late Era Palette">
    </div>

    <div class="section">
        <h2>Minor Arcana: Suit Visual Languages</h2>
        <p>
            Each suit represents a distinct visual world with its own complete aesthetic.
            These are not variations on a theme—they are separate approaches to seeing.
        </p>

        <div class="card-grid">
            <div class="card-item">
                <h3>Structures</h3>
                <img src="palette_structures.png" alt="Structures Palette">
                <img src="example_structures.png" alt="Structures Example">
                <p>
                    <strong>Keywords:</strong> Observation, analysis, blueprints, containment<br>
                    <strong>Visual Style:</strong> Clean geometric compositions, architectural drawings,
                    grids, measured spaces, documentation aesthetic
                </p>
            </div>

            <div class="card-item">
                <h3>Rivers</h3>
                <img src="palette_rivers.png" alt="Rivers Palette">
                <img src="example_rivers.png" alt="Rivers Example">
                <p>
                    <strong>Keywords:</strong> Cycles, patterns, rhythm, natural systems<br>
                    <strong>Visual Style:</strong> Organic patterns, polyrhythmic layering,
                    warm earth tones, systems in motion viewed from above
                </p>
            </div>

            <div class="card-item">
                <h3>Curiosity</h3>
                <img src="palette_curiosity.png" alt="Curiosity Palette">
                <img src="example_curiosity.png" alt="Curiosity Example">
                <p>
                    <strong>Keywords:</strong> Inquiry, civic engagement, dialogue, reasons to be cheerful<br>
                    <strong>Visual Style:</strong> Bright optimistic palettes (yellows, sky blues),
                    conversational compositions, open inviting spaces
                </p>
            </div>

            <div class="card-item">
                <h3>Dance</h3>
                <img src="palette_dance.png" alt="Dance Palette">
                <img src="example_dance.png" alt="Dance Example">
                <p>
                    <strong>Keywords:</strong> Embodied joy, collective movement, groove, presence<br>
                    <strong>Visual Style:</strong> Dynamic motion, vibrant warm colors (reds, oranges, golds),
                    energy and heat visible, the view from inside the groove
                </p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Suit Symbols</h2>
        <p>
            Each suit has a symbol that can be incorporated into cards as needed.
            These can be rendered in different styles and scales depending on the card.
        </p>

        <div class="symbols">
            <div class="symbol-item">
                <img src="symbol_structures.png" alt="Structures Symbol">
                <h4>Structures</h4>
                <p>Simple house with triangular roof</p>
            </div>
            <div class="symbol-item">
                <img src="symbol_rivers.png" alt="Rivers Symbol">
                <h4>Rivers</h4>
                <p>Vertical flowing water</p>
            </div>
            <div class="symbol-item">
                <img src="symbol_curiosity.png" alt="Curiosity Symbol">
                <h4>Curiosity</h4>
                <p>Question mark</p>
            </div>
            <div class="symbol-item">
                <img src="symbol_dance.png" alt="Dance Symbol">
                <h4>Dance</h4>
                <p>Dancing figure</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Reusable Visual Elements</h2>
        <p>
            These are example implementations showing how certain visual concepts might be rendered.
            Each card will interpret these concepts uniquely, but these provide reference points.
        </p>

        <h3>Figure Variations</h3>
        <p>
            Figures can be rendered with different postures and at different scales.
            These examples show the <em>concept</em> of posture variation, not fixed templates.
        </p>
        <img src="figure_examples.png" alt="Figure Examples">

        <div class="note">
            <strong>Note on Reusability:</strong> The visual toolkit provides helper functions for
            common tasks (drawing grids, flow patterns, figures, buildings), but each card should
            use these as <em>starting points</em> for unique compositions. Think of these as an
            artist's reference sketches, not as clip-art to assemble.
        </div>
    </div>

    <div class="section">
        <h2>Using This Style Guide</h2>
        <p>
            When creating a card:
        </p>
        <ol>
            <li>Read the card's meaning and visual instructions from the deck JSON</li>
            <li>Reference this style guide to understand:
                <ul>
                    <li>Which color palette to use (major arcana number or suit)</li>
                    <li>What visual style is appropriate</li>
                    <li>What reusable elements might be helpful</li>
                </ul>
            </li>
            <li>Use the toolkit (<code>byrne_visual_toolkit.py</code>) as a helper library</li>
            <li>Create a unique composition interpreting the card's specific meaning</li>
        </ol>

        <div class="note">
            <strong>Remember:</strong> This is a <em>visual vocabulary</em>, not a template system.
            Each card should feel cohesive with the deck while being uniquely interpreted.
        </div>
    </div>

</body>
</html>
"""

    with open(os.path.join(OUTPUT_DIR, 'style_guide.html'), 'w') as f:
        f.write(html)


if __name__ == '__main__':
    main()
