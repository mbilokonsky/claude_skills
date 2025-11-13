#!/usr/bin/env python3
"""
Generate all Major Arcana cards for the Byrne Journey Tarot
Uses the visual toolkit and interprets the visual instructions from the JSON
"""

import json
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

def load_deck_data():
    """Load the deck JSON"""
    with open('/home/user/claude_skills/tarot/decks/byrne/byrne-journey-tarot.json', 'r') as f:
        return json.load(f)

def generate_card_0(card_data):
    """0: Uh-Oh, Love Comes to Town - Innocence, arrival, threshold"""
    palette = bvt.MajorArcanaColors.interpolate_palette(0)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Doorway threshold with bright exterior
    # Sky gradient
    for y in range(0, HEIGHT // 2):
        t = y / (HEIGHT // 2)
        r = int(220 + (palette['accent'][0] - 220) * t)
        g = int(228 + (palette['accent'][1] - 228) * t)
        b = int(195 + (palette['accent'][2] - 195) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Sidewalk
    draw.rectangle([0, HEIGHT // 2, WIDTH, HEIGHT], fill=(142, 148, 158))

    # City buildings in distance
    draw.rectangle([WIDTH//8, HEIGHT//4, WIDTH//3, HEIGHT//2], fill=palette['secondary'])
    for wy in range(HEIGHT//4 + 15, HEIGHT//2, 25):
        for wx in range(WIDTH//8 + 10, WIDTH//3 - 10, 20):
            draw.rectangle([wx, wy, wx+8, wy+12], fill=palette['shadow'])

    # Doorframe
    frame_width = 45
    draw.rectangle([frame_width-12, 40, frame_width, HEIGHT], fill=palette['shadow'])
    draw.rectangle([WIDTH - frame_width, 40, WIDTH - frame_width + 12, HEIGHT], fill=palette['shadow'])
    draw.rectangle([frame_width, 40, WIDTH - frame_width, 52], fill=palette['shadow'])

    # Interior floor
    draw.rectangle([0, HEIGHT - 80, frame_width, HEIGHT], fill=palette['primary'])

    # Figure at threshold with suitcase
    bvt.example_figure_simple(img, frame_width + 35, HEIGHT - 85, palette, posture='awkward', scale=1.1)

    # Suitcase
    suitcase_x = frame_width + 55
    suitcase_y = HEIGHT - 100
    draw.rectangle([suitcase_x, suitcase_y, suitcase_x + 24, suitcase_y + 18], fill=(95, 68, 52))
    draw.rectangle([suitcase_x + 8, suitcase_y - 6, suitcase_x + 16, suitcase_y], fill=palette['shadow'])

    return img

def generate_card_1(card_data):
    """1: Psycho Killer - Self-observation, doubling"""
    palette = bvt.MajorArcanaColors.interpolate_palette(1)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Mirror frame
    mirror_x = WIDTH // 2
    mirror_w = 120
    mirror_h = 180
    draw.rectangle([mirror_x - mirror_w//2, 100, mirror_x + mirror_w//2, 100 + mirror_h],
                   outline=palette['shadow'], width=6)
    draw.rectangle([mirror_x - mirror_w//2 + 10, 110, mirror_x + mirror_w//2 - 10, 100 + mirror_h - 10],
                   fill=palette['accent'])

    # Figure looking at reflection (two versions, slightly off)
    fig_x = WIDTH // 2 - 60
    bvt.example_figure_simple(img, fig_x, HEIGHT - 60, palette, posture='observing', scale=1.2)

    # "Reflection" inside mirror (slightly different)
    reflection_x = mirror_x + 10
    reflection_y = 240
    # Head
    draw.ellipse([reflection_x - 14, reflection_y - 20, reflection_x + 14, reflection_y + 4],
                 fill=palette['secondary'])
    # Body (slightly different posture)
    body = [
        (reflection_x, reflection_y + 2),
        (reflection_x - 16, reflection_y + 22),
        (reflection_x - 14, reflection_y + 60),
        (reflection_x - 7, reflection_y + 85),
        (reflection_x + 7, reflection_y + 85),
        (reflection_x + 12, reflection_y + 58),
        (reflection_x + 14, reflection_y + 20),
    ]
    draw.polygon(body, fill=palette['shadow'])

    # Eyes watching eyes
    draw.ellipse([fig_x + 4, HEIGHT - 147, fig_x + 8, HEIGHT - 143], fill=palette['shadow'])
    draw.line([(fig_x + 6, HEIGHT - 145), (reflection_x - 4, reflection_y - 8)],
              fill=palette['shadow'], width=2)

    return img

def generate_card_2(card_data):
    """2: Don't Worry About the Government - Systems, blueprints"""
    palette = bvt.MajorArcanaColors.interpolate_palette(2)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # House with blueprint overlay
    house_x, house_y = WIDTH // 2, HEIGHT // 2 + 40
    house_w, house_h = 140, 120

    # Solid house
    draw.rectangle([house_x - house_w//2, house_y, house_x + house_w//2, house_y + house_h],
                   fill=palette['secondary'])
    # Roof
    draw.polygon([
        (house_x - house_w//2 - 10, house_y),
        (house_x, house_y - 60),
        (house_x + house_w//2 + 10, house_y)
    ], fill=palette['accent'])

    # Windows
    draw.rectangle([house_x - 40, house_y + 30, house_x - 20, house_y + 55], fill=palette['highlight'])
    draw.rectangle([house_x + 20, house_y + 30, house_x + 40, house_y + 55], fill=palette['highlight'])
    # Door
    draw.rectangle([house_x - 15, house_y + 65, house_x + 15, house_y + house_h], fill=palette['shadow'])

    # Blueprint grid overlay
    bvt.draw_grid_pattern(draw, (20, 20, WIDTH - 20, HEIGHT - 20), 30, palette['accent'])

    # Dimension lines
    draw.line([(house_x - house_w//2 - 20, house_y - 10),
               (house_x + house_w//2 + 20, house_y - 10)],
              fill=palette['highlight'], width=2)
    draw.line([(house_x - house_w//2 - 20, house_y - 15),
               (house_x - house_w//2 - 20, house_y - 5)],
              fill=palette['highlight'], width=2)
    draw.line([(house_x + house_w//2 + 20, house_y - 15),
               (house_x + house_w//2 + 20, house_y - 5)],
              fill=palette['highlight'], width=2)

    return img

def generate_card_3(card_data):
    """3: The Big Country - Aerial view, detachment"""
    palette = bvt.MajorArcanaColors.interpolate_palette(3)
    img = bvt.create_canvas(palette['accent'])
    draw = ImageDraw.Draw(img)

    # Use the aerial setting
    aerial_img = bvt.generate_setting_example('aerial', palette)
    img.paste(aerial_img, (0, 0))

    # Add airplane window frame
    draw.ellipse([10, HEIGHT//3, 80, HEIGHT//3 + 100], outline=palette['shadow'], width=8)
    draw.arc([10, HEIGHT//3, 80, HEIGHT//3 + 100], 180, 360, fill=palette['primary'], width=12)

    return img

def generate_card_4(card_data):
    """4: Life During Wartime - Urgency, crowds, tension"""
    palette = bvt.MajorArcanaColors.interpolate_palette(4)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Dense urban environment
    # Buildings on sides
    draw.rectangle([0, 60, 45, HEIGHT], fill=palette['secondary'])
    draw.rectangle([WIDTH - 45, 80, WIDTH, HEIGHT], fill=palette['secondary'])

    # Windows
    for wy in range(100, HEIGHT, 35):
        draw.rectangle([12, wy, 20, wy+12], fill=palette['shadow'])
        draw.rectangle([25, wy, 33, wy+12], fill=palette['shadow'])
        draw.rectangle([WIDTH - 33, wy, WIDTH - 25, wy+12], fill=palette['shadow'])
        draw.rectangle([WIDTH - 20, wy, WIDTH - 12, wy+12], fill=palette['shadow'])

    # Crowd of figures moving with purpose
    crowd_y = HEIGHT - 70
    for i, x in enumerate([70, 110, 150, 190, 230]):
        scale = 0.7 + (i % 3) * 0.1
        posture = 'moving' if i % 2 == 0 else 'observing'
        bvt.example_figure_simple(img, x, crowd_y - (i % 3) * 10, palette, posture=posture, scale=scale)

    # Motion lines suggesting movement
    for i in range(5):
        y = 50 + i * 60
        draw.line([(50, y), (WIDTH - 50, y)], fill=palette['accent'], width=1)

    return img

def generate_card_5(card_data):
    """5: Heaven - Perfection anxiety, stasis, frozen moment"""
    palette = bvt.MajorArcanaColors.interpolate_palette(5)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Perfect room
    draw.rectangle([40, 60, WIDTH - 40, HEIGHT - 60], outline=palette['shadow'], width=3)

    # Band on repeat - four identical frozen figures
    band_y = HEIGHT - 140
    for i, x in enumerate([80, 120, 160, 200]):
        # Identical frozen neutral poses
        bvt.example_figure_simple(img, x, band_y, palette, posture='neutral', scale=0.8)

    # Musical notes frozen in air
    for i in range(6):
        x = 60 + i * 35
        y = 120 + (i % 2) * 30
        draw.ellipse([x, y, x+10, y+8], fill=palette['accent'])
        draw.line([(x+9, y+4), (x+9, y-12)], fill=palette['accent'], width=2)

    # Everything too perfect - grid lines showing order
    for y in range(80, HEIGHT - 60, 40):
        draw.line([(50, y), (WIDTH - 50, y)], fill=palette['accent'], width=1)

    return img

def generate_card_6(card_data):
    """6: Houses in Motion - Beginning to move, structures alive"""
    palette = bvt.MajorArcanaColors.interpolate_palette(6)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Buildings that seem to breathe/tilt
    # Left building - tilted
    building1 = [
        (40, 120),
        (30, 280),
        (90, 290),
        (100, 110)
    ]
    draw.polygon(building1, fill=palette['secondary'])

    # Center building - wavy
    building2_points = []
    for y in range(80, HEIGHT - 40, 15):
        x_left = 120 + 10 * math.sin(y / 30)
        x_right = 180 + 10 * math.sin(y / 30)
        building2_points.append((x_left, y))
    for y in range(HEIGHT - 40, 80, -15):
        x_right = 180 + 10 * math.sin(y / 30)
        building2_points.append((x_right, y))
    draw.polygon(building2_points, fill=palette['accent'])

    # Right building - tilted other way
    building3 = [
        (200, 100),
        (190, 270),
        (250, 280),
        (260, 110)
    ]
    draw.polygon(building3, fill=palette['secondary'])

    # Motion lines
    for i in range(8):
        y = 60 + i * 45
        offset = 15 * math.sin(y / 40)
        draw.line([(20 + offset, y), (WIDTH - 20 + offset, y)], fill=palette['highlight'], width=1)

    return img

def generate_card_7(card_data):
    """7: Once in a Lifetime - Recognition, reflection, questioning"""
    palette = bvt.MajorArcanaColors.interpolate_palette(7)
    img = bvt.create_canvas(palette['accent'])
    draw = ImageDraw.Draw(img)

    # Water surface
    water_line = HEIGHT // 2 + 20
    # Sky reflection in water
    for y in range(0, water_line):
        t = y / water_line
        color = palette['primary']
        draw.line([(0, y), (WIDTH, y)], fill=color)

    # Water
    for y in range(water_line, HEIGHT):
        t = (y - water_line) / (HEIGHT - water_line)
        r = int(palette['secondary'][0] + (palette['shadow'][0] - palette['secondary'][0]) * t)
        g = int(palette['secondary'][1] + (palette['shadow'][1] - palette['secondary'][1]) * t)
        b = int(palette['secondary'][2] + (palette['shadow'][2] - palette['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Figure looking down at reflection
    fig_y = water_line - 10
    bvt.example_figure_simple(img, WIDTH//2, fig_y, palette, posture='observing', scale=1.3)

    # Reflection in water (upside down, distorted)
    reflection_y = water_line + 30
    # Distorted reflection head
    draw.ellipse([WIDTH//2 - 15, reflection_y, WIDTH//2 + 15, reflection_y + 25], fill=palette['shadow'])
    # Wavy reflection body
    refl_body = [
        (WIDTH//2, reflection_y + 23),
        (WIDTH//2 - 16, reflection_y + 45),
        (WIDTH//2 - 14, reflection_y + 75),
        (WIDTH//2 - 8, reflection_y + 100),
        (WIDTH//2 + 8, reflection_y + 100),
        (WIDTH//2 + 14, reflection_y + 75),
        (WIDTH//2 + 16, reflection_y + 45),
    ]
    draw.polygon(refl_body, fill=palette['shadow'])

    # Ripples
    for r in range(30, 120, 25):
        draw.ellipse([WIDTH//2 - r, water_line - r//4, WIDTH//2 + r, water_line + r//4],
                     outline=palette['highlight'], width=1)

    # Questioning gesture - arm raised
    draw.line([(WIDTH//2 + 8, fig_y - 50), (WIDTH//2 + 25, fig_y - 80)], fill=palette['secondary'], width=6)

    return img

def generate_card_8(card_data):
    """8: Road to Nowhere - Acceptance, journey without destination"""
    palette = bvt.MajorArcanaColors.interpolate_palette(8)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Sky gradient
    for y in range(0, HEIGHT // 2):
        t = y / (HEIGHT // 2)
        r = int(palette['highlight'][0] + (palette['accent'][0] - palette['highlight'][0]) * t)
        g = int(palette['highlight'][1] + (palette['accent'][1] - palette['highlight'][1]) * t)
        b = int(palette['highlight'][2] + (palette['accent'][2] - palette['highlight'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Ground
    draw.rectangle([0, HEIGHT // 2, WIDTH, HEIGHT], fill=palette['ground'])

    # Road disappearing into light (perspective)
    road_points = [
        (WIDTH//2 - 80, HEIGHT),
        (WIDTH//2 + 80, HEIGHT),
        (WIDTH//2 + 30, HEIGHT // 2),
        (WIDTH//2 - 30, HEIGHT // 2)
    ]
    draw.polygon(road_points, fill=palette['secondary'])

    # Center line disappearing
    for i in range(8):
        y_start = HEIGHT - i * 45
        y_end = y_start - 20
        width = 8 - i
        if width > 0:
            draw.line([(WIDTH//2 - width//2, y_start), (WIDTH//2 - width//2, y_end)],
                     fill=palette['highlight'], width=width)

    # Travelers dancing as they walk
    for i, x_offset in enumerate([-40, 0, 35]):
        y = HEIGHT - 90 + (i * 15)
        scale = 0.9 - (i * 0.15)
        bvt.example_figure_simple(img, WIDTH//2 + x_offset, y, palette, posture='moving', scale=scale)

    # Light at vanishing point
    vp = (WIDTH//2, HEIGHT // 2)
    for r in range(60, 10, -10):
        alpha = (60 - r) / 50
        glow_color = tuple(int(palette['highlight'][i] * alpha + palette['primary'][i] * (1 - alpha)) for i in range(3))
        draw.ellipse([vp[0] - r, vp[1] - r//2, vp[0] + r, vp[1] + r//2], fill=glow_color)

    return img

def generate_card_9(card_data):
    """9: Burning Down the House - Destruction, fire, transformation"""
    palette = bvt.MajorArcanaColors.interpolate_palette(9)
    img = bvt.create_canvas(palette['shadow'])
    draw = ImageDraw.Draw(img)

    # House structure
    house_y = HEIGHT - 160
    draw.rectangle([WIDTH//2 - 70, house_y, WIDTH//2 + 70, HEIGHT - 40], fill=palette['secondary'])
    # Roof
    draw.polygon([
        (WIDTH//2 - 80, house_y),
        (WIDTH//2, house_y - 60),
        (WIDTH//2 + 80, house_y)
    ], fill=palette['primary'])

    # Flames (irregular shapes)
    flame_colors = [palette['accent'], palette['highlight'], (255, 200, 100)]
    import random
    random.seed(42)
    for i in range(25):
        fx = WIDTH//2 - 60 + random.randint(0, 120)
        fy = house_y - random.randint(10, 80)
        flame_h = random.randint(20, 50)
        flame_w = random.randint(8, 20)
        color = flame_colors[i % 3]
        # Flame shape
        flame = [
            (fx, fy),
            (fx - flame_w//2, fy + flame_h//2),
            (fx - flame_w//3, fy + flame_h),
            (fx + flame_w//3, fy + flame_h),
            (fx + flame_w//2, fy + flame_h//2),
        ]
        draw.polygon(flame, fill=color)

    # Dancing figures inside (silhouettes through flames)
    for x_offset in [-30, 0, 30]:
        bvt.example_figure_simple(img, WIDTH//2 + x_offset, HEIGHT - 90, palette, posture='moving', scale=0.9)

    # Heat waves
    for y in range(house_y - 100, house_y, 15):
        for x in range(0, WIDTH, 40):
            offset = 10 * math.sin((x + y) / 20)
            draw.line([(x + offset, y), (x + 30 + offset, y)], fill=palette['highlight'], width=2)

    return img

def generate_card_10(card_data):
    """10: This Must Be the Place - Home, love, belonging"""
    palette = bvt.MajorArcanaColors.interpolate_palette(10)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Domestic interior space
    # Room frame
    draw.rectangle([30, 50, WIDTH - 30, HEIGHT - 50], outline=palette['secondary'], width=4)

    # Window with view
    draw.rectangle([WIDTH - 100, 70, WIDTH - 50, 130], fill=palette['highlight'])
    # Window panes
    draw.line([(WIDTH - 75, 70), (WIDTH - 75, 130)], fill=palette['secondary'], width=2)
    draw.line([(WIDTH - 100, 100), (WIDTH - 50, 100)], fill=palette['secondary'], width=2)

    # Simple furniture
    # Table
    draw.rectangle([50, HEIGHT - 140, 120, HEIGHT - 120], fill=palette['accent'])
    draw.line([(60, HEIGHT - 120), (60, HEIGHT - 70)], fill=palette['accent'], width=6)
    draw.line([(110, HEIGHT - 120), (110, HEIGHT - 70)], fill=palette['accent'], width=6)

    # Objects on table (simple, sacred by presence)
    draw.ellipse([70, HEIGHT - 155, 90, HEIGHT - 140], fill=palette['highlight'])  # Bowl
    draw.rectangle([95, HEIGHT - 150, 102, HEIGHT - 140], fill=palette['secondary'])  # Cup

    # Two figures in embrace (center of composition)
    fig1_x = WIDTH//2 - 20
    fig2_x = WIDTH//2 + 20
    fig_y = HEIGHT - 110

    # Left figure
    draw.ellipse([fig1_x - 12, fig_y - 85, fig1_x + 12, fig_y - 61], fill=palette['secondary'])
    # Right figure
    draw.ellipse([fig2_x - 12, fig_y - 85, fig2_x + 12, fig_y - 61], fill=palette['accent'])

    # Embracing bodies (overlapping polygons)
    body1 = [
        (fig1_x, fig_y - 60),
        (fig1_x - 14, fig_y - 40),
        (fig1_x - 12, fig_y - 5),
        (fig1_x - 6, fig_y + 20),
        (fig1_x + 10, fig_y + 20),
        (fig1_x + 14, fig_y - 5),
        (fig1_x + 12, fig_y - 40),
    ]
    draw.polygon(body1, fill=palette['secondary'])

    body2 = [
        (fig2_x, fig_y - 60),
        (fig2_x - 12, fig_y - 40),
        (fig2_x - 14, fig_y - 5),
        (fig2_x - 10, fig_y + 20),
        (fig2_x + 6, fig_y + 20),
        (fig2_x + 12, fig_y - 5),
        (fig2_x + 14, fig_y - 40),
    ]
    draw.polygon(body2, fill=palette['accent'])

    # Warm light glow around figures
    for r in range(60, 30, -10):
        alpha = (60 - r) / 30
        glow = tuple(int(palette['highlight'][i] * alpha + palette['primary'][i] * (1 - alpha)) for i in range(3))
        draw.ellipse([WIDTH//2 - r, fig_y - 90 - r//2, WIDTH//2 + r, fig_y + 20 + r//2], outline=glow, width=2)

    return img

def generate_card_11(card_data):
    """11: Nothing But Flowers - Nature reclaiming, civilization questioned"""
    palette = bvt.MajorArcanaColors.interpolate_palette(11)
    img = bvt.create_canvas(palette['accent'])
    draw = ImageDraw.Draw(img)

    # Building structure (Pizza Hut reference)
    building_y = HEIGHT // 2
    draw.polygon([
        (WIDTH//2 - 80, building_y),
        (WIDTH//2, building_y - 40),
        (WIDTH//2 + 80, building_y)
    ], fill=palette['secondary'])  # Distinctive roof
    draw.rectangle([WIDTH//2 - 70, building_y, WIDTH//2 + 70, HEIGHT - 60], fill=palette['secondary'])

    # Windows
    draw.rectangle([WIDTH//2 - 50, building_y + 30, WIDTH//2 - 25, building_y + 55], fill=palette['shadow'])
    draw.rectangle([WIDTH//2 + 25, building_y + 30, WIDTH//2 + 50, building_y + 55], fill=palette['shadow'])

    # Vines and plants overtaking (organic irregular shapes)
    import random
    random.seed(42)
    plant_green = (100, 140, 90)
    flower_color = palette['highlight']

    # Vines crawling up walls
    for i in range(12):
        start_x = WIDTH//2 - 70 + i * 12
        for y in range(building_y + 40, HEIGHT - 60, 20):
            vine_x = start_x + random.randint(-5, 5)
            draw.ellipse([vine_x - 4, y - 4, vine_x + 4, y + 4], fill=plant_green)
            if i < 10:
                draw.line([(vine_x, y), (vine_x + random.randint(-3, 3), y + 20)],
                         fill=plant_green, width=3)

    # Flowers/vegetation at base
    for i in range(15):
        x = WIDTH//2 - 80 + random.randint(0, 160)
        y = HEIGHT - 60 + random.randint(0, 50)
        # Flower petals
        for angle in range(0, 360, 72):
            rad = math.radians(angle)
            px = x + 8 * math.cos(rad)
            py = y + 8 * math.sin(rad)
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=flower_color)
        # Center
        draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=plant_green)

    # Grass/plants in foreground
    for i in range(20):
        x = random.randint(20, WIDTH - 20)
        y = HEIGHT - random.randint(20, 60)
        h = random.randint(15, 35)
        draw.line([(x, HEIGHT), (x + random.randint(-5, 5), y)], fill=plant_green, width=3)

    return img

def generate_card_12(card_data):
    """12: Something Ain't Right - Unease, subtle wrongness"""
    palette = bvt.MajorArcanaColors.interpolate_palette(12)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Familiar room but off
    # Room frame (slightly tilted)
    draw.polygon([
        (35, 55),
        (WIDTH - 30, 50),
        (WIDTH - 35, HEIGHT - 50),
        (30, HEIGHT - 55)
    ], outline=palette['secondary'], width=3)

    # Window (wrong size/position)
    draw.rectangle([WIDTH - 110, 90, WIDTH - 45, 140], fill=palette['accent'])
    draw.line([(WIDTH - 77, 90), (WIDTH - 77, 140)], fill=palette['shadow'], width=2)
    draw.line([(WIDTH - 110, 115), (WIDTH - 45, 115)], fill=palette['shadow'], width=2)

    # Table (legs uneven)
    draw.rectangle([60, HEIGHT - 140, 130, HEIGHT - 120], fill=palette['accent'])
    draw.line([(70, HEIGHT - 120), (68, HEIGHT - 75)], fill=palette['accent'], width=6)  # Tilted
    draw.line([(120, HEIGHT - 120), (120, HEIGHT - 70)], fill=palette['accent'], width=6)  # Different height

    # Figure in familiar place, unease posture
    bvt.example_figure_simple(img, WIDTH//2 + 30, HEIGHT - 100, palette, posture='awkward', scale=1.1)

    # Shadows where there weren't shadows (multiple shadow directions)
    # Shadow 1 (from figure, wrong direction)
    shadow1 = [
        (WIDTH//2 + 30, HEIGHT - 100),
        (WIDTH//2 + 20, HEIGHT - 10),
        (WIDTH//2 + 40, HEIGHT - 10)
    ]
    draw.polygon(shadow1, fill=palette['shadow'])

    # Shadow 2 (from table, different direction)
    draw.polygon([
        (60, HEIGHT - 120),
        (40, HEIGHT - 90),
        (100, HEIGHT - 90),
        (130, HEIGHT - 120)
    ], fill=palette['shadow'])

    # Objects slightly wrong
    # Cup tilted wrong
    draw.polygon([
        (85, HEIGHT - 155),
        (75, HEIGHT - 145),
        (82, HEIGHT - 140),
        (92, HEIGHT - 150)
    ], fill=palette['secondary'])

    return img

def generate_card_13(card_data):
    """13: The Civil Wars - Internal conflict, shadow self"""
    palette = bvt.MajorArcanaColors.interpolate_palette(13)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Divided composition
    # Left side - lighter
    for y in range(HEIGHT):
        x_div = WIDTH // 2 + int(10 * math.sin(y / 30))
        draw.line([(0, y), (x_div, y)], fill=palette['accent'])

    # Right side - darker
    for y in range(HEIGHT):
        x_div = WIDTH // 2 + int(10 * math.sin(y / 30))
        draw.line([(x_div, y), (WIDTH, y)], fill=palette['shadow'])

    # Figure on left (lighter self)
    fig1_x = WIDTH // 2 - 50
    bvt.example_figure_simple(img, fig1_x, HEIGHT - 80, palette, posture='observing', scale=1.2)

    # Shadow self on right (darker)
    fig2_x = WIDTH // 2 + 50
    # Head
    draw.ellipse([fig2_x - 14, HEIGHT - 158, fig2_x + 14, HEIGHT - 134], fill=palette['shadow'])
    # Body (mirror posture but dark)
    shadow_body = [
        (fig2_x, HEIGHT - 135),
        (fig2_x + 18, HEIGHT - 108),
        (fig2_x + 16, HEIGHT - 68),
        (fig2_x + 9, HEIGHT - 20),
        (fig2_x - 9, HEIGHT - 20),
        (fig2_x - 14, HEIGHT - 70),
        (fig2_x - 16, HEIGHT - 110),
    ]
    draw.polygon(shadow_body, fill=(30, 30, 35))

    # Battlefield elements at intimate scale
    # Crossed lines between figures
    draw.line([(fig1_x + 15, HEIGHT - 120), (fig2_x - 15, HEIGHT - 120)],
             fill=palette['highlight'], width=3)
    draw.line([(fig1_x + 10, HEIGHT - 100), (fig2_x - 10, HEIGHT - 140)],
             fill=palette['secondary'], width=2)
    draw.line([(fig1_x + 10, HEIGHT - 140), (fig2_x - 10, HEIGHT - 100)],
             fill=palette['secondary'], width=2)

    # Wavy division line emphasized
    for y in range(0, HEIGHT, 20):
        x_div = WIDTH // 2 + int(10 * math.sin(y / 30))
        draw.ellipse([x_div - 3, y - 3, x_div + 3, y + 3], fill=palette['highlight'])

    return img

def generate_card_14(card_data):
    """14: A Self-Made Man - Confronting your construction"""
    palette = bvt.MajorArcanaColors.interpolate_palette(14)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Blueprint of self
    bvt.draw_grid_pattern(draw, (20, 20, WIDTH - 20, HEIGHT - 20), 25, palette['accent'])

    # Figure looking at blueprint/statue of themselves
    fig_x = WIDTH // 2 - 60
    bvt.example_figure_simple(img, fig_x, HEIGHT - 70, palette, posture='observing', scale=1.0)

    # Blueprint/statue version (right side)
    statue_x = WIDTH // 2 + 60
    statue_y_base = HEIGHT - 70

    # Blueprint lines around statue
    draw.rectangle([statue_x - 40, statue_y_base - 130, statue_x + 40, statue_y_base + 20],
                   outline=palette['secondary'], width=2)

    # Dimension lines
    draw.line([(statue_x - 50, statue_y_base - 140), (statue_x + 50, statue_y_base - 140)],
             fill=palette['highlight'], width=2)
    draw.line([(statue_x - 50, statue_y_base - 145), (statue_x - 50, statue_y_base - 135)],
             fill=palette['highlight'], width=2)
    draw.line([(statue_x + 50, statue_y_base - 145), (statue_x + 50, statue_y_base - 135)],
             fill=palette['highlight'], width=2)

    # The statue/blueprint figure (more geometric)
    draw.ellipse([statue_x - 12, statue_y_base - 106, statue_x + 12, statue_y_base - 82],
                 fill=palette['secondary'])
    statue_body = [
        (statue_x, statue_y_base - 81),
        (statue_x - 16, statue_y_base - 60),
        (statue_x - 14, statue_y_base - 20),
        (statue_x - 7, statue_y_base + 15),
        (statue_x + 7, statue_y_base + 15),
        (statue_x + 14, statue_y_base - 20),
        (statue_x + 16, statue_y_base - 60),
    ]
    draw.polygon(statue_body, fill=palette['accent'])

    # Annotations/labels
    draw.line([(statue_x - 20, statue_y_base - 95), (statue_x - 60, statue_y_base - 110)],
             fill=palette['highlight'], width=1)
    draw.line([(statue_x + 20, statue_y_base - 40), (statue_x + 60, statue_y_base - 50)],
             fill=palette['highlight'], width=1)

    # Recognition line from figure to statue
    draw.line([(fig_x + 10, HEIGHT - 145), (statue_x - 15, statue_y_base - 95)],
             fill=palette['secondary'], width=2, )

    return img

def generate_card_15(card_data):
    """15: Broken Things - Acceptance, beauty in damage"""
    palette = bvt.MajorArcanaColors.interpolate_palette(15)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Shattered objects arranged beautifully
    # Broken vase pieces
    pieces_center = (WIDTH // 2, HEIGHT // 2)

    # Large piece
    piece1 = [
        (pieces_center[0] - 30, pieces_center[1] - 20),
        (pieces_center[0] - 35, pieces_center[1] + 30),
        (pieces_center[0] - 10, pieces_center[1] + 35),
        (pieces_center[0] - 5, pieces_center[1] - 15),
    ]
    draw.polygon(piece1, fill=palette['accent'])
    draw.polygon(piece1, outline=palette['highlight'], width=2)

    # Another piece
    piece2 = [
        (pieces_center[0] + 5, pieces_center[1] - 25),
        (pieces_center[0] + 10, pieces_center[1] + 20),
        (pieces_center[0] + 35, pieces_center[1] + 15),
        (pieces_center[0] + 30, pieces_center[1] - 30),
    ]
    draw.polygon(piece2, fill=palette['secondary'])
    draw.polygon(piece2, outline=palette['highlight'], width=2)

    # Smaller pieces scattered
    for i, (x, y) in enumerate([(WIDTH//2 - 50, HEIGHT//2 + 50),
                                  (WIDTH//2 + 45, HEIGHT//2 - 40),
                                  (WIDTH//2 + 10, HEIGHT//2 + 55)]):
        size = 15 - i * 3
        draw.polygon([
            (x, y),
            (x - size, y + size),
            (x + size//2, y + size + 5)
        ], fill=palette['accent'])
        draw.polygon([
            (x, y),
            (x - size, y + size),
            (x + size//2, y + size + 5)
        ], outline=palette['highlight'], width=1)

    # Figure holding pieces
    fig_x = WIDTH // 2
    fig_y = HEIGHT - 90
    bvt.example_figure_simple(img, fig_x, fig_y, palette, posture='neutral', scale=1.1)

    # Hands holding (extended from body)
    draw.line([(fig_x - 20, fig_y - 50), (pieces_center[0] - 25, pieces_center[1])],
             fill=palette['secondary'], width=6)
    draw.line([(fig_x + 20, fig_y - 50), (pieces_center[0] + 20, pieces_center[1])],
             fill=palette['secondary'], width=6)

    # Light through cracks
    for x in range(pieces_center[0] - 40, pieces_center[0] + 50, 15):
        for y in range(pieces_center[1] - 30, pieces_center[1] + 60, 15):
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=palette['highlight'])

    # Radial glow from center
    for r in range(80, 30, -15):
        alpha = (80 - r) / 50
        glow = tuple(int(palette['highlight'][i] * alpha + palette['primary'][i] * (1 - alpha)) for i in range(3))
        draw.ellipse([pieces_center[0] - r, pieces_center[1] - r,
                     pieces_center[0] + r, pieces_center[1] + r],
                    outline=glow, width=1)

    return img

def generate_card_16(card_data):
    """16: Tiny Apocalypse - Personal catastrophe, domestic disaster"""
    palette = bvt.MajorArcanaColors.interpolate_palette(16)
    img = bvt.create_canvas(palette['shadow'])
    draw = ImageDraw.Draw(img)

    # Room mid-collapse
    # Tilted walls
    draw.polygon([
        (25, 40),
        (WIDTH - 20, 50),
        (WIDTH - 30, HEIGHT - 40),
        (20, HEIGHT - 50)
    ], outline=palette['accent'], width=4)

    # Furniture floating/falling
    # Table floating at angle
    table_angle = math.radians(25)
    table_cx, table_cy = WIDTH // 2 - 30, HEIGHT // 2 - 40
    table_w, table_h = 70, 15
    cos_a, sin_a = math.cos(table_angle), math.sin(table_angle)
    table_corners = [
        (table_cx - table_w//2 * cos_a + table_h//2 * sin_a,
         table_cy - table_w//2 * sin_a - table_h//2 * cos_a),
        (table_cx + table_w//2 * cos_a + table_h//2 * sin_a,
         table_cy + table_w//2 * sin_a - table_h//2 * cos_a),
        (table_cx + table_w//2 * cos_a - table_h//2 * sin_a,
         table_cy + table_w//2 * sin_a + table_h//2 * cos_a),
        (table_cx - table_w//2 * cos_a - table_h//2 * sin_a,
         table_cy - table_w//2 * sin_a + table_h//2 * cos_a),
    ]
    draw.polygon(table_corners, fill=palette['secondary'])

    # Chair tumbling
    draw.rectangle([WIDTH - 90, HEIGHT // 2 + 30, WIDTH - 60, HEIGHT // 2 + 70],
                   fill=palette['accent'])
    draw.rectangle([WIDTH - 88, HEIGHT // 2 + 25, WIDTH - 85, HEIGHT // 2 + 35],
                   fill=palette['accent'])

    # Objects in mid-air
    for (x, y) in [(80, 120), (WIDTH - 70, 180), (WIDTH // 2, 90)]:
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=palette['highlight'])
        # Motion blur
        draw.line([(x, y - 15), (x, y + 15)], fill=palette['accent'], width=2)

    # Figure falling/floating
    fig_x = WIDTH // 2 + 40
    fig_y = HEIGHT // 2 + 80
    # Tilted figure
    draw.ellipse([fig_x - 10, fig_y - 80, fig_x + 14, fig_y - 56], fill=palette['secondary'])
    tilted_body = [
        (fig_x + 2, fig_y - 58),
        (fig_x - 12, fig_y - 35),
        (fig_x - 8, fig_y + 5),
        (fig_x + 0, fig_y + 35),
        (fig_x + 15, fig_y + 30),
        (fig_x + 20, fig_y),
        (fig_x + 18, fig_y - 38),
    ]
    draw.polygon(tilted_body, fill=palette['primary'])

    # Cracks radiating
    center = (WIDTH // 2, HEIGHT // 2)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        end_x = center[0] + 100 * math.cos(rad)
        end_y = center[1] + 100 * math.sin(rad)
        draw.line([(center[0], center[1]), (end_x, end_y)], fill=palette['highlight'], width=2)

    # Floor falling away
    hole_center = (WIDTH // 2, HEIGHT - 60)
    for r in range(20, 80, 15):
        draw.ellipse([hole_center[0] - r, hole_center[1] - r//2,
                     hole_center[0] + r, hole_center[1] + r//2],
                    outline=palette['shadow'], width=2)

    return img

def generate_card_17(card_data):
    """17: One Fine Day - Hope returns, dawn"""
    palette = bvt.MajorArcanaColors.interpolate_palette(17)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Dawn breaking
    for y in range(HEIGHT):
        t = y / HEIGHT
        # Dark to light gradient
        r = int(palette['shadow'][0] + (palette['highlight'][0] - palette['shadow'][0]) * t)
        g = int(palette['shadow'][1] + (palette['highlight'][1] - palette['shadow'][1]) * t)
        b = int(palette['shadow'][2] + (palette['highlight'][2] - palette['shadow'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Sun rising
    sun_y = HEIGHT // 3
    for r in range(50, 10, -8):
        alpha = (50 - r) / 40
        sun_color = tuple(int(255 * alpha + palette['highlight'][i] * (1 - alpha)) for i in range(3))
        draw.ellipse([WIDTH//2 - r, sun_y - r, WIDTH//2 + r, sun_y + r], fill=sun_color)

    # Sun rays
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        start_x = WIDTH//2 + 55 * math.cos(rad)
        start_y = sun_y + 55 * math.sin(rad)
        end_x = WIDTH//2 + 120 * math.cos(rad)
        end_y = sun_y + 120 * math.sin(rad)
        draw.line([(start_x, start_y), (end_x, end_y)], fill=palette['highlight'], width=3)

    # Road ahead visible
    road_points = [
        (WIDTH//2 - 60, HEIGHT),
        (WIDTH//2 + 60, HEIGHT),
        (WIDTH//2 + 25, HEIGHT // 2 + 40),
        (WIDTH//2 - 25, HEIGHT // 2 + 40)
    ]
    draw.polygon(road_points, fill=palette['secondary'])

    # Figure looking toward horizon (posture of readiness)
    bvt.example_figure_simple(img, WIDTH//2, HEIGHT - 80, palette, posture='observing', scale=1.3)

    # Horizon line
    draw.line([(0, HEIGHT // 2 + 40), (WIDTH, HEIGHT // 2 + 40)], fill=palette['accent'], width=2)

    return img

def generate_card_18(card_data):
    """18: Lazarus - Resurrection, rising"""
    palette = bvt.MajorArcanaColors.interpolate_palette(18)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Light from above
    light_center = (WIDTH // 2, 60)
    for r in range(100, 20, -15):
        alpha = (100 - r) / 80
        light_color = tuple(int(palette['highlight'][i] * alpha + palette['primary'][i] * (1 - alpha)) for i in range(3))
        draw.ellipse([light_center[0] - r, light_center[1] - r//3,
                     light_center[0] + r, light_center[1] + r//3],
                    fill=light_color)

    # Light beam down to figure
    beam_points = [
        (WIDTH//2 - 40, 80),
        (WIDTH//2 + 40, 80),
        (WIDTH//2 + 60, HEIGHT // 2 + 40),
        (WIDTH//2 - 60, HEIGHT // 2 + 40)
    ]
    for i, point in enumerate(beam_points):
        next_point = beam_points[(i + 1) % len(beam_points)]
        alpha = 0.3
        beam_color = tuple(int(palette['highlight'][j] * alpha + palette['primary'][j] * (1 - alpha)) for j in range(3))
        if i < 2:
            draw.line([point, next_point], fill=beam_color, width=3)
    draw.polygon(beam_points, fill=tuple(int(palette['highlight'][j] * 0.2 + palette['primary'][j] * 0.8) for j in range(3)))

    # Ground/tomb
    draw.rectangle([WIDTH//2 - 70, HEIGHT - 120, WIDTH//2 + 70, HEIGHT - 50],
                   fill=palette['secondary'])

    # Figure standing/rising (dynamic upward posture)
    fig_x = WIDTH // 2
    fig_y = HEIGHT - 50

    # Head
    draw.ellipse([fig_x - 14, fig_y - 130, fig_x + 14, fig_y - 106], fill=palette['accent'])

    # Rising body (arms raised)
    rising_body = [
        (fig_x, fig_y - 105),
        (fig_x - 18, fig_y - 85),
        (fig_x - 35, fig_y - 115),  # Left arm raised
        (fig_x - 25, fig_y - 90),
        (fig_x - 14, fig_y - 50),
        (fig_x - 7, fig_y),
        (fig_x + 7, fig_y),
        (fig_x + 14, fig_y - 50),
        (fig_x + 25, fig_y - 90),
        (fig_x + 35, fig_y - 115),  # Right arm raised
        (fig_x + 18, fig_y - 85),
    ]
    draw.polygon(rising_body, fill=palette['secondary'])

    # Motion lines suggesting upward movement
    for i in range(5):
        y = fig_y - 140 + i * 20
        draw.line([(fig_x - 50, y), (fig_x - 40, y - 10)], fill=palette['highlight'], width=2)
        draw.line([(fig_x + 50, y), (fig_x + 40, y - 10)], fill=palette['highlight'], width=2)

    return img

def generate_card_19(card_data):
    """19: I Dance Like This - Embodied declaration, authentic movement"""
    palette = bvt.MajorArcanaColors.interpolate_palette(19)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Radial energy
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2 + 20, 180, palette['accent'], palette['primary'])

    # Body mid-dance (large, central, dynamic)
    fig_x = WIDTH // 2
    fig_y = HEIGHT // 2 + 100

    # Head (tilted, in motion)
    draw.ellipse([fig_x - 18, fig_y - 115, fig_x + 18, fig_y - 87], fill=palette['secondary'])

    # Body in dynamic dance pose (asymmetric, energetic)
    dance_body = [
        (fig_x + 8, fig_y - 88),     # Neck
        (fig_x - 30, fig_y - 55),    # Left arm extended
        (fig_x - 45, fig_y - 75),    # Left hand up
        (fig_x - 25, fig_y - 60),    # Back to shoulder
        (fig_x - 20, fig_y - 10),    # Left hip
        (fig_x - 10, fig_y + 40),    # Left foot off ground
        (fig_x + 18, fig_y + 35),    # Right foot
        (fig_x + 28, fig_y - 15),    # Right hip
        (fig_x + 40, fig_y - 50),    # Right arm out
        (fig_x + 55, fig_y - 40),    # Right hand
        (fig_x + 35, fig_y - 55),    # Back to shoulder
    ]
    draw.polygon(dance_body, fill=palette['accent'])

    # Suit jacket flying (big suit!)
    jacket = [
        (fig_x + 8, fig_y - 88),
        (fig_x - 60, fig_y - 70),    # Left side flying
        (fig_x - 55, fig_y + 20),
        (fig_x - 30, fig_y + 10),
        (fig_x + 30, fig_y + 10),
        (fig_x + 55, fig_y + 20),
        (fig_x + 70, fig_y - 60),    # Right side flying
    ]
    draw.polygon(jacket, fill=palette['secondary'])

    # Motion blur/energy lines
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        length = 60 + i * 5
        end_x = fig_x + length * math.cos(rad)
        end_y = fig_y - 50 + length * math.sin(rad)
        draw.line([(fig_x, fig_y - 50), (end_x, end_y)], fill=palette['highlight'], width=3)

    # Feet off ground emphasized
    draw.ellipse([fig_x - 15, fig_y + 35, fig_x - 5, fig_y + 45], fill=palette['shadow'])
    draw.ellipse([fig_x + 13, fig_y + 30, fig_x + 23, fig_y + 40], fill=palette['shadow'])

    # Unselfconscious - no eyes on the face, just shape

    return img

def generate_card_20(card_data):
    """20: Every Day Is a Miracle - Joy in the present, ordinary made luminous"""
    palette = bvt.MajorArcanaColors.interpolate_palette(20)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Ordinary objects made luminous
    objects = [
        # Coffee cup
        ((70, HEIGHT - 150), 'cup'),
        # Apple
        ((WIDTH // 2, HEIGHT // 2 - 30), 'apple'),
        # Book
        ((WIDTH - 80, HEIGHT - 160), 'book'),
    ]

    for (x, y), obj_type in objects:
        # Radiant glow around object
        for r in range(50, 15, -8):
            alpha = (50 - r) / 35
            glow = tuple(int(palette['highlight'][i] * alpha + palette['primary'][i] * (1 - alpha)) for i in range(3))
            draw.ellipse([x - r, y - r, x + r, y + r], fill=glow)

        if obj_type == 'cup':
            # Cup shape
            draw.rectangle([x - 12, y - 15, x + 12, y + 15], fill=palette['accent'])
            draw.ellipse([x - 12, y - 17, x + 12, y - 13], fill=palette['secondary'])
            # Handle
            draw.arc([x + 10, y - 8, x + 25, y + 8], 270, 90, fill=palette['accent'], width=4)

        elif obj_type == 'apple':
            # Apple
            draw.ellipse([x - 18, y - 15, x + 18, y + 15], fill=(200, 80, 70))
            # Stem
            draw.line([(x - 2, y - 15), (x - 2, y - 25)], fill=palette['ground'], width=3)
            # Highlight
            draw.ellipse([x - 8, y - 8, x - 2, y - 2], fill=palette['highlight'])

        elif obj_type == 'book':
            # Book
            draw.rectangle([x - 20, y - 10, x + 20, y + 18], fill=palette['secondary'])
            draw.line([(x - 20, y), (x + 20, y)], fill=palette['accent'], width=2)
            draw.line([(x, y - 10), (x, y + 18)], fill=palette['highlight'], width=1)

    # Light pouring from above
    for x in range(0, WIDTH, 25):
        beam_top = 0
        beam_bottom = HEIGHT
        beam_x_shift = 15 * math.sin(x / 40)
        draw.line([(x, beam_top), (x + beam_x_shift, beam_bottom)],
                 fill=palette['highlight'], width=2)

    # Figure pointing with genuine awe
    fig_x = WIDTH // 2 + 40
    fig_y = HEIGHT - 90
    bvt.example_figure_simple(img, fig_x, fig_y, palette, posture='observing', scale=1.2)

    # Pointing arm extended toward apple
    draw.line([(fig_x - 15, fig_y - 60), (WIDTH // 2 - 25, HEIGHT // 2 - 30)],
             fill=palette['secondary'], width=7)

    # Stars/sparkles around everything
    import random
    random.seed(42)
    for i in range(30):
        sx = random.randint(10, WIDTH - 10)
        sy = random.randint(10, HEIGHT - 10)
        size = random.randint(2, 5)
        draw.line([(sx - size, sy), (sx + size, sy)], fill=palette['highlight'], width=2)
        draw.line([(sx, sy - size), (sx, sy + size)], fill=palette['highlight'], width=2)

    return img

def generate_card_21(card_data):
    """21: Everybody Laughs - Completion, collective joy, finale"""
    palette = bvt.MajorArcanaColors.interpolate_palette(21)
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Warm, vibrant background
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 200, palette['highlight'], palette['accent'])

    # Crowd all moving together - overlapping figures
    # Back row (smaller, distant)
    back_row_y = HEIGHT - 200
    for i, x in enumerate([40, 80, 120, 160, 200, 240]):
        scale = 0.55 + (i % 3) * 0.05
        posture = 'moving' if i % 2 == 0 else 'observing'
        bvt.example_figure_simple(img, x, back_row_y, palette, posture=posture, scale=scale)

    # Middle row (medium)
    mid_row_y = HEIGHT - 140
    for i, x in enumerate([60, 110, 160, 210]):
        scale = 0.75 + (i % 2) * 0.1
        posture = 'moving'
        bvt.example_figure_simple(img, x, mid_row_y, palette, posture=posture, scale=scale)

    # Front row (larger, present)
    front_row_y = HEIGHT - 70
    for i, x in enumerate([70, 140, 210]):
        scale = 1.0 + (i % 2) * 0.15
        posture = 'moving'
        bvt.example_figure_simple(img, x, front_row_y, palette, posture=posture, scale=scale)

    # Everyone laughing - indicated by heads tilted back
    # Add simple mouth curves to some front figures
    for x in [70, 140, 210]:
        y = front_row_y - 85
        draw.arc([x - 8, y, x + 8, y + 12], 0, 180, fill=(255, 255, 255), width=3)

    # Energy/joy radiating outward
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        start_r = 50
        end_r = 140
        start_x = WIDTH//2 + start_r * math.cos(rad)
        start_y = HEIGHT//2 + start_r * math.sin(rad)
        end_x = WIDTH//2 + end_r * math.cos(rad)
        end_y = HEIGHT//2 + end_r * math.sin(rad)
        draw.line([(start_x, start_y), (end_x, end_y)], fill=palette['highlight'], width=2)

    # Overlapping bodies creating unity
    # Draw some connection lines between figures
    for (x1, y1), (x2, y2) in [((70, front_row_y - 50), (140, front_row_y - 50)),
                                ((140, front_row_y - 50), (210, front_row_y - 50)),
                                ((60, mid_row_y - 40), (110, mid_row_y - 40))]:
        draw.line([(x1, y1), (x2, y2)], fill=palette['accent'], width=4)

    # Finale energy - confetti/sparkles
    import random
    random.seed(42)
    for i in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT - 100)
        size = random.randint(3, 8)
        color_choice = [palette['highlight'], palette['accent'], (255, 220, 100)]
        draw.ellipse([x, y, x + size, y + size], fill=color_choice[i % 3])

    return img

def main():
    """Generate all 22 Major Arcana cards"""
    print("Loading deck data...")
    deck_data = load_deck_data()

    # Create output directory
    output_dir = '/home/user/claude_skills/tarot/decks/byrne/cards'
    os.makedirs(output_dir, exist_ok=True)

    # Card generation functions
    generators = [
        generate_card_0, generate_card_1, generate_card_2, generate_card_3,
        generate_card_4, generate_card_5, generate_card_6, generate_card_7,
        generate_card_8, generate_card_9, generate_card_10, generate_card_11,
        generate_card_12, generate_card_13, generate_card_14, generate_card_15,
        generate_card_16, generate_card_17, generate_card_18, generate_card_19,
        generate_card_20, generate_card_21
    ]

    print(f"\nGenerating 22 Major Arcana cards...")
    for i, generator in enumerate(generators):
        card_key = f"major-{i}"
        card_data = deck_data['cards'].get(card_key, {})

        print(f"  [{i+1}/22] Generating: {card_data.get('name', card_key)}...")

        img = generator(card_data)
        output_path = os.path.join(output_dir, f'major-{i:02d}.png')
        img.save(output_path)

    print(f"\n✓ All 22 cards generated successfully!")
    print(f"  Location: {output_dir}/")
    print(f"  Files: major-00.png through major-21.png")

if __name__ == '__main__':
    main()
