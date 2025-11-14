#!/usr/bin/env python3
"""
Generate even more cards - completing Puppets, Mountains, and Major Arcana
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

# === PUPPETS SUIT ADDITIONS ===

def draw_two_of_puppets():
    """Two of Puppets: First performance, first craft shared"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # TWO puppets - learning together
    left_x, right_x = CARD_WIDTH // 3, 2 * CARD_WIDTH // 3
    puppet_y = CARD_HEIGHT * 2 // 3

    for px in [left_x, right_x]:
        # Puppet
        draw.ellipse([px-10, puppet_y-30, px+10, puppet_y-15],
                    fill=(200, 180, 150))
        draw.polygon([
            (px, puppet_y-15),
            (px-12, puppet_y+10),
            (px+12, puppet_y+10)
        ], fill=(180, 60, 60))

        # Control bar above
        control_y = CARD_HEIGHT // 3
        draw.rectangle([px-20, control_y-5, px+20, control_y+5],
                      fill=PuppetsColors.SECONDARY)

        # Strings
        draw_puppet_strings(draw, px, control_y+5, px, puppet_y-30,
                           PuppetsColors.STRING)

    # Spotlight between them - shared stage
    for r in range(80, 0, -4):
        draw.ellipse([CARD_WIDTH//2-r, puppet_y-r, CARD_WIDTH//2+r, puppet_y+r],
                    fill=(60+r//2, 40+r//2, 0), outline=(60+r//2, 40+r//2, 0))

    return img


def draw_four_of_puppets():
    """Four of Puppets: Sanctuary in theater, craft as refuge"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # STAGE as sanctuary - golden proscenium
    draw.rectangle([40, 100, CARD_WIDTH-40, CARD_HEIGHT-100],
                  outline=PuppetsColors.SECONDARY, width=8)

    # Warm light within
    for y in range(120, CARD_HEIGHT-120):
        brightness = 40 + int(20 * math.sin((y - 120) / 50))
        for x in range(60, CARD_WIDTH-60):
            draw.point((x, y), fill=(brightness, brightness//2, 0))

    # FOUR figures - safe in the theater
    positions = [(80, 200), (CARD_WIDTH-80, 200),
                (80, CARD_HEIGHT-150), (CARD_WIDTH-80, CARD_HEIGHT-150)]

    for px, py in positions:
        # Small figures watching/performing
        draw.ellipse([px-8, py-20, px+8, py-10],
                    fill=(200, 180, 160))
        draw.rectangle([px-10, py-10, px+10, py+10],
                      fill=(random.choice([(180, 60, 60), (60, 80, 180)])))

    # Center: small puppet stage - craft within craft
    stage_x = CARD_WIDTH // 2
    stage_y = CARD_HEIGHT // 2
    draw.rectangle([stage_x-30, stage_y-20, stage_x+30, stage_y+10],
                  fill=(139, 69, 19))

    # Tiny puppet visible
    draw.ellipse([stage_x-5, stage_y-15, stage_x+5, stage_y-8],
                fill=(200, 180, 150))

    return img


def draw_five_of_puppets():
    """Five of Puppets: Performance failing, strings tangled, craft frustrated"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # FIVE control bars - but chaotic
    control_y = CARD_HEIGHT // 4

    for i, cx in enumerate([50, 100, CARD_WIDTH//2, CARD_WIDTH-100, CARD_WIDTH-50]):
        # Control bar at odd angles
        angle = random.randint(-15, 15)
        draw.rectangle([cx-18, control_y-4, cx+18, control_y+4],
                      fill=PuppetsColors.SECONDARY)

        # Puppet below - tangled
        puppet_y = CARD_HEIGHT - 120 + random.randint(-20, 20)
        draw.ellipse([cx-8, puppet_y-25, cx+8, puppet_y-15],
                    fill=(200, 180, 150))

        # TANGLED strings
        for j in range(4):
            sx = cx + random.randint(-15, 15)
            ex = cx + random.randint(-10, 10)
            ey = puppet_y - 25 + random.randint(-5, 5)

            draw.line([(sx, control_y+4), (ex, ey)],
                     fill=PuppetsColors.STRING, width=1)

    # Dark stage - failure
    draw.rectangle([0, CARD_HEIGHT-60, CARD_WIDTH, CARD_HEIGHT],
                  fill=(10, 10, 10))

    return img


def draw_eight_of_puppets():
    """Eight of Puppets: Craft becoming mechanical, performance without heart"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # EIGHT identical puppets - mass production
    for row in range(2):
        for col in range(4):
            px = 45 + col * 60
            py = CARD_HEIGHT//2 + 50 + row * 90

            # Each puppet IDENTICAL
            draw.ellipse([px-8, py-25, px+8, py-15],
                        fill=(200, 180, 150))
            draw.polygon([
                (px, py-15),
                (px-10, py+8),
                (px+10, py+8)
            ], fill=(180, 140, 60))

            # Identical strings
            control_y = py - 60
            for sx in [px-5, px+5]:
                draw.line([(sx, control_y), (sx, py-25)],
                         fill=PuppetsColors.STRING, width=1)

    # Factory-like grid
    for x in range(0, CARD_WIDTH, 60):
        draw.line([(x, 0), (x, CARD_HEIGHT)],
                 fill=(30, 30, 30), width=1)

    return img


def draw_singer_of_puppets():
    """Singer of Puppets: Voice as craft, emotion staged"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # SPOTLIGHT - dramatic
    for y in range(CARD_HEIGHT):
        for x in range(CARD_WIDTH):
            dist = math.sqrt((x - CARD_WIDTH//2)**2 + (y - CARD_HEIGHT//2)**2)
            brightness = max(0, int(150 - dist * 0.8))
            draw.point((x, y), fill=(brightness//3, brightness//4, 0))

    # SINGER - center stage
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Head
    draw.ellipse([fig_x-18, fig_y-55, fig_x+18, fig_y-25],
                fill=(220, 200, 180))

    # Theatrical costume
    draw.polygon([
        (fig_x, fig_y-25),
        (fig_x-35, fig_y+40),
        (fig_x+35, fig_y+40)
    ], fill=(180, 60, 60))

    # Mouth OPEN - performing
    draw.ellipse([fig_x-10, fig_y-45, fig_x+10, fig_y-38],
                fill=(200, 100, 100))

    # But STRINGS visible - even the voice is controlled
    control_y = 80
    for sx in [fig_x-10, fig_x-3, fig_x+3, fig_x+10]:
        draw.line([(sx, control_y), (sx, fig_y-55)],
                 fill=PuppetsColors.STRING, width=1)

    # Control bar
    draw.rectangle([fig_x-25, control_y-5, fig_x+25, control_y+5],
                  fill=PuppetsColors.SECONDARY)

    # Musical notes - but theatrical, staged
    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        nx = fig_x + int(70 * math.cos(rad))
        ny = fig_y + int(70 * math.sin(rad))
        draw_musical_note(draw, nx, ny, 8, PuppetsColors.HIGHLIGHT)

    return img


def draw_officer_of_puppets():
    """Officer of Puppets: Authority through spectacle, command as performance"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # MAXIMUM drama - this is power AS theater
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Dramatic radiating light
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        ray_length = 150
        draw.line([
            (fig_x, fig_y),
            (fig_x + int(ray_length * math.cos(rad)),
             fig_y + int(ray_length * math.sin(rad)))
        ], fill=PuppetsColors.SECONDARY, width=3)

    # THE FIGURE - commanding, theatrical
    # Head
    draw.ellipse([fig_x-22, fig_y-65, fig_x+22, fig_y-30],
                fill=(200, 180, 160))

    # Dramatic costume - part uniform, part theater
    draw.rectangle([fig_x-35, fig_y-30, fig_x+35, fig_y+50],
                  fill=PuppetsColors.PRIMARY)

    # Gold epaulettes
    draw.rectangle([fig_x-35, fig_y-30, fig_x-25, fig_y-15],
                  fill=PuppetsColors.SECONDARY)
    draw.rectangle([fig_x+25, fig_y-30, fig_x+35, fig_y-15],
                  fill=PuppetsColors.SECONDARY)

    # MANY control bars - commanding multiple puppets
    for i, bar_x in enumerate([fig_x-50, fig_x, fig_x+50]):
        bar_y = fig_y + 70 + i * 10
        draw.rectangle([bar_x-20, bar_y-4, bar_x+20, bar_y+4],
                      fill=PuppetsColors.SECONDARY)

        # Strings to unseen puppets below
        for sx in [bar_x-10, bar_x+10]:
            draw.line([(sx, bar_y+4), (sx, CARD_HEIGHT)],
                     fill=PuppetsColors.STRING, width=1)

    # Border - theatrical proscenium
    draw.rectangle([8, 8, CARD_WIDTH-8, CARD_HEIGHT-8],
                  outline=PuppetsColors.SECONDARY, width=6)

    return img


# === MOUNTAINS SUIT ADDITIONS ===

def draw_four_of_mountains():
    """Four of Mountains: Sanctuary in stone, ancient refuge"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # FOUR standing stones - ancient sanctuary
    stone_y = CARD_HEIGHT * 2 // 3

    for sx in [70, 120, CARD_WIDTH-120, CARD_WIDTH-70]:
        # Standing stone
        draw.rectangle([sx-15, stone_y-60, sx+15, stone_y],
                      fill=MountainsColors.PRIMARY)

        # Weathering
        for i in range(5):
            wy = stone_y - random.randint(20, 50)
            draw.line([(sx-12, wy), (sx+12, wy)],
                     fill=MountainsColors.SHADOW, width=2)

    # CENTER - safe space between stones
    center_x = CARD_WIDTH // 2
    draw.ellipse([center_x-30, stone_y-20, center_x+30, stone_y+5],
                fill=MountainsColors.GROUND)

    # Fire in center - warmth, gathering
    for r in range(15, 0, -2):
        color = (255 - r*10, 200 - r*8, 0)
        draw.ellipse([center_x-r, stone_y-15-r, center_x+r, stone_y-15+r],
                    fill=color)

    # Edelweiss growing at each stone
    for sx in [70, 120, CARD_WIDTH-120, CARD_WIDTH-70]:
        draw_edelweiss(draw, sx+20, stone_y-10, 10)

    return img


def draw_five_of_mountains():
    """Five of Mountains: Tradition challenged, old ways questioned"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Background - mountains in mist
    get_mountains_background(draw, with_peaks=True)

    # FIVE figures - one apart from four
    # Four together - traditional
    for i, fx in enumerate([60, 100, 140, 180]):
        fy = CARD_HEIGHT - 120

        draw.ellipse([fx-10, fy-30, fx+10, fy-15],
                    fill=(180, 160, 140))
        draw.rectangle([fx-12, fy-15, fx+12, fy+20],
                      fill=(100, 80, 60))

    # FIFTH figure - separate, questioning
    apart_x = CARD_WIDTH - 70
    apart_y = CARD_HEIGHT - 140

    draw.ellipse([apart_x-12, apart_y-35, apart_x+12, apart_y-15],
                fill=(180, 160, 140))
    draw.rectangle([apart_x-14, apart_y-15, apart_x+14, apart_y+25],
                  fill=(120, 100, 80))

    # Gap between them - distance
    draw.line([(190, CARD_HEIGHT-100), (apart_x-20, apart_y)],
             fill=MountainsColors.SHADOW, width=3)

    return img


def draw_eight_of_mountains():
    """Eight of Mountains: Transmission becoming rote, wisdom ossified"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Gray, heavy background
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(100, 100, 110))

    # EIGHT identical stone markers - tradition hardened
    for row in range(2):
        for col in range(4):
            sx = 45 + col * 60
            sy = CARD_HEIGHT//3 + row * 120

            # Stone marker - same shape, same size
            draw.rectangle([sx-12, sy-40, sx+12, sy],
                          fill=MountainsColors.PRIMARY)

            # Same symbol on each
            draw.line([(sx, sy-35), (sx, sy-25)],
                     fill=MountainsColors.ACCENT, width=2)
            draw.line([(sx-5, sy-30), (sx+5, sy-30)],
                     fill=MountainsColors.ACCENT, width=2)

    # No flowers - lifeless
    # Heavy, oppressive sky
    for y in range(0, CARD_HEIGHT//3):
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(90, 90, 100))

    return img


def draw_singer_of_mountains():
    """Singer of Mountains: Voice carrying ancient songs forward"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # SINGER - voice of the mountains
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # Mountain-stone quality
    for r in range(80, 0, -4):
        gray = 100 + r
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    fill=(gray, gray, gray+10), outline=(gray, gray, gray+10))

    # Head
    draw.ellipse([fig_x-18, fig_y-55, fig_x+18, fig_y-25],
                fill=(180, 160, 140))

    # Traditional clothing
    draw.polygon([
        (fig_x, fig_y-25),
        (fig_x-30, fig_y+35),
        (fig_x+30, fig_y+35)
    ], fill=(100, 80, 60))

    # Mouth OPEN - singing the old songs
    draw.ellipse([fig_x-12, fig_y-45, fig_x+12, fig_y-38],
                fill=(180, 100, 100))

    # Sound waves - connecting to mountains
    for r in [50, 70, 90]:
        draw.arc([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                start=0, end=180, fill=MountainsColors.ACCENT, width=3)

    # Notes floating - but ancient symbols, not modern notation
    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        nx = fig_x + int(70 * math.cos(rad))
        ny = fig_y + int(70 * math.sin(rad))

        # Ancient symbol (simple circle)
        draw.ellipse([nx-5, ny-5, nx+5, ny+5],
                    fill=MountainsColors.ACCENT)

    # Edelweiss crown
    for offset in [-15, 0, 15]:
        draw_edelweiss(draw, fig_x+offset, fig_y-65, 8)

    return img


def draw_puppeteer_of_mountains():
    """Puppeteer of Mountains: Ancient control, tradition as manipulation"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=False)

    # ELDER figure - tradition weaponized
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 3

    # Stone-like authority
    for r in range(100, 0, -5):
        gray = 80 + r//2
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    fill=(gray, gray-10, gray-20), outline=(gray, gray-10, gray-20))

    # Head - ancient, stern
    draw.ellipse([fig_x-22, fig_y-60, fig_x+22, fig_y-25],
                fill=(160, 140, 120))

    # Traditional robes
    draw.polygon([
        (fig_x, fig_y-25),
        (fig_x-40, fig_y+50),
        (fig_x+40, fig_y+50)
    ], fill=(60, 50, 40))

    # Staff - symbol of authority
    staff_x = fig_x + 50
    draw.line([(staff_x, fig_y-50), (staff_x, fig_y+70)],
             fill=(80, 60, 40), width=10)

    # Top of staff - stone
    draw.ellipse([staff_x-8, fig_y-60, staff_x+8, fig_y-50],
                fill=MountainsColors.PRIMARY)

    # But STRINGS from other hand - tradition as control
    hand_x = fig_x - 40
    hand_y = fig_y

    # Control strings to figures below
    for i, puppet_x in enumerate([CARD_WIDTH//4, CARD_WIDTH//2, 3*CARD_WIDTH//4]):
        puppet_y = CARD_HEIGHT - 80

        # Small figure below
        draw.ellipse([puppet_x-6, puppet_y-20, puppet_x+6, puppet_y-12],
                    fill=(180, 160, 140))
        draw.rectangle([puppet_x-8, puppet_y-12, puppet_x+8, puppet_y+5],
                      fill=(100, 80, 60))

        # Control strings
        draw.line([(hand_x, hand_y), (puppet_x, puppet_y-20)],
                 fill=(120, 120, 120), width=1)

    return img


# Generate all these additional cards
if __name__ == '__main__':
    print("🎨 CONTINUING THE CREATIVE JOURNEY! More cards! 🎨\n")

    cards_to_generate = [
        # Puppets additions
        ("puppets-01", draw_two_of_puppets),
        ("puppets-03", draw_four_of_puppets),
        ("puppets-04", draw_five_of_puppets),
        ("puppets-07", draw_eight_of_puppets),
        ("puppets-10", draw_singer_of_puppets),
        ("puppets-13", draw_officer_of_puppets),

        # Mountains additions
        ("mountains-03", draw_four_of_mountains),
        ("mountains-04", draw_five_of_mountains),
        ("mountains-07", draw_eight_of_mountains),
        ("mountains-10", draw_singer_of_mountains),
        ("mountains-13", draw_puppeteer_of_mountains),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} more cards! ✨")
    print("🎭 The deck takes shape... 🎭")
