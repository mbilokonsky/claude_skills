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


def create_palette_swatch(palette, name, width=600, height=80):
    """Create a visual swatch showing a color palette (no text, just colors)"""
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
        draw.rectangle([x, 0, x + swatch_width, height], fill=color)

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


def generate_figure_postures():
    """Show various postures"""
    width = 1200
    height = 420
    img = Image.new('RGB', (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    draw.text((10, 10), "Posture Variations", fill=(0, 0, 0))

    postures = ['neutral', 'awkward', 'observing', 'moving']
    for i, posture in enumerate(postures):
        x = 150 + i * 280

        # Background
        draw.rectangle([x - 100, 50, x + 100, 400], fill=(200, 210, 220))

        # Figure
        bvt.example_figure_simple(img, x, 380, bvt.MajorArcanaColors.EARLY,
                                  posture=posture, scale=1.3)

        # Label
        draw.text((x - len(posture)*4, 400), posture, fill=(0, 0, 0))

    return img


def generate_figure_scales():
    """Show scale/distance variations"""
    width = 1000
    height = 420
    img = Image.new('RGB', (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    draw.text((10, 10), "Scale Variations (distance/presence)", fill=(0, 0, 0))

    # Small/distant figure (observed)
    draw.text((80, 50), "Distant/Observed", fill=(60, 60, 60))
    draw.rectangle([50, 80, 250, 400], fill=(200, 210, 220))
    bvt.example_figure_simple(img, 150, 380, bvt.MajorArcanaColors.EARLY,
                              posture='neutral', scale=0.5)

    # Medium figure
    draw.text((380, 50), "Medium", fill=(60, 60, 60))
    draw.rectangle([320, 80, 520, 400], fill=(200, 210, 220))
    bvt.example_figure_simple(img, 420, 380, bvt.MajorArcanaColors.MIDDLE,
                              posture='neutral', scale=1.0)

    # Large/present figure
    draw.text((680, 50), "Present/Engaged", fill=(60, 60, 60))
    draw.rectangle([600, 80, 900, 400], fill=(200, 210, 220))
    bvt.example_figure_simple(img, 750, 380, bvt.MajorArcanaColors.LATE,
                              posture='moving', scale=1.8)

    return img


def generate_byrne_big_suit():
    """Show the Big Suit Byrne character - using same no-legs approach"""
    width = 800
    height = 500
    img = Image.new('RGB', (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    draw.text((10, 10), "The Big Suit - Byrne Character", fill=(0, 0, 0))

    # Early Byrne (stiff, boxy, upright)
    draw.text((100, 50), "Early: Stiff/Boxy", fill=(60, 60, 60))
    draw.rectangle([60, 80, 280, 480], fill=(200, 210, 220))

    head_x, head_y = 170, 140

    # Head
    draw.ellipse([head_x-15, head_y, head_x+15, head_y+30],
                 fill=bvt.MajorArcanaColors.EARLY['secondary'])

    # The BIG SUIT - massively oversized boxy jacket polygon
    # No separate legs - the jacket polygon tapers to suggest legs inside
    jacket_color = (70, 80, 90)
    big_suit_shape = [
        (head_x, head_y+28),           # neck
        (head_x-90, head_y+45),        # left shoulder (HUGE)
        (head_x-85, head_y+120),       # left mid-jacket
        (head_x-70, head_y+250),       # left lower jacket
        (head_x-25, head_y+320),       # left foot area
        (head_x+25, head_y+320),       # right foot area
        (head_x+70, head_y+250),       # right lower jacket
        (head_x+85, head_y+120),       # right mid-jacket
        (head_x+90, head_y+45),        # right shoulder (HUGE)
    ]
    draw.polygon(big_suit_shape, fill=jacket_color)

    # Lapels (darker for depth)
    lapel_color = (50, 60, 70)
    draw.polygon([
        (head_x, head_y+28), (head_x-25, head_y+45),
        (head_x-20, head_y+150), (head_x-5, head_y+120)
    ], fill=lapel_color)
    draw.polygon([
        (head_x, head_y+28), (head_x+25, head_y+45),
        (head_x+20, head_y+150), (head_x+5, head_y+120)
    ], fill=lapel_color)

    # Late Byrne (still big, but with flow and tilt)
    draw.text((500, 50), "Late: Big Suit Dancing", fill=(60, 60, 60))
    draw.rectangle([460, 80, 680, 480], fill=(220, 200, 180))

    head_x, head_y = 570, 140

    # Head (tilted for motion)
    draw.ellipse([head_x-12, head_y+5, head_x+18, head_y+35],
                 fill=bvt.MajorArcanaColors.LATE['secondary'])

    # The BIG SUIT in motion - still huge, but tilted and dynamic
    # Arms INSIDE jacket - the whole jacket shape shows movement
    jacket_color = (200, 100, 80)
    moving_suit_shape = [
        (head_x+5, head_y+30),         # neck (tilted)
        (head_x-85, head_y+55),        # left shoulder/arm (back extended)
        (head_x-90, head_y+140),       # left arm extended
        (head_x-65, head_y+250),       # left lower
        (head_x-20, head_y+320),       # left foot
        (head_x+30, head_y+325),       # right foot (forward)
        (head_x+75, head_y+260),       # right lower (forward)
        (head_x+100, head_y+150),      # right arm extended forward
        (head_x+95, head_y+60),        # right shoulder (forward)
    ]
    draw.polygon(moving_suit_shape, fill=jacket_color)

    # Lapel showing tilt
    lapel_color = (160, 80, 60)
    draw.polygon([
        (head_x+5, head_y+30), (head_x-20, head_y+55),
        (head_x-15, head_y+160), (head_x+10, head_y+130)
    ], fill=lapel_color)

    return img


def generate_crowd_examples():
    """Show different crowd/group representations"""
    width = 1000
    height = 500
    img = Image.new('RGB', (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    draw.text((10, 10), "Crowd/Group Representations", fill=(0, 0, 0))

    # Geometric/observed crowd (early)
    draw.text((70, 50), "Geometric Pattern (Early)", fill=(60, 60, 60))
    draw.rectangle([40, 80, 310, 240], fill=(200, 210, 220))

    # Grid of identical small figures
    for row in range(4):
        for col in range(6):
            x = 65 + col * 40
            y = 220 - row * 35
            # Tiny identical figures
            draw.ellipse([x-3, y-20, x+3, y-14],
                        fill=bvt.MajorArcanaColors.EARLY['primary'])
            draw.rectangle([x-4, y-14, x+4, y],
                          fill=bvt.MajorArcanaColors.EARLY['secondary'])

    # Abstract/dots crowd
    draw.text((370, 50), "Abstract/Distant", fill=(60, 60, 60))
    draw.rectangle([340, 80, 610, 240], fill=(200, 210, 220))

    # Dots and shapes suggesting crowd
    import random
    random.seed(42)  # Consistent generation
    for i in range(40):
        x = 360 + random.randint(0, 230)
        y = 100 + random.randint(0, 120)
        size = random.randint(3, 8)
        draw.ellipse([x-size, y-size, x+size, y+size],
                    fill=bvt.MajorArcanaColors.MIDDLE['secondary'])

    # Organic/varied crowd (late)
    draw.text((680, 50), "Varied Community (Late)", fill=(60, 60, 60))
    draw.rectangle([650, 80, 960, 240], fill=(220, 200, 180))

    # Different sized figures, varied
    crowd_positions = [(700, 220), (740, 215), (780, 225), (820, 210),
                       (860, 220), (900, 215)]
    crowd_scales = [0.6, 0.7, 0.55, 0.65, 0.6, 0.7]
    for (cx, cy), scale in zip(crowd_positions, crowd_scales):
        bvt.example_figure_simple(img, cx, cy, bvt.MajorArcanaColors.LATE,
                                  posture='moving', scale=scale)

    # Detail level examples
    draw.text((70, 270), "Detail Levels", fill=(60, 60, 60))

    # Silhouette
    draw.text((100, 300), "Silhouette", fill=(60, 60, 60))
    draw.rectangle([60, 330, 200, 480], fill=(200, 210, 220))
    # Simple filled shape
    shadow = bvt.MajorArcanaColors.EARLY['shadow']
    draw.ellipse([120, 360, 140, 380], fill=shadow)
    draw.polygon([(130, 380), (115, 395), (115, 455), (145, 455), (145, 395)], fill=shadow)

    # Simple (what we've been using)
    draw.text((280, 300), "Simple", fill=(60, 60, 60))
    draw.rectangle([240, 330, 380, 480], fill=(200, 210, 220))
    bvt.example_figure_simple(img, 310, 465, bvt.MajorArcanaColors.MIDDLE,
                              posture='neutral', scale=1.0)

    # More detailed (but still following circle + polygon approach)
    draw.text((450, 300), "More Defined", fill=(60, 60, 60))
    draw.rectangle([420, 330, 560, 480], fill=(200, 210, 220))

    # Head with more detail
    head_x, head_y = 490, 375
    draw.ellipse([head_x-12, head_y, head_x+12, head_y+24],
                fill=bvt.MajorArcanaColors.LATE['accent'])
    # Face hint (eyes)
    draw.line([(head_x-6, head_y+10), (head_x-4, head_y+10)],
             fill=bvt.MajorArcanaColors.LATE['shadow'], width=2)
    draw.line([(head_x+4, head_y+10), (head_x+6, head_y+10)],
             fill=bvt.MajorArcanaColors.LATE['shadow'], width=2)

    # Body polygon with more defined structure but NO separate legs
    # Added arm extensions and more articulation
    detailed_body = [
        (head_x, head_y+24),            # neck
        (head_x-18, head_y+40),         # left shoulder
        (head_x-32, head_y+70),         # left arm extended
        (head_x-20, head_y+75),         # left arm back to body
        (head_x-18, head_y+100),        # left hip
        (head_x-8, head_y+140),         # left foot
        (head_x+8, head_y+140),         # right foot
        (head_x+18, head_y+100),        # right hip
        (head_x+20, head_y+75),         # right arm back to body
        (head_x+28, head_y+72),         # right arm extended
        (head_x+18, head_y+40),         # right shoulder
    ]
    draw.polygon(detailed_body, fill=bvt.MajorArcanaColors.LATE['secondary'])

    return img


def generate_common_elements():
    """Show common visual building blocks"""
    width = 1000
    height = 500
    img = Image.new('RGB', (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    # Title
    draw.text((10, 10), "Common Visual Elements", fill=(0, 0, 0))

    # Buildings
    draw.text((30, 50), "Buildings", fill=(60, 60, 60))
    bvt.example_urban_building(draw, 30, 80, 80, 160, bvt.SuitColors.STRUCTURES, style='simple')
    bvt.example_urban_building(draw, 130, 80, 90, 160, bvt.SuitColors.STRUCTURES, style='geometric')

    # Grid
    draw.text((260, 50), "Grid/Blueprint", fill=(60, 60, 60))
    bvt.example_grid_structure(draw, (260, 80, 440, 240), bvt.SuitColors.STRUCTURES, style='blueprint')

    # Doorway/Threshold
    draw.text((30, 260), "Doorway/Threshold", fill=(60, 60, 60))
    bvt.example_doorway_threshold(draw, 30, 290, 120, 180, bvt.MajorArcanaColors.EARLY)

    # Stage elements
    draw.text((480, 50), "Stage/Performance", fill=(60, 60, 60))
    bvt.example_stage_elements(draw, 480, 200, 480, bvt.SuitColors.DANCE)

    # Musical elements
    draw.text((200, 260), "Musical Elements", fill=(60, 60, 60))
    for i in range(3):
        bvt.example_musical_elements(img, 200 + i * 40, 290, bvt.SuitColors.DANCE)

    # Flow patterns
    draw.text((480, 260), "Flow Patterns", fill=(60, 60, 60))
    bvt.draw_flow_pattern(draw, (480, 290, 950, 350), 50, 20, bvt.SuitColors.RIVERS['flow'])
    bvt.draw_flow_pattern(draw, (480, 360, 950, 420), 40, 15, bvt.SuitColors.RIVERS['secondary'])

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

    # 6. Figure examples (multiple images)
    print("  - Figure postures...")
    fig_postures = generate_figure_postures()
    fig_postures.save(os.path.join(OUTPUT_DIR, 'figure_postures.png'))

    print("  - Figure scales...")
    fig_scales = generate_figure_scales()
    fig_scales.save(os.path.join(OUTPUT_DIR, 'figure_scales.png'))

    print("  - Byrne big suit...")
    byrne_suit = generate_byrne_big_suit()
    byrne_suit.save(os.path.join(OUTPUT_DIR, 'byrne_big_suit.png'))

    print("  - Crowd examples...")
    crowds = generate_crowd_examples()
    crowds.save(os.path.join(OUTPUT_DIR, 'crowd_examples.png'))

    # 7. Common visual elements
    print("  - Common visual elements...")
    elements = generate_common_elements()
    elements.save(os.path.join(OUTPUT_DIR, 'common_elements.png'))

    # 8. Setting types
    print("  - Setting type examples...")
    setting_types = ['city_street', 'stage', 'aerial', 'interior', 'natural', 'collaborative']
    for setting in setting_types:
        # Use appropriate palette for each setting
        if setting == 'city_street':
            pal = bvt.SuitColors.STRUCTURES
        elif setting == 'stage':
            pal = bvt.SuitColors.DANCE
        elif setting == 'aerial':
            pal = bvt.MajorArcanaColors.EARLY
        elif setting == 'interior':
            pal = bvt.SuitColors.STRUCTURES
        elif setting == 'natural':
            pal = bvt.SuitColors.RIVERS
        else:  # collaborative
            pal = bvt.SuitColors.CURIOSITY

        setting_img = bvt.generate_setting_example(setting, pal)
        setting_img.save(os.path.join(OUTPUT_DIR, f'setting_{setting}.png'))

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
        <p><small>Colors (left to right): primary, secondary, accent, highlight, shadow, ground</small></p>

        <h3>Middle Era (Cards 8-14)</h3>
        <p>
            <strong>Aesthetic:</strong> Transitional, warmer tones emerging, more complexity<br>
            <strong>Reference:</strong> Remain in Light (late), Speaking in Tongues, world music collaborations<br>
            <strong>Themes:</strong> Discovery, polyrhythm, beginning to connect, systems observed in motion
        </p>
        <img src="palette_middle.png" alt="Middle Era Palette">
        <p><small>Colors (left to right): primary, secondary, accent, highlight, shadow, ground</small></p>

        <h3>Late Era (Cards 15-21)</h3>
        <p>
            <strong>Aesthetic:</strong> Warm, vibrant, dynamic, embodied<br>
            <strong>Reference:</strong> American Utopia, civic engagement, optimistic collaboration<br>
            <strong>Themes:</strong> Joy, presence, collective movement, sincere participation
        </p>
        <img src="palette_late.png" alt="Late Era Palette">
        <p><small>Colors (left to right): primary, secondary, accent, highlight, shadow, ground</small></p>
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
                <p><small>Colors: primary, secondary, accent, grid, shadow, frame</small></p>
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
                <p><small>Colors: primary, secondary, accent, flow, shadow, pattern</small></p>
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
                <p><small>Colors: primary, secondary, accent, dialogue, shadow, text</small></p>
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
                <p><small>Colors: primary, secondary, accent, electric, shadow, heat</small></p>
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
        <h2>Representing Humans</h2>
        <p>
            How people appear in this deck carries meaning. Body language, scale, and detail level
            all communicate the relationship between observer and observed, self and other.
        </p>

        <h3>General Principles</h3>
        <ul>
            <li><strong>Body language carries meaning:</strong> rigid/geometric → fluid/organic reflects the journey</li>
            <li><strong>Simplified but expressive:</strong> Faces are minimal—the body tells the story</li>
            <li><strong>Scale indicates relationship:</strong> Small figures = observed from distance, large = present and engaged</li>
        </ul>

        <h3>Specific Characters</h3>
        <p><strong>Byrne (when depicted as himself):</strong></p>
        <ul>
            <li><strong>The Big Suit:</strong> Oversized boxy jacket, especially in later cards</li>
            <li><strong>Posture evolution:</strong> Stiff/angular (early) → loose/dancing (late)</li>
            <li>Often in performance stance, conducting, presenting, or mid-gesture</li>
        </ul>

        <p><strong>Audience/Crowd:</strong></p>
        <ul>
            <li>Geometric patterns (early: observed) or organic groups (late: felt presence)</li>
            <li>Repetition with variation</li>
            <li>May be abstracted to dots, shapes, or simplified figures</li>
        </ul>

        <h3>Visual Shortcuts</h3>
        <ul>
            <li>Big boxy jacket = Byrne</li>
            <li>Suit and tie = formal/structured self</li>
            <li>Loose clothing = relaxed/authentic self</li>
            <li>Multiple identical figures = pattern observation</li>
            <li>Varied figures together = genuine community</li>
        </ul>

        <h3>Posture Variations</h3>
        <img src="figure_postures.png" alt="Figure Postures">
        <p>Different postures communicate different states: neutral, awkward/anxious, observing, moving/dancing.</p>

        <h3>Scale and Presence</h3>
        <img src="figure_scales.png" alt="Figure Scales">
        <p>Scale indicates relationship to the scene. Small/distant = observed from outside; large/present = engaged and embodied.</p>

        <h3>The Big Suit - Byrne as Character</h3>
        <img src="byrne_big_suit.png" alt="Byrne Big Suit">
        <p>When Byrne appears as a character, the oversized boxy jacket is the key identifier. Early cards show it stiff and angular; late cards show it flowing and dynamic.</p>

        <h3>Crowds and Groups</h3>
        <img src="crowd_examples.png" alt="Crowd Examples">
        <p>Multiple ways to represent groups: geometric patterns (observed), abstract dots (distant), varied figures (community), and different detail levels (silhouette to defined).</p>

        <div class="note">
            <strong>Important:</strong> These examples show the <em>range of possibilities</em>, not templates to copy. Each card should select appropriate approaches based on its specific meaning and suit aesthetic.
        </div>
    </div>

    <div class="section">
        <h2>Common Visual Elements</h2>
        <p>
            Reusable building blocks for constructing card scenes. These are tools and reference examples,
            not templates to copy-paste. Each use should be adapted to the specific card's needs.
        </p>
        <img src="common_elements.png" alt="Common Visual Elements">
        <ul>
            <li><strong>Buildings:</strong> Simple and geometric styles for urban scenes</li>
            <li><strong>Grids/Blueprints:</strong> Structured patterns for Structures suit</li>
            <li><strong>Doorways/Thresholds:</strong> Recurring transition motif</li>
            <li><strong>Stage Elements:</strong> Performance spaces, speakers, equipment</li>
            <li><strong>Musical Elements:</strong> Notes, rhythmic symbols</li>
            <li><strong>Flow Patterns:</strong> Organic waves and rhythms for Rivers suit</li>
        </ul>
    </div>

    <div class="section">
        <h2>Setting Types</h2>
        <p>
            Common kinds of spaces that recur across the deck. Not specific places, but spatial
            archetypes that carry meaning.
        </p>

        <div class="card-grid">
            <div class="card-item">
                <h4>City Street</h4>
                <img src="setting_city_street.png" alt="City Street">
                <p>Suggestive container showing urban context. Buildings frame edges, leaving center open for figures and action. Sky, ground, architectural hints.<br>
                <strong>Used in:</strong> Early cards, Structures suit</p>
            </div>

            <div class="card-item">
                <h4>Performance Stage</h4>
                <img src="setting_stage.png" alt="Performance Stage">
                <p>Raised platform, lighting, equipment, audience space.<br>
                <strong>Used in:</strong> Late cards, Dance suit</p>
            </div>

            <div class="card-item">
                <h4>Aerial View</h4>
                <img src="setting_aerial.png" alt="Aerial View">
                <p>Looking down from above: nature (greens, blues) intersecting with sparse human structures. Detached observation of the relationship between natural and built.<br>
                <strong>Used in:</strong> Early-mid cards, "The Big Country"</p>
            </div>

            <div class="card-item">
                <h4>Interior Domestic</h4>
                <img src="setting_interior.png" alt="Interior">
                <p>Rooms with objects, organized space, windows looking out.<br>
                <strong>Used in:</strong> "Don't Worry About the Government", Structures</p>
            </div>

            <div class="card-item">
                <h4>Natural Landscape</h4>
                <img src="setting_natural.png" alt="Natural Landscape">
                <p>Rivers, organic flows, patterns in nature, earth tones.<br>
                <strong>Used in:</strong> Rivers suit, transition cards</p>
            </div>

            <div class="card-item">
                <h4>Collaborative Space</h4>
                <img src="setting_collaborative.png" alt="Collaborative Space">
                <p>Open inclusive composition, bright and welcoming.<br>
                <strong>Used in:</strong> Late cards, Curiosity and Dance suits</p>
            </div>
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
