#!/usr/bin/env python3
"""
Custom pixel art generation for the Structures suit
Each card is hand-crafted to tell its unique story
"""

import sys
import os
from PIL import Image, ImageDraw
import math

# Add the visuals directory to path
sys.path.insert(0, '/home/user/claude_skills/tarot/decks/byrne/visuals')
import byrne_visual_toolkit as bvt

# Dimensions
WIDTH = 280
HEIGHT = 420

# Color palette
PALETTE = bvt.SuitColors.STRUCTURES


def draw_structures_0_ace(img, draw):
    """
    Ace of Structures: the seed of analysis, pure observational potential
    Content: A single clean line on white space, the first mark of order

    Visual: Pure minimalism - a single perfect intersection, the origin point
    """
    # Single vertical line - the first axis
    draw.line([(WIDTH//2, 60), (WIDTH//2, HEIGHT - 60)],
              fill=PALETTE['frame'], width=3)

    # Single horizontal line - the second axis
    draw.line([(60, HEIGHT//2), (WIDTH - 60, HEIGHT//2)],
              fill=PALETTE['frame'], width=3)

    # Small square at the center - the seed
    center_size = 8
    draw.rectangle([WIDTH//2 - center_size, HEIGHT//2 - center_size,
                   WIDTH//2 + center_size, HEIGHT//2 + center_size],
                  fill=PALETTE['accent'])


def draw_structures_1_two(img, draw):
    """
    Two of Structures: choosing between frameworks, dual perspectives
    Content: Two architectural plans side by side, two windows with different views

    Visual: Split composition - left and right halves show different systems
    """
    midline = WIDTH // 2

    # Left framework - vertical emphasis
    draw.rectangle([40, 100, 120, 320], outline=PALETTE['frame'], width=2)
    # Vertical subdivisions
    draw.line([(80, 100), (80, 320)], fill=PALETTE['grid'], width=1)
    # Windows looking up
    draw.rectangle([50, 120, 70, 160], fill=PALETTE['secondary'])
    draw.rectangle([90, 120, 110, 160], fill=PALETTE['secondary'])

    # Right framework - horizontal emphasis
    draw.rectangle([160, 100, 240, 320], outline=PALETTE['frame'], width=2)
    # Horizontal subdivisions
    draw.line([(160, 210), (240, 210)], fill=PALETTE['grid'], width=1)
    # Windows looking across
    draw.rectangle([170, 180, 230, 200], fill=PALETTE['secondary'])
    draw.rectangle([170, 220, 230, 240], fill=PALETTE['secondary'])

    # Subtle dividing line between the two choices
    draw.line([(midline, 80), (midline, 340)], fill=PALETTE['grid'], width=1)


def draw_structures_2_three(img, draw):
    """
    Three of Structures: taxonomy emerging, categories forming
    Content: Three architectural elements forming initial structure

    Visual: Three distinct architectural forms starting to organize space
    """
    # Top element - triangular roof/concept
    points = [(WIDTH//2, 70), (100, 140), (180, 140)]
    draw.polygon(points, fill=PALETTE['secondary'], outline=PALETTE['frame'])

    # Left element - vertical tower
    draw.rectangle([60, 180, 100, 320], fill=PALETTE['secondary'],
                   outline=PALETTE['frame'], width=2)
    draw.rectangle([68, 200, 92, 220], fill=PALETTE['accent'])
    draw.rectangle([68, 240, 92, 260], fill=PALETTE['accent'])
    draw.rectangle([68, 280, 92, 300], fill=PALETTE['accent'])

    # Right element - horizontal base
    draw.rectangle([120, 260, 220, 320], fill=PALETTE['secondary'],
                   outline=PALETTE['frame'], width=2)
    draw.line([(140, 260), (140, 320)], fill=PALETTE['grid'], width=1)
    draw.line([(170, 260), (170, 320)], fill=PALETTE['grid'], width=1)
    draw.line([(200, 260), (200, 320)], fill=PALETTE['grid'], width=1)


def draw_structures_3_four(img, draw):
    """
    Four of Structures: stable system, the framework complete, four walls standing
    Content: A complete architectural structure, windows looking out but figure looking in

    Visual: A solid building with four walls, figure inside looking inward
    """
    # The complete four-walled structure
    building_x = 70
    building_y = 100
    building_w = 140
    building_h = 220

    # Outer walls
    draw.rectangle([building_x, building_y, building_x + building_w, building_y + building_h],
                   fill=PALETTE['secondary'], outline=PALETTE['frame'], width=3)

    # Windows looking OUT (to the world)
    draw.rectangle([85, 120, 110, 155], fill=PALETTE['primary'])  # top left
    draw.rectangle([155, 120, 180, 155], fill=PALETTE['primary'])  # top right
    draw.rectangle([85, 180, 110, 215], fill=PALETTE['primary'])   # bottom left
    draw.rectangle([155, 180, 180, 215], fill=PALETTE['primary'])  # bottom right

    # Door (closed)
    draw.rectangle([120, 260, 150, 320], outline=PALETTE['frame'], width=2)

    # Small figure INSIDE looking inward at the structure itself
    # Head
    draw.ellipse([132, 245, 142, 255], fill=PALETTE['accent'])
    # Body (simple geometric)
    draw.rectangle([130, 255, 144, 275], fill=PALETTE['shadow'])


def draw_structures_4_five(img, draw):
    """
    Five of Structures: framework challenged, cracks in the system
    Content: Architectural plans with elements that don't align, cracks in walls

    Visual: A structure with visible cracks, misalignments, the anomaly appearing
    """
    # Main structure - but slightly off
    draw.rectangle([60, 90, 180, 280], fill=PALETTE['secondary'],
                   outline=PALETTE['frame'], width=2)

    # CRACK - diagonal through the structure
    crack_points = [(100, 90), (105, 90), (135, 280), (130, 280)]
    draw.polygon(crack_points, fill=PALETTE['shadow'])

    # Grid that doesn't quite align
    draw.line([(60, 140), (180, 145)], fill=PALETTE['grid'], width=1)  # slightly off
    draw.line([(60, 190), (180, 185)], fill=PALETTE['grid'], width=1)  # opposite off
    draw.line([(60, 240), (180, 242)], fill=PALETTE['grid'], width=1)  # barely off

    # An element that doesn't fit - fifth piece jutting out awkwardly
    draw.rectangle([180, 160, 220, 210], fill=PALETTE['accent'],
                   outline=PALETTE['frame'], width=2)
    # Connection line showing the failed integration
    draw.line([(180, 185), (220, 185)], fill=PALETTE['shadow'], width=1)


def draw_structures_5_six(img, draw):
    """
    Six of Structures: revised framework, adaptive system, restored order at higher level
    Content: Architectural elements rearranged into new configuration, negotiated structure

    Visual: Six elements in a new, more complex but coherent arrangement
    """
    # New arrangement - hexagonal organization (six points)
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    radius = 85

    # Six elements arranged in hexagon
    for i in range(6):
        angle = (i * 60 - 90) * math.pi / 180  # Start from top
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))

        # Each element is a small architectural form
        size = 28
        draw.rectangle([x - size//2, y - size//2, x + size//2, y + size//2],
                      fill=PALETTE['secondary'], outline=PALETTE['frame'], width=2)
        # Window in each
        draw.rectangle([x - size//4, y - size//4, x + size//4, y + size//4],
                      fill=PALETTE['accent'])

    # Connecting lines showing the new relationships
    for i in range(6):
        angle1 = (i * 60 - 90) * math.pi / 180
        angle2 = ((i + 1) * 60 - 90) * math.pi / 180
        x1 = center_x + int(radius * math.cos(angle1))
        y1 = center_y + int(radius * math.sin(angle1))
        x2 = center_x + int(radius * math.cos(angle2))
        y2 = center_y + int(radius * math.sin(angle2))
        draw.line([(x1, y1), (x2, y2)], fill=PALETTE['grid'], width=1)


def draw_structures_6_seven(img, draw):
    """
    Seven of Structures: examining the system, meta-analysis, studying the map itself
    Content: A figure examining multiple blueprints, floor plans spread out

    Visual: Figure bent over table with multiple overlapping plans
    """
    # Table/desk surface
    draw.rectangle([40, 240, 240, 260], fill=PALETTE['shadow'])

    # Multiple blueprint sheets scattered, overlapping
    # Blueprint 1 (back)
    draw.rectangle([50, 180, 130, 250], fill=PALETTE['primary'],
                   outline=PALETTE['grid'], width=1)
    bvt.draw_grid_pattern(draw, (55, 185, 125, 245), 15, PALETTE['grid'])

    # Blueprint 2 (middle)
    draw.rectangle([90, 200, 170, 270], fill=PALETTE['primary'],
                   outline=PALETTE['grid'], width=1)
    bvt.draw_grid_pattern(draw, (95, 205, 165, 265), 15, PALETTE['grid'])

    # Blueprint 3 (front)
    draw.rectangle([130, 190, 210, 260], fill=PALETTE['primary'],
                   outline=PALETTE['grid'], width=1)
    bvt.draw_grid_pattern(draw, (135, 195, 205, 255), 15, PALETTE['grid'])

    # Figure leaning over, examining (head and shoulders visible)
    # Head
    draw.ellipse([125, 140, 145, 160], fill=PALETTE['accent'])
    # Neck/shoulders bent forward
    draw.polygon([(135, 160), (115, 180), (115, 200), (155, 200), (155, 180)],
                fill=PALETTE['secondary'])
    # Arm pointing at blueprint
    draw.line([(155, 190), (180, 220)], fill=PALETTE['secondary'], width=6)


def draw_structures_7_eight(img, draw):
    """
    Eight of Structures: implementing the plan, blueprint executed, theory becoming practice
    Content: Architectural plans being actively built, systematic transformation in progress

    Visual: Building in construction, half blueprint/half physical structure
    """
    split_x = WIDTH // 2

    # LEFT SIDE: The blueprint (plan)
    draw.rectangle([30, 100, split_x - 5, 320], fill=PALETTE['primary'])
    # Blueprint grid
    bvt.draw_grid_pattern(draw, (35, 105, split_x - 10, 315), 20, PALETTE['grid'])
    # Drawn structure on blueprint
    draw.rectangle([50, 140, 110, 280], outline=PALETTE['frame'], width=2)
    draw.line([(80, 140), (80, 280)], fill=PALETTE['grid'], width=1)
    draw.line([(50, 210), (110, 210)], fill=PALETTE['grid'], width=1)

    # RIGHT SIDE: The built structure (reality)
    # Actual 3D-ish building
    # Front face
    draw.rectangle([split_x + 15, 140, split_x + 95, 320],
                   fill=PALETTE['secondary'], outline=PALETTE['frame'], width=2)
    # Side face (showing depth)
    side_points = [
        (split_x + 95, 140),
        (split_x + 115, 125),
        (split_x + 115, 305),
        (split_x + 95, 320)
    ]
    draw.polygon(side_points, fill=PALETTE['shadow'], outline=PALETTE['frame'])
    # Top (roof)
    top_points = [
        (split_x + 15, 140),
        (split_x + 35, 125),
        (split_x + 115, 125),
        (split_x + 95, 140)
    ]
    draw.polygon(top_points, fill=PALETTE['accent'], outline=PALETTE['frame'])

    # Windows on built structure
    draw.rectangle([split_x + 30, 180, split_x + 50, 210], fill=PALETTE['primary'])
    draw.rectangle([split_x + 60, 180, split_x + 80, 210], fill=PALETTE['primary'])
    draw.rectangle([split_x + 30, 240, split_x + 50, 270], fill=PALETTE['primary'])
    draw.rectangle([split_x + 60, 240, split_x + 80, 270], fill=PALETTE['primary'])


def draw_structures_8_nine(img, draw):
    """
    Nine of Structures: comprehensive system, analysis fulfilled, the complete map
    Content: Nine architectural elements in complete harmony, total system visible

    Visual: Nine structures in perfect 3x3 grid, the complete taxonomy
    """
    # Perfect 3x3 grid of architectural elements
    margin = 45
    spacing_x = (WIDTH - 2 * margin) // 3
    spacing_y = (HEIGHT - 2 * margin) // 3
    element_size = 45

    for row in range(3):
        for col in range(3):
            x = margin + col * spacing_x + spacing_x // 2
            y = margin + row * spacing_y + spacing_y // 2

            # Each element is a different architectural form (variety in unity)
            element_num = row * 3 + col

            if element_num % 3 == 0:
                # Square building
                draw.rectangle([x - element_size//2, y - element_size//2,
                              x + element_size//2, y + element_size//2],
                              fill=PALETTE['secondary'], outline=PALETTE['frame'], width=2)
            elif element_num % 3 == 1:
                # Triangular roof structure
                points = [(x, y - element_size//2),
                         (x - element_size//2, y + element_size//2),
                         (x + element_size//2, y + element_size//2)]
                draw.polygon(points, fill=PALETTE['secondary'], outline=PALETTE['frame'])
            else:
                # Circular structure
                draw.ellipse([x - element_size//2, y - element_size//2,
                            x + element_size//2, y + element_size//2],
                            fill=PALETTE['secondary'], outline=PALETTE['frame'], width=2)

            # Small window in each
            draw.rectangle([x - 8, y - 8, x + 8, y + 8], fill=PALETTE['accent'])

    # Subtle grid lines connecting everything
    for i in range(4):
        x = margin + i * spacing_x
        draw.line([(x, margin), (x, HEIGHT - margin)], fill=PALETTE['grid'], width=1)
    for i in range(4):
        y = margin + i * spacing_y
        draw.line([(margin, y), (WIDTH - margin, y)], fill=PALETTE['grid'], width=1)


def draw_structures_9_ten(img, draw):
    """
    Ten of Structures: system at its limit, framework overflowing, analysis exhausted
    Content: Ten architectural elements spilling beyond containment, order becoming chaos

    Visual: Too many structures, overlapping, competing, bursting the frame
    """
    # Start with rigid grid but elements break free
    structures = [
        # These start organized
        (60, 80, 50, 70),
        (140, 80, 50, 70),
        (220, 80, 50, 70),
        (60, 170, 50, 70),
        (140, 170, 50, 70),
        (220, 170, 50, 70),
        # These are spilling out, overlapping
        (100, 260, 60, 80),   # Larger, overlapping
        (180, 250, 55, 75),   # Askew
        (30, 300, 45, 90),    # Near edge
        (200, 310, 50, 95),   # Pushing boundary
    ]

    for i, (x, y, w, h) in enumerate(structures):
        # Later structures are more chaotic
        if i < 6:
            # Early ones: organized
            draw.rectangle([x - w//2, y - h//2, x + w//2, y + h//2],
                          fill=PALETTE['secondary'], outline=PALETTE['frame'], width=2)
        else:
            # Later ones: tilted, overlapping, darker
            # Slight rotation effect via polygon
            offset = (i - 6) * 3
            points = [
                (x - w//2 + offset, y - h//2),
                (x + w//2 + offset, y - h//2 - offset),
                (x + w//2 - offset, y + h//2),
                (x - w//2 - offset, y + h//2 + offset)
            ]
            draw.polygon(points, fill=PALETTE['shadow'], outline=PALETTE['frame'])

    # Crossing lines showing conflict
    draw.line([(40, 200), (240, 350)], fill=PALETTE['frame'], width=1)
    draw.line([(240, 200), (40, 350)], fill=PALETTE['frame'], width=1)


def draw_structures_10_observer(img, draw):
    """
    Observer of Structures: the architect as witness, documenting human systems
    Content: A figure with notebook watching people in buildings, architectural anthropology

    Visual: Figure in foreground with notebook, buildings with people visible through windows in background
    """
    # Background: Building with windows showing people inside
    draw.rectangle([120, 80, 250, 280], fill=PALETTE['secondary'],
                   outline=PALETTE['frame'], width=3)

    # Windows with tiny people visible inside (being observed)
    # Top left window - person standing
    draw.rectangle([135, 100, 170, 150], fill=PALETTE['primary'])
    draw.ellipse([148, 110, 157, 119], fill=PALETTE['accent'])  # head
    draw.rectangle([150, 119, 155, 135], fill=PALETTE['shadow'])  # body

    # Top right window - person sitting
    draw.rectangle([180, 100, 215, 150], fill=PALETTE['primary'])
    draw.ellipse([193, 115, 202, 124], fill=PALETTE['accent'])
    draw.rectangle([195, 124, 200, 135], fill=PALETTE['shadow'])

    # Bottom windows with more people
    draw.rectangle([135, 170, 170, 220], fill=PALETTE['primary'])
    draw.ellipse([148, 180, 157, 189], fill=PALETTE['accent'])
    draw.rectangle([150, 189, 155, 205], fill=PALETTE['shadow'])

    draw.rectangle([180, 170, 215, 220], fill=PALETTE['primary'])
    draw.ellipse([193, 185, 202, 194], fill=PALETTE['accent'])
    draw.rectangle([195, 194, 200, 210], fill=PALETTE['shadow'])

    # Foreground: THE OBSERVER - larger figure with notebook
    # Head (looking toward building)
    draw.ellipse([55, 260, 80, 285], fill=PALETTE['accent'])

    # Body
    body_points = [(67, 285), (45, 300), (45, 380), (90, 380), (90, 300)]
    draw.polygon(body_points, fill=PALETTE['frame'])

    # Notebook held in front
    draw.rectangle([50, 310, 75, 340], fill=PALETTE['primary'],
                   outline=PALETTE['shadow'], width=2)
    # Lines on notebook
    draw.line([(55, 318), (70, 318)], fill=PALETTE['grid'], width=1)
    draw.line([(55, 325), (70, 325)], fill=PALETTE['grid'], width=1)
    draw.line([(55, 332), (70, 332)], fill=PALETTE['grid'], width=1)

    # Pencil
    draw.line([(75, 320), (85, 315)], fill=PALETTE['shadow'], width=3)


def draw_structures_11_pretender(img, draw):
    """
    Pretender of Structures: performing systematic knowledge, theatrical architecture
    Content: Figure in oversized architect's clothes, grand gestures over impressive but untested plans

    Visual: Big suit Byrne gesturing dramatically over elaborate blueprint, commanding attention
    """
    # Elaborate blueprint on table/ground (impressive but untested)
    draw.rectangle([40, 280, 240, 380], fill=PALETTE['primary'],
                   outline=PALETTE['grid'], width=2)
    # Complex-looking but questionable plans
    bvt.draw_grid_pattern(draw, (45, 285, 235, 375), 15, PALETTE['grid'])
    # Overly ambitious structure drawn
    draw.polygon([(140, 300), (100, 340), (180, 340)], outline=PALETTE['frame'], width=2)
    draw.rectangle([110, 340, 170, 370], outline=PALETTE['frame'], width=2)

    # THE PRETENDER - large figure with oversized clothes, commanding gesture
    # Small head (Byrne style - escaping cognitive prison)
    head_x, head_y = 140, 140
    draw.ellipse([head_x - 12, head_y, head_x + 12, head_y + 24], fill=PALETTE['accent'])

    # HUGE oversized "architect's suit" - boxy and impressive
    suit_points = [
        (head_x, head_y + 24),        # neck
        (head_x - 75, head_y + 50),   # left shoulder (MASSIVE)
        (head_x - 70, head_y + 120),  # left mid
        (head_x - 60, head_y + 200),  # left lower
        (head_x - 25, head_y + 275),  # left bottom
        (head_x + 25, head_y + 275),  # right bottom
        (head_x + 60, head_y + 200),  # right lower
        (head_x + 70, head_y + 120),  # right mid
        (head_x + 75, head_y + 50),   # right shoulder (MASSIVE)
    ]
    draw.polygon(suit_points, fill=PALETTE['shadow'])

    # Arm extended in grand gesture (pointing at plans)
    draw.line([(head_x + 75, head_y + 80), (head_x + 110, head_y + 200)],
              fill=PALETTE['shadow'], width=12)
    # Hand pointing
    draw.ellipse([head_x + 105, head_y + 195, head_x + 120, head_y + 210],
                fill=PALETTE['shadow'])


def draw_structures_12_exile(img, draw):
    """
    Exile of Structures: alone with failed systems, frameworks collapsing
    Content: Solitary figure amid ruins of structures they built, carrying collapsed blueprints

    Visual: Figure alone with torn blueprint, broken buildings crumbling around them
    """
    # Ruined structures in background - broken, collapsed
    # Left ruin - tilted
    ruin_points = [(40, 200), (70, 180), (75, 320), (45, 330)]
    draw.polygon(ruin_points, fill=PALETTE['shadow'], outline=PALETTE['frame'])

    # Right ruin - partially collapsed
    draw.rectangle([190, 160, 240, 240], fill=PALETTE['shadow'],
                   outline=PALETTE['frame'], width=2)
    # Crack
    draw.line([(215, 160), (220, 240)], fill=PALETTE['primary'], width=4)
    # Broken top
    draw.polygon([(190, 160), (215, 140), (240, 160)], fill=PALETTE['shadow'])

    # Rubble on ground
    for x, y in [(60, 340), (90, 350), (200, 260), (225, 270)]:
        draw.rectangle([x, y, x + 15, y + 10], fill=PALETTE['frame'])

    # THE EXILE - figure hunched, holding torn blueprint
    # Head bowed
    head_x, head_y = 130, 260
    draw.ellipse([head_x - 15, head_y, head_x + 15, head_y + 30], fill=PALETTE['accent'])

    # Body hunched forward
    body_points = [
        (head_x, head_y + 30),
        (head_x - 30, head_y + 50),
        (head_x - 35, head_y + 120),
        (head_x - 20, head_y + 160),
        (head_x + 20, head_y + 160),
        (head_x + 35, head_y + 120),
        (head_x + 30, head_y + 50)
    ]
    draw.polygon(body_points, fill=PALETTE['frame'])

    # Torn blueprint held in hands (ripped, failing)
    # Top piece
    draw.polygon([(head_x - 40, head_y + 100), (head_x - 20, head_y + 90),
                 (head_x - 15, head_y + 130), (head_x - 45, head_y + 135)],
                fill=PALETTE['primary'], outline=PALETTE['grid'])
    # Bottom piece (torn away)
    draw.polygon([(head_x - 42, head_y + 138), (head_x - 12, head_y + 133),
                 (head_x - 10, head_y + 155), (head_x - 50, head_y + 160)],
                fill=PALETTE['primary'], outline=PALETTE['grid'])
    # Tear mark
    draw.line([(head_x - 43, head_y + 136), (head_x - 14, head_y + 131)],
             fill=PALETTE['shadow'], width=2)


def draw_structures_13_giant(img, draw):
    """
    Giant of Structures: authentic architectural vision, collaborative building
    Content: Figure at full height designing with others visible, structures that contain without confining

    Visual: Tall figure working alongside others, building that opens up rather than closes in
    """
    # Background: Open, inviting structure (contains without confining)
    # Framework that creates space rather than walls
    draw.line([(60, 100), (60, 300)], fill=PALETTE['frame'], width=3)  # left pillar
    draw.line([(220, 100), (220, 300)], fill=PALETTE['frame'], width=3)  # right pillar
    draw.line([(60, 100), (220, 100)], fill=PALETTE['frame'], width=3)  # top beam
    # NO walls - just structure creating space

    # Collaborative elements - multiple people working together
    # Person on left
    draw.ellipse([75, 260, 90, 275], fill=PALETTE['accent'])
    draw.rectangle([78, 275, 87, 300], fill=PALETTE['secondary'])

    # Person on right
    draw.ellipse([195, 270, 210, 285], fill=PALETTE['accent'])
    draw.rectangle([198, 285, 207, 310], fill=PALETTE['secondary'])

    # THE GIANT - tall figure in center, at full height
    head_x, head_y = 140, 180

    # Head proportional (not tiny - authentic self)
    draw.ellipse([head_x - 15, head_y, head_x + 15, head_y + 30], fill=PALETTE['accent'])

    # Body upright, confident but not oversized - natural proportion
    body_points = [
        (head_x, head_y + 30),         # neck
        (head_x - 35, head_y + 55),    # left shoulder
        (head_x - 40, head_y + 130),   # left mid
        (head_x - 35, head_y + 200),   # left hip
        (head_x - 15, head_y + 320),   # left foot
        (head_x + 15, head_y + 320),   # right foot
        (head_x + 35, head_y + 200),   # right hip
        (head_x + 40, head_y + 130),   # right mid
        (head_x + 35, head_y + 55),    # right shoulder
    ]
    draw.polygon(body_points, fill=PALETTE['frame'])

    # Arms outstretched in collaborative gesture (not commanding, but inviting)
    # Left arm reaching to left person
    draw.line([(head_x - 35, head_y + 80), (85, head_y + 60)],
             fill=PALETTE['frame'], width=8)
    # Right arm reaching to right person
    draw.line([(head_x + 35, head_y + 80), (200, head_y + 70)],
             fill=PALETTE['frame'], width=8)

    # Blueprint between them on ground (collaborative design)
    draw.rectangle([100, 330, 180, 370], fill=PALETTE['primary'],
                   outline=PALETTE['grid'], width=1)
    bvt.draw_grid_pattern(draw, (105, 335, 175, 365), 10, PALETTE['grid'])


# Main generation function
def generate_card(rank):
    """Generate a specific Structures card by rank (0-13)"""
    img = bvt.create_canvas(PALETTE['primary'])
    draw = ImageDraw.Draw(img)

    # Subtle grid background for all cards
    bvt.draw_grid_pattern(draw, (15, 15, WIDTH - 15, HEIGHT - 15), 40, PALETTE['grid'])

    # Draw the specific card
    card_functions = [
        draw_structures_0_ace,
        draw_structures_1_two,
        draw_structures_2_three,
        draw_structures_3_four,
        draw_structures_4_five,
        draw_structures_5_six,
        draw_structures_6_seven,
        draw_structures_7_eight,
        draw_structures_8_nine,
        draw_structures_9_ten,
        draw_structures_10_observer,
        draw_structures_11_pretender,
        draw_structures_12_exile,
        draw_structures_13_giant,
    ]

    if 0 <= rank <= 13:
        card_functions[rank](img, draw)

    return img


def main():
    """Generate all 14 Structures cards with custom pixel art"""
    print("Generating custom Structures suit cards...\n")

    output_dir = '/home/user/claude_skills/tarot/decks/byrne/cards'
    os.makedirs(output_dir, exist_ok=True)

    card_names = [
        "Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
        "Eight", "Nine", "Ten", "Observer", "Pretender", "Exile", "Giant"
    ]

    for rank in range(14):
        print(f"  [{rank + 1}/14] {card_names[rank]} of Structures...")
        img = generate_card(rank)
        output_path = os.path.join(output_dir, f'structures-{rank:02d}.png')
        img.save(output_path)

    print(f"\n✓ All 14 Structures cards generated!")
    print(f"  Location: {output_dir}/structures-*.png")


if __name__ == '__main__':
    main()
