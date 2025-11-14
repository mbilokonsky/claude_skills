#!/usr/bin/env python3
"""
Generate additional cards for all suits to complete the deck
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

# === SONGS SUIT ADDITIONS ===

def draw_four_of_songs():
    """Four of Songs: Rest in joy, sanctuary of sound"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_songs_background(draw)

    # FOUR corners - musical refuge
    corners = [
        (60, 100), (CARD_WIDTH-60, 100),
        (60, CARD_HEIGHT-100), (CARD_WIDTH-60, CARD_HEIGHT-100)
    ]

    for cx, cy in corners:
        # Musical note at each corner
        draw_musical_note(draw, cx, cy, 12, SongsColors.ACCENT_3)

        # Gentle glow
        for r in range(30, 0, -3):
            draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                        outline=SongsColors.HIGHLIGHT, width=1)

    # CENTER figure - resting, peaceful
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Lying down peacefully
    draw.ellipse([fig_x-15, fig_y-10, fig_x+15, fig_y+10],
                fill=(220, 200, 180))
    draw.ellipse([fig_x-30, fig_y-5, fig_x+30, fig_y+25],
                fill=(200, 220, 240))

    # Wildflowers all around
    for i in range(20):
        fx = random.randint(40, CARD_WIDTH-40)
        fy = random.randint(CARD_HEIGHT//2, CARD_HEIGHT-30)
        color = random.choice([SongsColors.ACCENT_1, SongsColors.ACCENT_2, SongsColors.ACCENT_3])
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=color)

    return img


def draw_five_of_songs():
    """Five of Songs: Song interrupted, silenced - joy paused"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_songs_background(draw)

    # A mouth MID-SONG - but stopping
    mouth_x, mouth_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Face
    draw.ellipse([mouth_x-40, mouth_y-60, mouth_x+40, mouth_y+20],
                fill=(220, 200, 180))

    # Open mouth - interrupted
    draw.ellipse([mouth_x-25, mouth_y-10, mouth_x+25, mouth_y+10],
                fill=(220, 100, 100))

    # Musical notes FALLING - song interrupted
    for i in range(5):
        nx = mouth_x + random.randint(-40, 40)
        ny = mouth_y + 40 + i*20
        draw_musical_note(draw, nx, ny, 8, (150, 150, 150))

    # Hand covering mouth - external silencing
    draw.ellipse([mouth_x+20, mouth_y-20, mouth_x+60, mouth_y+20],
                fill=(180, 160, 140))

    return img


def draw_eight_of_songs():
    """Eight of Songs: Song becoming rote, joy memorized not felt"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Faded colors - joy going mechanical
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     (200, 200, 210), (180, 190, 200))
    draw.rectangle([0, CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT],
                  fill=(100, 120, 100))

    # EIGHT identical figures - singing but mechanical
    for row in range(2):
        for col in range(4):
            fx = 45 + col * 60
            fy = CARD_HEIGHT//2 + 40 + row * 80

            # Each figure IDENTICAL
            draw.ellipse([fx-10, fy-25, fx+10, fy-10],
                        fill=(180, 180, 180))
            draw.rectangle([fx-12, fy-10, fx+12, fy+25],
                          fill=(140, 140, 140))

            # Same mouth, same note
            draw.ellipse([fx-4, fy-18, fx+4, fy-14],
                        fill=(100, 100, 100))
            draw_musical_note(draw, fx, fy-40, 7, (160, 160, 160))

    return img


def draw_goatherd_of_songs():
    """Goatherd of Songs: Playful authenticity, pure creative joy"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_songs_background(draw)

    # FIGURE - dancing, puppet show, PLAY
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # Rainbow joy aura
    for r in range(100, 0, -5):
        hue = (r * 3) % 255
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    outline=(255-hue//2, 150+hue//3, 200), width=2)

    # Head
    draw.ellipse([fig_x-18, fig_y-55, fig_x+18, fig_y-25],
                fill=(220, 200, 180))

    # Lederhosen costume - theatrical
    draw.polygon([
        (fig_x, fig_y-25),
        (fig_x-30, fig_y+30),
        (fig_x+30, fig_y+30)
    ], fill=(180, 60, 60))

    # Arms OUT - performing
    draw.line([(fig_x-30, fig_y), (fig_x-70, fig_y-20)],
             fill=(220, 200, 180), width=10)
    draw.line([(fig_x+30, fig_y), (fig_x+70, fig_y-20)],
             fill=(220, 200, 180), width=10)

    # Puppet theater at feet
    theater_y = CARD_HEIGHT - 70
    draw.rectangle([fig_x-35, theater_y-25, fig_x+35, theater_y],
                  fill=(139, 69, 19))

    # Tiny puppets
    for px in [fig_x-20, fig_x, fig_x+20]:
        draw.ellipse([px-4, theater_y-20, px+4, theater_y-12],
                    fill=(random.randint(200, 255), random.randint(150, 220), random.randint(100, 200)))

    # Musical notes everywhere
    for i in range(12):
        nx = random.randint(40, CARD_WIDTH-40)
        ny = random.randint(40, CARD_HEIGHT-100)
        draw_musical_note(draw, nx, ny, 7,
                         (random.randint(200, 255), random.randint(150, 250), random.randint(100, 200)))

    return img


def draw_officer_of_songs():
    """Officer of Songs: Disciplined musician, technique mastered"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Blended sky and structure
    for y in range(CARD_HEIGHT):
        t = y / CARD_HEIGHT
        r = int(135 + (25 - 135) * t)
        g = int(206 + (25 - 206) * t)
        b = int(250 + (112 - 250) * t)
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

    # CONDUCTOR - authoritative but musical
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Precise aura
    for r in range(0, 100, 20):
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    outline=SongsColors.ACCENT_3, width=2)

    # Head
    draw.ellipse([fig_x-20, fig_y-65, fig_x+20, fig_y-30],
                fill=(200, 180, 160))

    # Formal concert attire
    draw.rectangle([fig_x-32, fig_y-30, fig_x+32, fig_y+45],
                  fill=(20, 20, 20))
    draw.rectangle([fig_x-10, fig_y-30, fig_x+10, fig_y+45],
                  fill=(255, 255, 255))

    # BATON
    baton_x, baton_y = fig_x + 40, fig_y - 30
    draw.line([(baton_x, baton_y), (baton_x+35, baton_y-35)],
             fill=(255, 255, 255), width=4)

    # Hand
    draw.ellipse([baton_x-8, baton_y-8, baton_x+8, baton_y+8],
                fill=(200, 180, 160))

    # Sheet music
    music_x, music_y = fig_x - 40, fig_y
    draw.rectangle([music_x-15, music_y-20, music_x+15, music_y+20],
                  fill=(255, 255, 240))

    # Staff lines
    for i in range(5):
        draw.line([(music_x-12, music_y-15+i*8), (music_x+12, music_y-15+i*8)],
                 fill=(0, 0, 0), width=1)

    # Ordered notes floating
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        nx = fig_x + int(90 * math.cos(rad))
        ny = fig_y + int(90 * math.sin(rad))
        draw_musical_note(draw, nx, ny, 8, SongsColors.PRIMARY)

    return img


# === WHISTLES SUIT ADDITIONS ===

def draw_two_of_whistles():
    """Two of Whistles: Partnership in discipline, mutual structure"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_whistles_background(draw)

    # TWO figures - mirrored, coordinated
    left_x, right_x = CARD_WIDTH // 3, 2 * CARD_WIDTH // 3
    fig_y = CARD_HEIGHT * 2 // 3

    for fx in [left_x, right_x]:
        # Each figure in formation
        draw.ellipse([fx-12, fig_y-35, fx+12, fig_y-15],
                    fill=(200, 200, 220))
        draw.rectangle([fx-15, fig_y-15, fx+15, fig_y+25],
                      fill=WhistlesColors.SECONDARY)

    # Whistles synchronized
    for fx in [left_x, right_x]:
        draw_whistle(draw, fx, fig_y+40, 15, WhistlesColors.ACCENT)

    # Connection line - coordination
    draw.line([(left_x, fig_y), (right_x, fig_y)],
             fill=WhistlesColors.ACCENT, width=3)

    return img


def draw_five_of_whistles():
    """Five of Whistles: Discipline threatened, structure under strain"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Background with disorder creeping in
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=WhistlesColors.PRIMARY)

    # Grid BREAKING
    for x in range(0, CARD_WIDTH, 40):
        offset = random.randint(-5, 5)
        draw.line([(x+offset, 0), (x-offset, CARD_HEIGHT)],
                 fill=(35, 35, 122), width=1)

    # FIVE figures - formation failing
    positions = [
        (CARD_WIDTH//2, CARD_HEIGHT//3),
        (CARD_WIDTH//3, CARD_HEIGHT//2),
        (2*CARD_WIDTH//3, CARD_HEIGHT//2),
        (CARD_WIDTH//3, 2*CARD_HEIGHT//3),
        (2*CARD_WIDTH//3, 2*CARD_HEIGHT//3)
    ]

    for i, (fx, fy) in enumerate(positions):
        # Some figures out of alignment
        offset = random.randint(-10, 10) if i > 2 else 0

        draw.ellipse([fx-10+offset, fy-25, fx+10+offset, fy-10],
                    fill=(180, 180, 200))
        draw.rectangle([fx-12+offset, fy-10, fx+12+offset, fy+15],
                      fill=WhistlesColors.SECONDARY)

    return img


def draw_singer_of_whistles():
    """Singer of Whistles: Discipline expressed through voice, ordered beauty"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Structured but musical background
    for y in range(CARD_HEIGHT):
        t = y / CARD_HEIGHT
        r = int(25 + (135 - 25) * t)
        g = int(25 + (206 - 25) * t)
        b = int(112 + (250 - 112) * t)
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

    # Grid lines - subtle
    for y in range(0, CARD_HEIGHT, 40):
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(35, 35, 122), width=1)

    # SINGER - precise, powerful
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Head
    draw.ellipse([fig_x-18, fig_y-60, fig_x+18, fig_y-25],
                fill=(200, 200, 220))

    # Uniform but singing
    draw.rectangle([fig_x-25, fig_y-25, fig_x+25, fig_y+40],
                  fill=WhistlesColors.SECONDARY)

    # Mouth OPEN - disciplined voice
    draw.ellipse([fig_x-12, fig_y-45, fig_x+12, fig_y-35],
                fill=(100, 120, 180))

    # Musical notes but GEOMETRIC
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        nx = fig_x + int(80 * math.cos(rad))
        ny = fig_y + int(80 * math.sin(rad))

        # Precise musical note
        draw_musical_note(draw, nx, ny, 8, WhistlesColors.ACCENT)

    # Sound waves - ordered
    for r in [50, 70, 90]:
        draw.ellipse([fig_x-r, fig_y-r//2, fig_x+r, fig_y+r//2],
                    outline=(200, 200, 255), width=2)

    return img


def draw_puppeteer_of_whistles():
    """Puppeteer of Whistles: Instrumental control disguised as care"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Dark navy with geometric precision
    get_whistles_background(draw)

    # PUPPETEER figure - commanding
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 3

    # Head - stern
    draw.ellipse([fig_x-18, fig_y-55, fig_x+18, fig_y-25],
                fill=(200, 200, 220))

    # Uniform - authority
    draw.rectangle([fig_x-28, fig_y-25, fig_x+28, fig_y+40],
                  fill=WhistlesColors.PRIMARY)

    # Whistle as control device
    draw_whistle(draw, fig_x, fig_y+55, 20, WhistlesColors.ACCENT)

    # STRINGS from hands to figures below - disciplinary control
    for side, sx in [(-1, fig_x-60), (1, fig_x+60)]:
        # Hand
        draw.ellipse([sx-10, fig_y-10, sx+10, fig_y+10],
                    fill=(200, 200, 220))

        # Puppet below
        puppet_y = CARD_HEIGHT - 80
        draw.ellipse([sx-8, puppet_y-20, sx+8, puppet_y-10],
                    fill=(180, 180, 200))
        draw.rectangle([sx-10, puppet_y-10, sx+10, puppet_y+10],
                      fill=WhistlesColors.SECONDARY)

        # Control strings
        draw_puppet_strings(draw, sx, fig_y+10, sx, puppet_y-20,
                           (192, 192, 192))

    return img


# Generate all additional cards
if __name__ == '__main__':
    print("🎨 FILLING OUT THE DECK! Creating more cards! 🎨\n")

    cards_to_generate = [
        # Songs additions
        ("songs-03", draw_four_of_songs),
        ("songs-04", draw_five_of_songs),
        ("songs-07", draw_eight_of_songs),
        ("songs-12", draw_goatherd_of_songs),
        ("songs-13", draw_officer_of_songs),

        # Whistles additions
        ("whistles-01", draw_two_of_whistles),
        ("whistles-04", draw_five_of_whistles),
        ("whistles-10", draw_singer_of_whistles),
        ("whistles-12", draw_puppeteer_of_whistles),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} more cards! ✨")
    print("🎯 The deck grows richer...")
