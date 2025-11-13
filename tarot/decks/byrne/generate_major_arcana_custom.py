#!/usr/bin/env python3
"""
Custom pixel art generation for the Major Arcana
Each card is hand-crafted to tell its unique story
The journey from anxious observation to embodied joy
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


def get_palette(card_number):
    """Get the appropriate palette based on card position in the journey"""
    if card_number <= 7:
        return bvt.MajorArcanaColors.EARLY
    elif card_number <= 14:
        return bvt.MajorArcanaColors.MIDDLE
    else:
        return bvt.MajorArcanaColors.LATE


def draw_major_0(img, draw):
    """
    0: Uh-Oh, Love Comes to Town - Innocence, arrival, naïve entry
    Content: A figure stepping through a doorway into bright light, slightly awkward posture
    """
    palette = get_palette(0)

    # Doorway frame
    draw.rectangle([60, 80, 100, 340], fill=palette['shadow'])  # Left
    draw.rectangle([180, 80, 220, 340], fill=palette['shadow'])  # Right
    draw.rectangle([60, 80, 220, 120], fill=palette['shadow'])  # Top

    # Bright light beyond the door
    for y in range(120, 340):
        t = (y - 120) / 220
        brightness = int(255 - (50 * t))
        draw.line([(100, y), (180, y)], fill=(brightness, brightness, brightness - 20))

    # City silhouette in the distance
    city_shapes = [(110, 200, 130, 250), (145, 180, 165, 250), (170, 190, 185, 250)]
    for x1, y1, x2, y2 in city_shapes:
        draw.rectangle([x1, y1, x2, y2], fill=palette['accent'])

    # Figure stepping through - awkward posture
    fig_x, fig_y = 140, 280

    # Head
    draw.ellipse([fig_x - 14, fig_y - 80, fig_x + 14, fig_y - 52], fill=palette['secondary'])

    # Body slightly off-balance
    body_points = [
        (fig_x - 2, fig_y - 52),
        (fig_x - 24, fig_y - 28),
        (fig_x - 22, fig_y + 20),
        (fig_x + 18, fig_y + 20),
        (fig_x + 20, fig_y - 28)
    ]
    draw.polygon(body_points, fill=palette['primary'])

    # Suitcase in hand
    draw.rectangle([fig_x + 20, fig_y - 10, fig_x + 38, fig_y + 10],
                   fill=palette['accent'], outline=palette['shadow'], width=2)
    # Handle
    draw.arc([fig_x + 23, fig_y - 18, fig_x + 35, fig_y - 8], 0, 180,
            fill=palette['shadow'], width=2)

    # One foot forward (stepping)
    draw.ellipse([fig_x + 10, fig_y + 20, fig_x + 22, fig_y + 28], fill=palette['secondary'])


def draw_major_1(img, draw):
    """
    1: Psycho Killer - The voice in your head, self-observation taken to extreme
    Content: A mirror reflecting a face that's slightly off, eyes watching eyes
    """
    palette = get_palette(1)

    # Mirror frame
    mirror_x, mirror_y = WIDTH // 2, HEIGHT // 2
    draw.rectangle([mirror_x - 80, mirror_y - 100, mirror_x + 80, mirror_y + 100],
                   fill=palette['primary'], outline=palette['shadow'], width=4)

    # Face in mirror - slightly distorted
    face_x, face_y = mirror_x, mirror_y

    # Head
    draw.ellipse([face_x - 35, face_y - 50, face_x + 35, face_y + 50], fill=palette['secondary'])

    # Eyes - INTENSE, watching
    # Left eye
    draw.ellipse([face_x - 22, face_y - 15, face_x - 8, face_y - 1], fill=(255, 255, 255))
    draw.ellipse([face_x - 18, face_y - 12, face_x - 12, face_y - 6], fill=(0, 0, 0))

    # Right eye (slightly off)
    draw.ellipse([face_x + 8, face_y - 18, face_x + 22, face_y - 4], fill=(255, 255, 255))
    draw.ellipse([face_x + 12, face_y - 15, face_x + 18, face_y - 9], fill=(0, 0, 0))

    # Mouth - uncertain
    draw.arc([face_x - 18, face_y + 10, face_x + 18, face_y + 30], 0, 180,
            fill=palette['shadow'], width=3)

    # Figure outside mirror looking in
    viewer_x, viewer_y = WIDTH // 2, HEIGHT - 60

    # Back of head
    draw.ellipse([viewer_x - 28, viewer_y - 25, viewer_x + 28, viewer_y + 10],
                fill=palette['accent'])

    # Shoulders
    draw.rectangle([viewer_x - 40, viewer_y + 10, viewer_x + 40, viewer_y + 40],
                   fill=palette['accent'])


def draw_major_2(img, draw):
    """
    2: Don't Worry About the Government - Systems as comfort, rules for living
    Content: A neat house with visible blueprints overlaid, orderly streets
    """
    palette = get_palette(2)

    # Grid background
    bvt.draw_grid_pattern(draw, (20, 20, WIDTH - 20, HEIGHT - 20), 30, palette['shadow'])

    # House - neat and orderly
    house_x, house_y = WIDTH // 2, HEIGHT // 2 + 20

    # Roof
    roof_points = [(house_x, house_y - 60), (house_x - 60, house_y - 20), (house_x + 60, house_y - 20)]
    draw.polygon(roof_points, fill=palette['accent'])

    # Walls
    draw.rectangle([house_x - 60, house_y - 20, house_x + 60, house_y + 80],
                   fill=palette['secondary'], outline=palette['shadow'], width=3)

    # Windows - perfectly aligned
    draw.rectangle([house_x - 45, house_y, house_x - 25, house_y + 25],
                   fill=palette['highlight'])
    draw.rectangle([house_x + 25, house_y, house_x + 45, house_y + 25],
                   fill=palette['highlight'])

    # Door
    draw.rectangle([house_x - 15, house_y + 35, house_x + 15, house_y + 80],
                   fill=palette['primary'], outline=palette['shadow'], width=2)

    # Blueprint overlay - showing the system
    for offset in [-70, 70]:
        draw.line([(house_x + offset, house_y - 80), (house_x + offset, house_y + 100)],
                 fill=palette['shadow'], width=1)

    # Dimension lines
    draw.line([(house_x - 70, house_y - 70), (house_x + 70, house_y - 70)],
             fill=palette['accent'], width=2)
    draw.line([(house_x - 70, house_y - 75), (house_x - 70, house_y - 65)],
             fill=palette['accent'], width=2)
    draw.line([(house_x + 70, house_y - 75), (house_x + 70, house_y - 65)],
             fill=palette['accent'], width=2)


def draw_major_3(img, draw):
    """
    3: The Big Country - The view from above, detached observation
    Content: An airplane window view, landscape geometrically arranged below
    """
    palette = get_palette(3)

    # Airplane window frame
    window_x, window_y = WIDTH // 2 + 20, HEIGHT // 2
    draw.ellipse([window_x - 90, window_y - 120, window_x + 90, window_y + 120],
                fill=palette['highlight'])
    draw.ellipse([window_x - 80, window_y - 110, window_x + 80, window_y + 110],
                fill=palette['primary'])

    # View through window - geometric landscape from above
    # Fields
    field_colors = [palette['secondary'], palette['accent'], palette['ground']]
    for i, y_start in enumerate([window_y - 90, window_y - 30, window_y + 30]):
        color = field_colors[i % 3]
        draw.rectangle([window_x - 70, y_start, window_x + 70, y_start + 50], fill=color)

    # Roads (grid pattern)
    for y in range(window_y - 90, window_y + 90, 40):
        draw.line([(window_x - 70, y), (window_x + 70, y)], fill=palette['shadow'], width=2)

    for x in range(window_x - 60, window_x + 60, 45):
        draw.line([(x, window_y - 90), (x, window_y + 90)], fill=palette['shadow'], width=2)

    # Edge of seat/interior visible
    draw.rectangle([20, HEIGHT - 80, window_x - 100, HEIGHT - 20],
                   fill=palette['accent'])


def draw_major_4(img, draw):
    """
    4: Life During Wartime - Intensity, urgency, survival mode
    Content: Dense urban environment, moving through crowds with purpose
    """
    palette = get_palette(4)

    # Dense urban background - buildings crowding
    buildings = [
        (20, 100, 60, 280),
        (65, 80, 95, 280),
        (100, 120, 130, 280),
        (150, 90, 180, 280),
        (185, 110, 215, 280),
        (220, 85, 260, 280)
    ]

    for i, (x1, y1, x2, y2) in enumerate(buildings):
        color = palette['shadow'] if i % 2 == 0 else palette['accent']
        draw.rectangle([x1, y1, x2, y2], fill=color, outline=palette['shadow'], width=1)
        # Windows
        for wy in range(y1 + 15, y2, 20):
            for wx in range(x1 + 5, x2 - 5, 12):
                draw.rectangle([wx, wy, wx + 5, wy + 8], fill=palette['highlight'])

    # Crowd - small figures at street level
    for x in range(30, WIDTH - 30, 25):
        y = 290 + (x % 3) * 10
        # Tiny figures
        draw.ellipse([x - 4, y, x + 4, y + 8], fill=palette['secondary'])
        draw.rectangle([x - 3, y + 8, x + 3, y + 20], fill=palette['primary'])

    # Central figure - moving with purpose
    fig_x, fig_y = WIDTH // 2, 320

    # Head
    draw.ellipse([fig_x - 12, fig_y - 50, fig_x + 12, fig_y - 26], fill=palette['secondary'])

    # Body leaning forward - urgent posture
    body_points = [
        (fig_x + 5, fig_y - 26),
        (fig_x - 18, fig_y - 5),
        (fig_x - 15, fig_y + 30),
        (fig_x + 15, fig_y + 30),
        (fig_x + 20, fig_y - 5)
    ]
    draw.polygon(body_points, fill=palette['primary'])

    # Motion lines
    for offset in [10, 20, 30]:
        draw.line([(fig_x - 20 - offset, fig_y - 10), (fig_x - 25 - offset, fig_y - 10)],
                 fill=palette['accent'], width=2)


def draw_major_5(img, draw):
    """
    5: Heaven - Perfection anxiety, stasis
    Content: A still, perfect room with a band playing on endless repeat, beautiful and suffocating
    """
    palette = get_palette(5)

    # Perfect room - too perfect
    # Floor
    for i in range(8):
        y = HEIGHT - 100 + i * 12
        color = palette['primary'] if i % 2 == 0 else palette['secondary']
        draw.rectangle([0, y, WIDTH, y + 12], fill=color)

    # Walls with perfect pattern
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT - 100)], fill=palette['shadow'], width=1)

    # Band frozen in perfect pose - three figures
    for i, x in enumerate([70, 140, 210]):
        y = HEIGHT - 130

        # Head
        draw.ellipse([x - 10, y - 40, x + 10, y - 20], fill=palette['accent'])

        # Body - stiff, identical
        draw.rectangle([x - 12, y - 20, x + 12, y + 15], fill=palette['secondary'])

        # Arms in playing position - frozen
        if i == 0:  # Guitar
            draw.line([(x - 12, y - 5), (x - 25, y)], fill=palette['secondary'], width=5)
            draw.rectangle([x - 30, y, x - 20, y + 15], fill=palette['accent'])
        elif i == 1:  # Singing
            draw.ellipse([x - 6, y - 8, x + 6, y - 2], fill=(0, 0, 0))  # Mouth frozen open
        else:  # Drums
            draw.line([(x + 12, y - 5), (x + 22, y - 8)], fill=palette['secondary'], width=4)

    # Repeat symbols showing endless loop
    for y in [60, 120, 180]:
        draw.ellipse([WIDTH - 40, y - 8, WIDTH - 25, y + 8], fill=palette['accent'])
        draw.line([(WIDTH - 32, y - 8), (WIDTH - 32, y + 8)], fill=palette['shadow'], width=2)


def draw_major_6(img, draw):
    """
    6: Houses in Motion - Beginning to move, bodies entering
    Content: Buildings that seem to breathe, architectural forms in flux
    """
    palette = get_palette(6)

    # Buildings with motion - slightly distorted
    # Left building - leaning
    left_building = [
        (40, 180),
        (50, 100),
        (90, 100),
        (95, 180),
        (95, 320),
        (40, 320)
    ]
    draw.polygon(left_building, fill=palette['secondary'], outline=palette['shadow'], width=2)

    # Middle building - breathing (waves)
    for i in range(8):
        y_start = 120 + i * 25
        points = []
        for x in range(120, 170, 5):
            wave = 5 * math.sin((x - 120 + i * 10) / 10)
            points.append((x + wave, y_start))
        for x in range(170, 120, -5):
            wave = 5 * math.sin((x - 120 + i * 10) / 10)
            points.append((x + wave, y_start + 20))
        if len(points) > 2:
            draw.polygon(points, fill=palette['accent'] if i % 2 == 0 else palette['secondary'])

    # Right building - shifting
    right_building = [
        (200, 140),
        (240, 130),
        (245, 320),
        (195, 320)
    ]
    draw.polygon(right_building, fill=palette['secondary'], outline=palette['shadow'], width=2)

    # Motion lines around buildings
    for y in [90, 150, 210, 270]:
        # Horizontal motion lines
        draw.line([(25, y), (35, y)], fill=palette['accent'], width=2)
        draw.line([(245, y), (255, y)], fill=palette['accent'], width=2)


def draw_major_7(img, draw):
    """
    7: Once in a Lifetime - The recognition moment
    Content: A figure looking at their reflection in water, surprised, questioning gesture
    """
    palette = get_palette(7)

    # Water surface - horizontal line
    water_y = HEIGHT // 2 + 20
    draw.line([(0, water_y), (WIDTH, water_y)], fill=palette['accent'], width=3)

    # Ripples
    for i in range(1, 6):
        draw.ellipse([WIDTH//2 - 40 - i*15, water_y - i*8,
                     WIDTH//2 + 40 + i*15, water_y + i*8],
                    outline=palette['shadow'], width=1)

    # Figure above water
    fig_x, fig_y = WIDTH // 2, water_y - 80

    # Head
    draw.ellipse([fig_x - 16, fig_y, fig_x + 16, fig_y + 32], fill=palette['secondary'])

    # Eyes wide - surprised
    draw.ellipse([fig_x - 10, fig_y + 10, fig_x - 2, fig_y + 18], fill=(255, 255, 255))
    draw.ellipse([fig_x + 2, fig_y + 10, fig_x + 10, fig_y + 18], fill=(255, 255, 255))
    draw.ellipse([fig_x - 8, fig_y + 12, fig_x - 4, fig_y + 16], fill=(0, 0, 0))
    draw.ellipse([fig_x + 4, fig_y + 12, fig_x + 8, fig_y + 16], fill=(0, 0, 0))

    # Body
    body = [(fig_x, fig_y + 32), (fig_x - 24, fig_y + 50), (fig_x - 24, fig_y + 90),
            (fig_x + 24, fig_y + 90), (fig_x + 24, fig_y + 50)]
    draw.polygon(body, fill=palette['primary'])

    # Questioning gesture - hand raised
    arm = [(fig_x + 24, fig_y + 55), (fig_x + 50, fig_y + 35),
           (fig_x + 52, fig_y + 42), (fig_x + 26, fig_y + 62)]
    draw.polygon(arm, fill=palette['primary'])

    # Reflection below - distorted
    reflection_y = water_y + 80
    draw.ellipse([fig_x - 14, reflection_y, fig_x + 14, reflection_y + 28],
                fill=palette['shadow'])
    # Wavy body reflection
    refl_body = [(fig_x, reflection_y + 28), (fig_x - 20, reflection_y + 45),
                 (fig_x - 18, reflection_y + 80), (fig_x + 18, reflection_y + 80),
                 (fig_x + 20, reflection_y + 45)]
    draw.polygon(refl_body, fill=palette['accent'])


def draw_major_8(img, draw):
    """
    8: Road to Nowhere - Acceptance of aimlessness, joy in not knowing
    Content: An open highway disappearing into light, travelers dancing as they walk
    """
    palette = get_palette(8)

    # Sky - gradient to light
    for y in range(HEIGHT):
        t = y / HEIGHT
        brightness = int(180 + 75 * (1 - t))
        color = (brightness, brightness, brightness - 20)
        draw.line([(0, y), (WIDTH, y)], fill=color)

    # Road - perspective
    horizon_y = 100
    road_points = [
        (WIDTH // 2 - 80, HEIGHT),
        (WIDTH // 2 + 80, HEIGHT),
        (WIDTH // 2 + 20, horizon_y),
        (WIDTH // 2 - 20, horizon_y)
    ]
    draw.polygon(road_points, fill=palette['shadow'])

    # Center line - dashed
    for y in range(HEIGHT, horizon_y, -40):
        line_width = int(10 - (HEIGHT - y) / 50)
        if line_width > 1:
            draw.line([(WIDTH // 2, y), (WIDTH // 2, y - 20)],
                     fill=palette['highlight'], width=line_width)

    # Figures walking/dancing on the road - getting smaller in distance
    figures_data = [(140, 340, 1.0), (130, 280, 0.7), (135, 220, 0.5), (138, 170, 0.3)]

    for fig_x, fig_y, scale in figures_data:
        head_size = int(14 * scale)
        body_height = int(40 * scale)

        # Head
        draw.ellipse([fig_x - head_size//2, fig_y - body_height - head_size,
                     fig_x + head_size//2, fig_y - body_height],
                    fill=palette['secondary'])

        # Body - dance pose
        if scale > 0.6:
            # Close figures - arms up joyfully
            body_points = [
                (fig_x, fig_y - body_height),
                (fig_x - int(15 * scale), fig_y - int(body_height * 0.6)),
                (fig_x - int(12 * scale), fig_y),
                (fig_x + int(12 * scale), fig_y),
                (fig_x + int(15 * scale), fig_y - int(body_height * 0.6))
            ]
            draw.polygon(body_points, fill=palette['primary'])

            # Arms up
            draw.line([(fig_x, fig_y - int(body_height * 0.7)),
                      (fig_x - int(20 * scale), fig_y - int(body_height * 0.9))],
                     fill=palette['primary'], width=int(6 * scale))
            draw.line([(fig_x, fig_y - int(body_height * 0.7)),
                      (fig_x + int(20 * scale), fig_y - int(body_height * 0.9))],
                     fill=palette['primary'], width=int(6 * scale))
        else:
            # Distant figures - simplified
            draw.rectangle([fig_x - int(8 * scale), fig_y - body_height,
                          fig_x + int(8 * scale), fig_y],
                         fill=palette['primary'])


def draw_major_9(img, draw):
    """
    9: Burning Down the House - Destruction, transformation through fire
    Content: Flames consuming a structure, but inside there's dancing
    """
    palette = get_palette(9)

    # House structure
    draw.rectangle([60, 160, 220, 340], fill=palette['shadow'],
                   outline=palette['accent'], width=3)

    # Roof
    roof = [(60, 160), (140, 100), (220, 160)]
    draw.polygon(roof, fill=palette['shadow'], outline=palette['accent'], width=3)

    # Flames - orange/red rising
    flame_colors = [(255, 100, 0), (255, 150, 0), (255, 200, 50)]

    # Flames from bottom
    for i in range(8):
        x_base = 70 + i * 20
        flame_height = 60 + (i % 3) * 30

        flame_points = [
            (x_base, 340),
            (x_base - 10, 340 - flame_height // 2),
            (x_base, 340 - flame_height),
            (x_base + 10, 340 - flame_height // 2)
        ]
        color = flame_colors[i % 3]
        draw.polygon(flame_points, fill=color)

    # Flames from roof
    for i in range(6):
        x_base = 80 + i * 25
        flame_height = 40 + (i % 2) * 20

        flame_points = [
            (x_base, 160),
            (x_base - 8, 160 - flame_height // 2),
            (x_base, 160 - flame_height),
            (x_base + 8, 160 - flame_height // 2)
        ]
        color = flame_colors[i % 3]
        draw.polygon(flame_points, fill=color)

    # Window showing dancing figure INSIDE
    window_x, window_y = 140, 240
    draw.rectangle([window_x - 30, window_y - 35, window_x + 30, window_y + 35],
                   fill=(255, 200, 100))

    # Dancing figure silhouette
    draw.ellipse([window_x - 10, window_y - 25, window_x + 10, window_y - 10],
                fill=(50, 50, 50))
    draw.rectangle([window_x - 12, window_y - 10, window_x + 12, window_y + 20],
                   fill=(50, 50, 50))
    # Arms up dancing
    draw.line([(window_x, window_y), (window_x - 18, window_y - 15)],
             fill=(50, 50, 50), width=5)
    draw.line([(window_x, window_y), (window_x + 18, window_y - 15)],
             fill=(50, 50, 50), width=5)


def draw_major_10(img, draw):
    """
    10: This Must Be the Place (Naive Melody) - Home found, love as anchor
    Content: Two figures in an embrace, domestic space that feels earned
    """
    palette = get_palette(10)

    # Warm domestic interior
    # Floor
    draw.rectangle([0, HEIGHT - 100, WIDTH, HEIGHT], fill=palette['ground'])

    # Wall with simple decorations
    draw.rectangle([0, 0, WIDTH, HEIGHT - 100], fill=palette['primary'])

    # Simple furniture - table
    draw.rectangle([30, HEIGHT - 130, 100, HEIGHT - 100],
                   fill=palette['accent'])

    # Lamp on table
    draw.rectangle([60, HEIGHT - 170, 70, HEIGHT - 130], fill=palette['secondary'])
    # Lampshade
    lampshade = [(50, HEIGHT - 170), (80, HEIGHT - 170), (75, HEIGHT - 190), (55, HEIGHT - 190)]
    draw.polygon(lampshade, fill=palette['highlight'])

    # Window showing light
    draw.rectangle([200, 80, 260, 160], fill=palette['highlight'],
                   outline=palette['shadow'], width=2)

    # Two figures embracing - central
    fig_x, fig_y = WIDTH // 2 + 10, HEIGHT - 150

    # Left figure
    draw.ellipse([fig_x - 40, fig_y - 70, fig_x - 12, fig_y - 42],
                fill=palette['secondary'])
    left_body = [
        (fig_x - 26, fig_y - 42),
        (fig_x - 42, fig_y - 20),
        (fig_x - 40, fig_y + 30),
        (fig_x - 18, fig_y + 30),
        (fig_x - 20, fig_y - 20)
    ]
    draw.polygon(left_body, fill=palette['accent'])

    # Right figure
    draw.ellipse([fig_x + 12, fig_y - 70, fig_x + 40, fig_y - 42],
                fill=palette['secondary'])
    right_body = [
        (fig_x + 26, fig_y - 42),
        (fig_x + 20, fig_y - 20),
        (fig_x + 18, fig_y + 30),
        (fig_x + 40, fig_y + 30),
        (fig_x + 42, fig_y - 20)
    ]
    draw.polygon(right_body, fill=palette['accent'])

    # Arms embracing
    draw.line([(fig_x - 42, fig_y - 5), (fig_x + 30, fig_y)],
             fill=palette['accent'], width=8)
    draw.line([(fig_x + 42, fig_y - 5), (fig_x - 30, fig_y)],
             fill=palette['accent'], width=8)


def draw_major_11(img, draw):
    """
    11: (Nothing But) Flowers - The end of certainty, civilization questioned
    Content: Vines overtaking a Pizza Hut, nature reclaiming parking lots
    """
    palette = get_palette(11)

    # Building outline (Pizza Hut remnant)
    draw.rectangle([80, 180, 200, 280], fill=palette['shadow'],
                   outline=palette['accent'], width=2)

    # Faded sign
    draw.rectangle([90, 160, 190, 180], fill=palette['accent'])

    # Vines overtaking - organic curves over geometric structure
    vine_color = (60, 140, 60)

    # Main vine from bottom left
    vine_points = []
    for i in range(15):
        x = 30 + i * 15
        y = 320 - i * 20 + 15 * math.sin(i / 2)
        vine_points.append((x, y))

    for i in range(len(vine_points) - 1):
        draw.line([vine_points[i], vine_points[i + 1]], fill=vine_color, width=8)

    # Vine from right
    vine_points2 = []
    for i in range(12):
        x = 250 - i * 15
        y = 330 - i * 18 + 12 * math.sin(i / 2.5)
        vine_points2.append((x, y))

    for i in range(len(vine_points2) - 1):
        draw.line([vine_points2[i], vine_points2[i + 1]], fill=vine_color, width=7)

    # Leaves on vines
    for vx, vy in vine_points[::3]:
        draw.ellipse([vx - 8, vy - 10, vx + 8, vy + 10], fill=(80, 180, 80))

    for vx, vy in vine_points2[::3]:
        draw.ellipse([vx - 8, vy - 10, vx + 8, vy + 10], fill=(80, 180, 80))

    # Flowers blooming
    for fx, fy in [(120, 240), (160, 220), (100, 180)]:
        # Flower center
        draw.ellipse([fx - 8, fy - 8, fx + 8, fy + 8], fill=(255, 200, 0))
        # Petals
        for angle in range(0, 360, 60):
            rad = angle * math.pi / 180
            px = fx + int(15 * math.cos(rad))
            py = fy + int(15 * math.sin(rad))
            draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(255, 100, 150))

    # Grass/wild growth at bottom
    for x in range(0, WIDTH, 15):
        grass_height = 40 + (x % 30)
        draw.line([(x, HEIGHT), (x + (x % 3) - 1, HEIGHT - grass_height)],
                 fill=(70, 160, 70), width=3)


def draw_major_12(img, draw):
    """
    12: Something Ain't Right - Recognition that the old way no longer works
    Content: A figure in a familiar place that now feels off, shadows where there weren't
    """
    palette = get_palette(12)

    # Familiar room - but wrong
    # Floor tiles - slightly skewed
    for i in range(8):
        for j in range(6):
            x = i * 35 + (j % 2) * 3  # Slight offset - feels wrong
            y = HEIGHT - 200 + j * 33
            color = palette['primary'] if (i + j) % 2 == 0 else palette['secondary']
            # Slightly irregular rectangles
            draw.polygon([
                (x, y),
                (x + 32, y + 2),
                (x + 32, y + 32),
                (x - 2, y + 30)
            ], fill=color)

    # Window at wrong angle
    window_points = [
        (180, 90),
        (250, 95),
        (245, 180),
        (175, 175)
    ]
    draw.polygon(window_points, fill=palette['highlight'],
                outline=palette['shadow'], width=2)

    # Shadows in wrong places
    # Shadow on floor - shouldn't be there
    shadow1 = [(60, HEIGHT - 160), (120, HEIGHT - 150),
               (115, HEIGHT - 100), (55, HEIGHT - 110)]
    draw.polygon(shadow1, fill=palette['shadow'])

    # Shadow on wall - wrong direction
    shadow2 = [(30, 120), (70, 140), (65, 220), (25, 200)]
    draw.polygon(shadow2, fill=palette['shadow'])

    # Figure in center - confused posture
    fig_x, fig_y = 100, HEIGHT - 110

    # Head - looking around
    draw.ellipse([fig_x - 14, fig_y - 60, fig_x + 14, fig_y - 32],
                fill=palette['accent'])

    # Body
    body = [(fig_x, fig_y - 32), (fig_x - 20, fig_y - 10),
            (fig_x - 18, fig_y + 30), (fig_x + 18, fig_y + 30),
            (fig_x + 20, fig_y - 10)]
    draw.polygon(body, fill=palette['secondary'])

    # One arm reaching out - uncertain
    draw.line([(fig_x + 20, fig_y - 5), (fig_x + 40, fig_y - 15)],
             fill=palette['secondary'], width=7)


def draw_major_13(img, draw):
    """
    13: The Civil Wars - Internal conflict, battle with yourself
    Content: A figure facing their own shadow, battlefield imagery at intimate scale
    """
    palette = get_palette(13)

    # Ground - divided
    left_ground = [(0, HEIGHT - 80), (WIDTH // 2, HEIGHT - 80),
                   (WIDTH // 2, HEIGHT), (0, HEIGHT)]
    draw.polygon(left_ground, fill=palette['ground'])

    right_ground = [(WIDTH // 2, HEIGHT - 80), (WIDTH, HEIGHT - 80),
                    (WIDTH, HEIGHT), (WIDTH // 2, HEIGHT)]
    draw.polygon(right_ground, fill=palette['shadow'])

    # Dividing line - the battlefield
    draw.line([(WIDTH // 2, 100), (WIDTH // 2, HEIGHT)],
             fill=palette['accent'], width=4)

    # Figure on left - facing right
    left_fig_x, left_fig_y = WIDTH // 2 - 50, HEIGHT - 120

    draw.ellipse([left_fig_x - 14, left_fig_y - 60, left_fig_x + 14, left_fig_y - 32],
                fill=palette['secondary'])

    left_body = [
        (left_fig_x, left_fig_y - 32),
        (left_fig_x - 20, left_fig_y - 10),
        (left_fig_x - 18, left_fig_y + 40),
        (left_fig_x + 18, left_fig_y + 40),
        (left_fig_x + 22, left_fig_y - 10)
    ]
    draw.polygon(left_body, fill=palette['primary'])

    # Arm reaching toward divide
    draw.line([(left_fig_x + 22, left_fig_y), (left_fig_x + 45, left_fig_y - 10)],
             fill=palette['primary'], width=8)

    # Shadow/mirror figure on right - facing left
    right_fig_x, right_fig_y = WIDTH // 2 + 50, HEIGHT - 120

    draw.ellipse([right_fig_x - 14, right_fig_y - 60, right_fig_x + 14, right_fig_y - 32],
                fill=palette['shadow'])

    right_body = [
        (right_fig_x, right_fig_y - 32),
        (right_fig_x - 22, right_fig_y - 10),
        (right_fig_x - 18, right_fig_y + 40),
        (right_fig_x + 18, right_fig_y + 40),
        (right_fig_x + 20, right_fig_y - 10)
    ]
    draw.polygon(right_body, fill=palette['accent'])

    # Arm reaching toward divide
    draw.line([(right_fig_x - 22, right_fig_y), (right_fig_x - 45, right_fig_y - 10)],
             fill=palette['accent'], width=8)

    # Tension lines between them
    for y in [left_fig_y - 40, left_fig_y - 10, left_fig_y + 20]:
        draw.line([(left_fig_x + 25, y), (right_fig_x - 25, y)],
                 fill=palette['highlight'], width=1)


def draw_major_14(img, draw):
    """
    14: A Self-Made Man - Confronting what you've constructed
    Content: A figure looking at their own blueprint or statue of themselves
    """
    palette = get_palette(14)

    # Blueprint background
    bvt.draw_grid_pattern(draw, (100, 50, WIDTH - 20, HEIGHT - 100), 25, palette['shadow'])

    # Statue/construction of self - monument
    statue_x, statue_y = WIDTH - 100, HEIGHT // 2

    # Statue head (larger, idealized)
    draw.ellipse([statue_x - 20, statue_y - 80, statue_x + 20, statue_y - 40],
                fill=palette['accent'])

    # Statue body (heroic pose)
    statue_body = [
        (statue_x, statue_y - 40),
        (statue_x - 30, statue_y - 10),
        (statue_x - 28, statue_y + 60),
        (statue_x + 28, statue_y + 60),
        (statue_x + 30, statue_y - 10)
    ]
    draw.polygon(statue_body, fill=palette['secondary'])

    # Pedestal
    draw.rectangle([statue_x - 35, statue_y + 60, statue_x + 35, statue_y + 90],
                   fill=palette['ground'])

    # Actual figure looking at it - smaller, uncertain
    fig_x, fig_y = 70, HEIGHT - 130

    # Head
    draw.ellipse([fig_x - 14, fig_y - 60, fig_x + 14, fig_y - 32],
                fill=palette['secondary'])

    # Body - hunched, contemplative
    body = [
        (fig_x, fig_y - 32),
        (fig_x - 20, fig_y - 12),
        (fig_x - 18, fig_y + 40),
        (fig_x + 18, fig_y + 40),
        (fig_x + 20, fig_y - 12)
    ]
    draw.polygon(body, fill=palette['primary'])

    # Hand to chin - thinking
    draw.ellipse([fig_x + 18, fig_y - 20, fig_x + 28, fig_y - 10],
                fill=palette['primary'])

    # Sight line from figure to statue
    draw.line([(fig_x + 14, fig_y - 40), (statue_x - 20, statue_y - 60)],
             fill=palette['accent'], width=1)


def draw_major_15(img, draw):
    """
    15: Broken Things - Acceptance of limitation, death, endings
    Content: Shattered objects arranged beautifully, light through cracks
    """
    palette = get_palette(15)

    # Dark background
    for y in range(HEIGHT):
        t = y / HEIGHT
        darkness = int(40 + 30 * t)
        draw.line([(0, y), (WIDTH, y)], fill=(darkness, darkness, darkness + 10))

    # Broken vase/object - center
    vase_x, vase_y = WIDTH // 2, HEIGHT // 2

    # Fragments of a vase
    fragments = [
        # Left piece
        [(vase_x - 50, vase_y - 20), (vase_x - 30, vase_y - 40),
         (vase_x - 25, vase_y + 20), (vase_x - 45, vase_y + 30)],
        # Right piece
        [(vase_x + 30, vase_y - 40), (vase_x + 50, vase_y - 25),
         (vase_x + 48, vase_y + 25), (vase_x + 28, vase_y + 20)],
        # Bottom piece
        [(vase_x - 20, vase_y + 25), (vase_x + 20, vase_y + 25),
         (vase_x + 15, vase_y + 60), (vase_x - 15, vase_y + 60)],
        # Top piece
        [(vase_x - 15, vase_y - 60), (vase_x + 15, vase_y - 60),
         (vase_x + 10, vase_y - 35), (vase_x - 10, vase_y - 35)]
    ]

    for fragment in fragments:
        draw.polygon(fragment, fill=palette['accent'], outline=palette['highlight'], width=2)

    # Light streaming through the cracks
    light_rays = [
        (vase_x - 35, vase_y - 15),
        (vase_x + 35, vase_y - 10),
        (vase_x, vase_y + 40)
    ]

    for lx, ly in light_rays:
        # Ray of light
        ray_points = [
            (lx - 3, ly),
            (lx + 3, ly),
            (lx + 15, ly - 80),
            (lx + 9, ly - 80)
        ]
        draw.polygon(ray_points, fill=(255, 255, 200, 100))

    # Hands holding pieces gently
    # Left hand
    draw.ellipse([vase_x - 55, vase_y + 35, vase_x - 35, vase_y + 50],
                fill=palette['secondary'])

    # Right hand
    draw.ellipse([vase_x + 35, vase_y + 35, vase_x + 55, vase_y + 50],
                fill=palette['secondary'])


def draw_major_16(img, draw):
    """
    16: Tiny Apocalypse - Personal catastrophe, the tower moment
    Content: A room mid-collapse, furniture floating, domestic disaster
    """
    palette = get_palette(16)

    # Tilted room frame
    room_points = [
        (30, 80), (250, 100), (240, 350), (20, 340)
    ]
    draw.polygon(room_points, outline=palette['shadow'], width=3)

    # Floor - tilted
    draw.line([(30, 280), (240, 290)], fill=palette['ground'], width=8)

    # Furniture floating/falling
    # Chair - tilted
    chair_points = [
        (70, 180), (100, 178), (98, 230), (95, 250), (75, 252), (72, 230)
    ]
    draw.polygon(chair_points, fill=palette['accent'],
                outline=palette['shadow'], width=2)
    # Chair back
    draw.line([(73, 180), (70, 150)], fill=palette['accent'], width=6)
    draw.line([(98, 178), (95, 148)], fill=palette['accent'], width=6)

    # Table - upended
    table_points = [
        (160, 140), (220, 145), (215, 160), (155, 155)
    ]
    draw.polygon(table_points, fill=palette['secondary'],
                outline=palette['shadow'], width=2)
    # Table legs
    for x in [160, 215]:
        draw.line([(x, 155), (x + 5, 190)], fill=palette['secondary'], width=5)

    # Picture frame falling
    frame_points = [
        (180, 200), (230, 205), (228, 240), (178, 235)
    ]
    draw.polygon(frame_points, fill=palette['highlight'],
                outline=palette['accent'], width=3)

    # Motion lines showing movement
    for item_x, item_y in [(85, 200), (190, 160), (200, 220)]:
        for offset in [5, 10, 15]:
            draw.line([(item_x - offset, item_y), (item_x - offset - 8, item_y)],
                     fill=palette['accent'], width=2)

    # Cracks in the walls
    crack_lines = [
        [(30, 120), (80, 140), (120, 180)],
        [(200, 100), (180, 150), (160, 200)],
        [(100, 320), (130, 280), (150, 250)]
    ]

    for crack in crack_lines:
        for i in range(len(crack) - 1):
            draw.line([crack[i], crack[i + 1]], fill=palette['shadow'], width=3)


def draw_major_17(img, draw):
    """
    17: One Fine Day - Hope returns, the star after darkness
    Content: Dawn breaking, a figure looking toward horizon, posture of readiness
    """
    palette = get_palette(17)

    # Dawn sky - gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        if t < 0.3:
            # Dark blue to light blue
            r = int(40 + 140 * (t / 0.3))
            g = int(50 + 150 * (t / 0.3))
            b = int(80 + 120 * (t / 0.3))
        else:
            # Light blue to warm horizon
            sub_t = (t - 0.3) / 0.7
            r = int(180 + 75 * sub_t)
            g = int(200 + 55 * sub_t)
            b = int(200 - 50 * sub_t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Horizon line
    horizon_y = HEIGHT - 150
    draw.line([(0, horizon_y), (WIDTH, horizon_y)], fill=(255, 200, 100), width=3)

    # Sun rising
    sun_y = horizon_y - 20
    for radius in range(50, 30, -5):
        brightness = 255 - (50 - radius) * 3
        color = (brightness, brightness - 50, max(0, brightness - 100))
        draw.ellipse([WIDTH - 80 - radius, sun_y - radius,
                     WIDTH - 80 + radius, sun_y + radius],
                    fill=color)

    # Sun rays
    for angle in range(0, 360, 30):
        rad = angle * math.pi / 180
        start_x = WIDTH - 80 + int(35 * math.cos(rad))
        start_y = sun_y + int(35 * math.sin(rad))
        end_x = WIDTH - 80 + int(70 * math.cos(rad))
        end_y = sun_y + int(70 * math.sin(rad))
        draw.line([(start_x, start_y), (end_x, end_y)],
                 fill=(255, 220, 150), width=2)

    # Road ahead
    road_points = [
        (80, HEIGHT), (160, HEIGHT),
        (WIDTH - 90, horizon_y), (WIDTH - 70, horizon_y)
    ]
    draw.polygon(road_points, fill=(120, 120, 140))

    # Figure standing, facing dawn - ready
    fig_x, fig_y = 120, HEIGHT - 80

    # Head
    draw.ellipse([fig_x - 14, fig_y - 70, fig_x + 14, fig_y - 42],
                fill=palette['secondary'])

    # Body - upright, ready
    body = [
        (fig_x, fig_y - 42),
        (fig_x - 22, fig_y - 20),
        (fig_x - 20, fig_y + 35),
        (fig_x + 20, fig_y + 35),
        (fig_x + 22, fig_y - 20)
    ]
    draw.polygon(body, fill=palette['primary'])

    # One arm shielding eyes, looking at dawn
    draw.line([(fig_x + 22, fig_y - 15), (fig_x + 14, fig_y - 45)],
             fill=palette['primary'], width=8)


def draw_major_18(img, draw):
    """
    18: Lazarus - Resurrection, return from death
    Content: A figure standing from prone position, light from above or below
    """
    palette = get_palette(18)

    # Dark surroundings
    for y in range(HEIGHT):
        t = y / HEIGHT
        darkness = int(30 + 20 * t)
        draw.line([(0, y), (WIDTH, y)], fill=(darkness, darkness, darkness + 15))

    # Ground
    draw.rectangle([0, HEIGHT - 100, WIDTH, HEIGHT], fill=(50, 50, 60))

    # Divine light from above - concentrated beam
    light_center_x = WIDTH // 2
    light_center_y = 0

    # Light rays
    for i in range(15):
        angle = 70 + i * 2.5
        rad = angle * math.pi / 180
        length = 300 + i * 10
        end_x = light_center_x + int(length * math.cos(rad))
        end_y = light_center_y + int(length * math.sin(rad))

        brightness = 255 - i * 10
        color = (brightness, brightness, min(255, brightness + 20))
        draw.line([(light_center_x, light_center_y), (end_x, end_y)],
                 fill=color, width=3)

    # Figure rising - dramatic pose
    fig_x, fig_y = WIDTH // 2, HEIGHT - 150

    # Head tilted back - looking up
    draw.ellipse([fig_x - 16, fig_y - 50, fig_x + 16, fig_y - 22],
                fill=palette['accent'])

    # Body rising from ground
    body = [
        (fig_x, fig_y - 22),
        (fig_x - 26, fig_y),
        (fig_x - 24, fig_y + 60),
        (fig_x + 24, fig_y + 60),
        (fig_x + 26, fig_y)
    ]
    draw.polygon(body, fill=palette['primary'])

    # Arms outstretched - resurrection gesture
    # Left arm
    draw.line([(fig_x - 26, fig_y + 5), (fig_x - 60, fig_y - 15)],
             fill=palette['primary'], width=10)

    # Right arm
    draw.line([(fig_x + 26, fig_y + 5), (fig_x + 60, fig_y - 15)],
             fill=palette['primary'], width=10)

    # Shadow of previous position (prone)
    shadow_figure = [
        (fig_x - 50, fig_y + 70),
        (fig_x + 50, fig_y + 70),
        (fig_x + 45, fig_y + 90),
        (fig_x - 45, fig_y + 90)
    ]
    draw.polygon(shadow_figure, fill=(30, 30, 35))


def draw_major_19(img, draw):
    """
    19: I Dance Like This - Embodied declaration, authenticity found
    Content: A body mid-dance, suit jacket flying, feet off ground, face unselfconscious
    """
    palette = get_palette(19)

    # Warm energetic background
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2 - 20, 180,
                       palette['highlight'], palette['primary'])

    # Stage floor
    floor_points = [
        (40, HEIGHT - 60), (240, HEIGHT - 60),
        (230, HEIGHT - 20), (50, HEIGHT - 20)
    ]
    draw.polygon(floor_points, fill=palette['ground'])

    # Figure MID-LEAP - dynamic
    fig_x, fig_y = WIDTH // 2, HEIGHT // 2 - 20

    # Head - tilted, joyful
    draw.ellipse([fig_x - 16, fig_y - 80, fig_x + 16, fig_y - 48],
                fill=palette['accent'])

    # Face - simple but expressive
    draw.arc([fig_x - 12, fig_y - 70, fig_x + 12, fig_y - 55],
            0, 180, fill=(0, 0, 0), width=3)  # Smile

    # Body in motion - twisted
    body = [
        (fig_x + 5, fig_y - 48),
        (fig_x - 20, fig_y - 25),
        (fig_x - 15, fig_y + 35),
        (fig_x + 20, fig_y + 30),
        (fig_x + 25, fig_y - 20)
    ]
    draw.polygon(body, fill=palette['secondary'])

    # Big suit jacket - FLYING OFF
    jacket_left = [
        (fig_x - 20, fig_y - 20),
        (fig_x - 70, fig_y - 40),
        (fig_x - 75, fig_y + 10),
        (fig_x - 25, fig_y + 20)
    ]
    draw.polygon(jacket_left, fill=palette['primary'])

    jacket_right = [
        (fig_x + 25, fig_y - 15),
        (fig_x + 75, fig_y - 35),
        (fig_x + 80, fig_y + 15),
        (fig_x + 25, fig_y + 25)
    ]
    draw.polygon(jacket_right, fill=palette['primary'])

    # Legs - one bent, one extended (mid-leap)
    # Left leg
    draw.line([(fig_x - 10, fig_y + 35), (fig_x - 25, fig_y + 80)],
             fill=palette['secondary'], width=10)
    draw.ellipse([fig_x - 32, fig_y + 75, fig_x - 18, fig_y + 87],
                fill=palette['accent'])  # Foot

    # Right leg extended
    draw.line([(fig_x + 10, fig_y + 30), (fig_x + 45, fig_y + 50)],
             fill=palette['secondary'], width=10)
    draw.ellipse([fig_x + 38, fig_y + 45, fig_x + 52, fig_y + 57],
                fill=palette['accent'])  # Foot

    # Motion lines
    for offset in [10, 20, 30]:
        draw.line([(fig_x - 75 - offset, fig_y - 30), (fig_x - 80 - offset, fig_y - 30)],
                 fill=palette['highlight'], width=2)
        draw.line([(fig_x + 80 + offset, fig_y - 25), (fig_x + 85 + offset, fig_y - 25)],
                 fill=palette['highlight'], width=2)


def draw_major_20(img, draw):
    """
    20: Every Day Is a Miracle - Joy in the present, embodied wonder
    Content: Ordinary objects made luminous, light pouring from the everyday
    """
    palette = get_palette(20)

    # Bright, warm background
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(255 - 30 * t)
        g = int(240 - 30 * t)
        b = int(180 - 20 * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Ordinary objects made sacred by light
    # Coffee cup
    cup_x, cup_y = 70, HEIGHT - 200
    draw.rectangle([cup_x - 15, cup_y, cup_x + 15, cup_y + 30],
                   fill=palette['secondary'], outline=palette['shadow'], width=2)
    # Steam rising (light)
    for i in range(5):
        steam_y = cup_y - 10 - i * 15
        draw.line([(cup_x - 3, steam_y), (cup_x - 5, steam_y - 10)],
                 fill=(255, 255, 255, 150), width=2)
        draw.line([(cup_x + 3, steam_y), (cup_x + 5, steam_y - 10)],
                 fill=(255, 255, 255, 150), width=2)

    # Light radiating from cup
    for angle in range(0, 360, 45):
        rad = angle * math.pi / 180
        end_x = cup_x + int(40 * math.cos(rad))
        end_y = cup_y + 15 + int(40 * math.sin(rad))
        draw.line([(cup_x, cup_y + 15), (end_x, end_y)],
                 fill=(255, 255, 200), width=2)

    # Flower in vase
    flower_x, flower_y = 210, HEIGHT - 190
    # Vase
    vase_points = [(flower_x - 12, flower_y + 40), (flower_x + 12, flower_y + 40),
                   (flower_x + 8, flower_y + 70), (flower_x - 8, flower_y + 70)]
    draw.polygon(vase_points, fill=palette['accent'], outline=palette['shadow'], width=2)

    # Flower
    draw.ellipse([flower_x - 10, flower_y, flower_x + 10, flower_y + 20],
                fill=(255, 100, 100))
    # Stem
    draw.line([(flower_x, flower_y + 20), (flower_x, flower_y + 40)],
             fill=(80, 180, 80), width=3)

    # Light radiating from flower
    for angle in range(0, 360, 40):
        rad = angle * math.pi / 180
        end_x = flower_x + int(45 * math.cos(rad))
        end_y = flower_y + 10 + int(45 * math.sin(rad))
        draw.line([(flower_x, flower_y + 10), (end_x, end_y)],
                 fill=(255, 255, 200), width=2)

    # Figure pointing - awestruck
    fig_x, fig_y = WIDTH // 2, HEIGHT - 100

    # Head
    draw.ellipse([fig_x - 14, fig_y - 60, fig_x + 14, fig_y - 32],
                fill=palette['secondary'])

    # Eyes wide with wonder
    draw.ellipse([fig_x - 8, fig_y - 50, fig_x - 2, fig_y - 44], fill=(255, 255, 255))
    draw.ellipse([fig_x + 2, fig_y - 50, fig_x + 8, fig_y - 44], fill=(255, 255, 255))

    # Body
    body = [(fig_x, fig_y - 32), (fig_x - 20, fig_y - 10),
            (fig_x - 18, fig_y + 35), (fig_x + 18, fig_y + 35),
            (fig_x + 20, fig_y - 10)]
    draw.polygon(body, fill=palette['primary'])

    # Arm pointing at the ordinary miracle
    draw.line([(fig_x - 20, fig_y - 5), (cup_x + 20, cup_y + 10)],
             fill=palette['primary'], width=8)


def draw_major_21(img, draw):
    """
    21: Everybody Laughs - Completion, collective joy
    Content: A crowd all moving together, faces lit, overlapping bodies, everyone laughing
    """
    palette = get_palette(21)

    # Maximum warm, joyful background
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 220,
                       palette['highlight'], palette['secondary'])

    # CROWD - everyone dancing, laughing, together
    # Multiple figures overlapping - American Utopia finale energy

    # Back row figures (smaller, in background)
    for i, x in enumerate([50, 90, 130, 170, 210, 250]):
        y = 160 + (i % 3) * 10
        scale = 0.5

        # Head
        head_size = int(12 * scale)
        draw.ellipse([x - head_size, y, x + head_size, y + head_size * 2],
                    fill=palette['accent'])

        # Body
        body_height = int(30 * scale)
        draw.rectangle([x - int(10 * scale), y + head_size * 2,
                       x + int(10 * scale), y + head_size * 2 + body_height],
                      fill=palette['primary'] if i % 2 == 0 else palette['secondary'])

        # Arms up
        draw.line([(x, y + head_size * 2 + 5),
                  (x - int(15 * scale), y + head_size * 2 - 5)],
                 fill=palette['primary'] if i % 2 == 0 else palette['secondary'],
                 width=int(4 * scale))
        draw.line([(x, y + head_size * 2 + 5),
                  (x + int(15 * scale), y + head_size * 2 - 5)],
                 fill=palette['primary'] if i % 2 == 0 else palette['secondary'],
                 width=int(4 * scale))

    # Middle row (medium size)
    for i, (x, y) in enumerate([(60, 250), (110, 240), (160, 255),
                                 (210, 245), (260, 250)]):
        scale = 0.75

        # Head
        head_size = int(14 * scale)
        draw.ellipse([x - head_size, y, x + head_size, y + head_size * 2],
                    fill=palette['accent'])

        # Mouth open laughing
        draw.arc([x - int(8 * scale), y + int(14 * scale),
                 x + int(8 * scale), y + int(22 * scale)],
                0, 180, fill=(0, 0, 0), width=2)

        # Body
        body_height = int(40 * scale)
        draw.rectangle([x - int(12 * scale), y + head_size * 2,
                       x + int(12 * scale), y + head_size * 2 + body_height],
                      fill=palette['secondary'])

        # Arms in various dance positions
        if i % 2 == 0:
            draw.line([(x, y + head_size * 2 + 8),
                      (x - int(20 * scale), y + head_size * 2 - 10)],
                     fill=palette['secondary'], width=int(6 * scale))
            draw.line([(x, y + head_size * 2 + 8),
                      (x + int(20 * scale), y + head_size * 2 - 10)],
                     fill=palette['secondary'], width=int(6 * scale))
        else:
            draw.line([(x, y + head_size * 2 + 5),
                      (x - int(18 * scale), y + head_size * 2 + 15)],
                     fill=palette['secondary'], width=int(6 * scale))

    # Front row (largest, closest)
    for i, (x, y) in enumerate([(70, 320), (140, 310), (210, 325)]):
        scale = 1.0

        # Head
        head_size = 15
        draw.ellipse([x - head_size, y, x + head_size, y + head_size * 2],
                    fill=palette['accent'])

        # Face - laughing
        draw.arc([x - 10, y + 18, x + 10, y + 28],
                0, 180, fill=(0, 0, 0), width=3)

        # Body
        body_height = 45
        draw.rectangle([x - 15, y + head_size * 2,
                       x + 15, y + head_size * 2 + body_height],
                      fill=palette['primary'])

        # Arms up dancing
        draw.line([(x, y + head_size * 2 + 10),
                  (x - 25, y + head_size * 2 - 12)],
                 fill=palette['primary'], width=8)
        draw.line([(x, y + head_size * 2 + 10),
                  (x + 25, y + head_size * 2 - 12)],
                 fill=palette['primary'], width=8)

    # Joy rays emanating from the crowd
    for angle in range(0, 360, 20):
        rad = angle * math.pi / 180
        start_x = WIDTH // 2 + int(60 * math.cos(rad))
        start_y = HEIGHT // 2 + int(60 * math.sin(rad))
        end_x = WIDTH // 2 + int(110 * math.cos(rad))
        end_y = HEIGHT // 2 + int(110 * math.sin(rad))
        draw.line([(start_x, start_y), (end_x, end_y)],
                 fill=palette['highlight'], width=2)


# Main generation function
def generate_card(card_number):
    """Generate a specific Major Arcana card by number (0-21)"""
    palette = get_palette(card_number)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Draw the specific card
    card_functions = [
        draw_major_0, draw_major_1, draw_major_2, draw_major_3,
        draw_major_4, draw_major_5, draw_major_6, draw_major_7,
        draw_major_8, draw_major_9, draw_major_10, draw_major_11,
        draw_major_12, draw_major_13, draw_major_14, draw_major_15,
        draw_major_16, draw_major_17, draw_major_18, draw_major_19,
        draw_major_20, draw_major_21
    ]

    if 0 <= card_number <= 21:
        card_functions[card_number](img, draw)

    return img


def main():
    """Generate all 22 Major Arcana cards with custom pixel art"""
    print("Generating custom Major Arcana cards...\n")

    output_dir = '/home/user/claude_skills/tarot/decks/byrne/cards'
    os.makedirs(output_dir, exist_ok=True)

    card_names = [
        "Uh-Oh Love Comes to Town", "Psycho Killer", "Don't Worry About the Government",
        "The Big Country", "Life During Wartime", "Heaven", "Houses in Motion",
        "Once in a Lifetime", "Road to Nowhere", "Burning Down the House",
        "This Must Be the Place", "(Nothing But) Flowers", "Something Ain't Right",
        "The Civil Wars", "A Self-Made Man", "Broken Things", "Tiny Apocalypse",
        "One Fine Day", "Lazarus", "I Dance Like This", "Every Day Is a Miracle",
        "Everybody Laughs"
    ]

    for card_number in range(22):
        print(f"  [{card_number + 1}/22] {card_number}: {card_names[card_number]}...")
        img = generate_card(card_number)
        output_path = os.path.join(output_dir, f'major-{card_number:02d}.png')
        img.save(output_path)

    print(f"\n✓ All 22 Major Arcana cards generated!")
    print(f"  Location: {output_dir}/major-*.png")


if __name__ == '__main__':
    main()
