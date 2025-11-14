#!/usr/bin/env python3
"""
Generate Mountains suit cards
Authentic/Transmissive - permanence, transmission, ancient wisdom

Weathered stone romanticism, Caspar David Friedrich sublime
Each card explores what endures, what is passed down, what mountains remember
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

def draw_ace_of_mountains():
    """Ace: The first stone - foundation entering, permanence offered"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Sky - eternal, waiting
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     MountainsColors.HIGHLIGHT, MountainsColors.PRIMARY)

    # Ground - ancient earth
    draw.rectangle([0, CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT],
                  fill=MountainsColors.GROUND)

    # THE FIRST STONE - singular, perfect, placed
    stone_x, stone_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # Glow of significance
    for r in range(60, 0, -3):
        alpha = 255 - r * 3
        gray = 150 + r
        draw.ellipse([stone_x-r, stone_y-r, stone_x+r, stone_y+r],
                    fill=(gray, gray, gray), outline=(gray, gray, gray))

    # The stone itself - weighty, real
    stone_size = 40
    draw.ellipse([stone_x-stone_size, stone_y-stone_size,
                 stone_x+stone_size, stone_y+stone_size],
                fill=MountainsColors.PRIMARY)

    # Weathering marks - already ancient
    for i in range(10):
        mx = stone_x + random.randint(-stone_size//2, stone_size//2)
        my = stone_y + random.randint(-stone_size//2, stone_size//2)
        draw.line([(mx-5, my), (mx+5, my)],
                 fill=MountainsColors.SHADOW, width=2)

    # Distant peak - where this came from
    draw_mountain_peak(draw, CARD_WIDTH//2, CARD_HEIGHT//3, 100, 80,
                      MountainsColors.SHADOW, snow=True)

    # Edelweiss growing from stone - life and stone together
    draw_edelweiss(draw, stone_x + stone_size + 15, stone_y, 10)

    return img


def draw_three_of_mountains():
    """Three: Learning what mountains teach - the songs they sing"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # THREE FIGURES on the mountainside - listening, learning
    figures_y = CARD_HEIGHT * 2 // 3

    for i, fx in enumerate([80, CARD_WIDTH//2, CARD_WIDTH-80]):
        # Each figure sitting, receptive
        # Head
        draw.ellipse([fx-12, figures_y-30, fx+12, figures_y-10],
                    fill=(200, 180, 160))

        # Body - simple clothes
        draw.polygon([
            (fx, figures_y-10),
            (fx-18, figures_y+20),
            (fx+18, figures_y+20)
        ], fill=(120, 100, 80))

        # LISTENING posture - heads tilted up
        draw.line([(fx, figures_y-20), (fx-3, figures_y-35)],
                 fill=(200, 180, 160), width=3)

    # Sound waves from the mountain - the ancient song
    peak_x, peak_y = CARD_WIDTH // 2, 80
    for r in [40, 60, 80, 100]:
        draw.arc([peak_x-r, peak_y-r, peak_x+r, peak_y+r],
                start=30, end=150, fill=MountainsColors.ACCENT, width=3)

    # Edelweiss scattered - the mountain gives its teaching freely
    for i in range(8):
        ex = random.randint(40, CARD_WIDTH-40)
        ey = random.randint(CARD_HEIGHT//2, CARD_HEIGHT-40)
        draw_edelweiss(draw, ex, ey, 8)

    return img


def draw_seven_of_mountains():
    """Seven: Choice to honor or exploit - mountains wait for your answer"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Split scene - two paths
    # Left: respectful approach
    draw.rectangle([0, 0, CARD_WIDTH//2, CARD_HEIGHT],
                  fill=MountainsColors.GROUND)

    # Right: instrumental approach
    draw.rectangle([CARD_WIDTH//2, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(60, 50, 40))  # Darker, exploited

    # Mountain in center - unchanged, patient
    for side_x in [CARD_WIDTH//4, 3*CARD_WIDTH//4]:
        draw_mountain_peak(draw, side_x, CARD_HEIGHT//3, 80, 70,
                          MountainsColors.PRIMARY, snow=True)

    # Figure at CENTER - choosing
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    draw.ellipse([fig_x-15, fig_y-50, fig_x+15, fig_y-20],
                fill=(180, 160, 140))
    draw.rectangle([fig_x-20, fig_y-20, fig_x+20, fig_y+30],
                  fill=(100, 80, 60))

    # Left hand - open, receiving
    draw.ellipse([fig_x-35, fig_y-10, fig_x-20, fig_y+5],
                fill=(180, 160, 140))

    # Right hand - grasping, taking
    draw.ellipse([fig_x+20, fig_y-10, fig_x+35, fig_y+5],
                fill=(180, 160, 140))

    # Left path: edelweiss blooming
    for i in range(5):
        ex = random.randint(20, CARD_WIDTH//2-20)
        ey = random.randint(CARD_HEIGHT//2, CARD_HEIGHT-30)
        draw_edelweiss(draw, ex, ey, 10)

    # Right path: broken stones
    for i in range(8):
        sx = random.randint(CARD_WIDTH//2+20, CARD_WIDTH-20)
        sy = random.randint(CARD_HEIGHT//2, CARD_HEIGHT-30)
        draw.polygon([
            (sx, sy),
            (sx+8, sy-5),
            (sx+5, sy+8)
        ], fill=MountainsColors.SHADOW)

    return img


def draw_ten_of_mountains():
    """Ten: Transmission complete - ancient song learned, mountains fulfilled"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Monumental sky - achievement, permanence
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     MountainsColors.PEAK, MountainsColors.HIGHLIGHT)

    # RING OF MOUNTAINS - complete circle, eternal
    for i in range(10):
        angle = (i * 36) - 90  # Start from top
        rad = math.radians(angle)

        # Position around circle
        distance = 100
        mx = CARD_WIDTH//2 + int(distance * math.cos(rad))
        my = CARD_HEIGHT//2 + int(distance * math.sin(rad))

        # Each mountain peak
        peak_size = 30 + (i % 3) * 10
        draw_mountain_peak(draw, mx, my, 40, peak_size,
                          MountainsColors.PRIMARY, snow=True)

    # Center: FIGURE standing, song learned, passing it on
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Radiant with transmitted wisdom
    for r in range(50, 0, -3):
        gray = 200 - r
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    fill=(gray, gray, gray+20), outline=(gray, gray, gray+20))

    # The figure - transformed by what they've learned
    draw.ellipse([fig_x-15, fig_y-40, fig_x+15, fig_y-15],
                fill=MountainsColors.PEAK)
    draw.polygon([
        (fig_x, fig_y-15),
        (fig_x-25, fig_y+25),
        (fig_x+25, fig_y+25)
    ], fill=MountainsColors.PRIMARY)

    # Arms raised - teaching, transmitting
    draw.line([(fig_x-25, fig_y), (fig_x-45, fig_y-30)],
             fill=MountainsColors.PEAK, width=8)
    draw.line([(fig_x+25, fig_y), (fig_x+45, fig_y-30)],
             fill=MountainsColors.PEAK, width=8)

    # Sound waves emanating - the song continues
    for r in [60, 80, 100, 120]:
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    outline=MountainsColors.ACCENT, width=2)

    # Edelweiss everywhere - abundance, flourishing
    for i in range(15):
        ex = random.randint(30, CARD_WIDTH-30)
        ey = random.randint(CARD_HEIGHT-100, CARD_HEIGHT-20)
        draw_edelweiss(draw, ex, ey, 12)

    return img


def draw_goatherd_of_mountains():
    """Goatherd of Mountains - authentic transmission embodied"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # THE GOATHERD - at home in high places
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # Aura of mountain wisdom
    for r in range(80, 0, -4):
        gray = 120 + r
        draw.ellipse([fig_x-r, fig_y-r-20, fig_x+r, fig_y+r+20],
                    fill=(gray, gray, gray+20), outline=(gray, gray, gray+20))

    # Head - weathered, knowing
    draw.ellipse([fig_x-20, fig_y-60, fig_x+20, fig_y-25],
                fill=(160, 140, 120))

    # Traditional costume - passed down
    draw.polygon([
        (fig_x, fig_y-25),
        (fig_x-35, fig_y+40),
        (fig_x+35, fig_y+40)
    ], fill=(100, 80, 60))

    # Staff - ancient, smooth from use
    staff_x = fig_x + 40
    draw.line([(staff_x, fig_y-40), (staff_x, fig_y+60)],
             fill=(80, 60, 40), width=8)

    # Edelweiss in hat
    draw_edelweiss(draw, fig_x-15, fig_y-70, 12)

    # GOATS around - the living connection
    for i, gx in enumerate([fig_x-80, fig_x-60, fig_x+60, fig_x+80]):
        gy = CARD_HEIGHT - 100 + random.randint(-20, 20)

        # Simple goat shape
        # Body
        draw.ellipse([gx-12, gy-15, gx+12, gy+5],
                    fill=(180, 180, 180))
        # Head
        draw.ellipse([gx+8, gy-20, gx+18, gy-10],
                    fill=(200, 200, 200))
        # Little horns
        draw.line([(gx+10, gy-20), (gx+8, gy-25)],
                 fill=(80, 80, 80), width=2)
        draw.line([(gx+16, gy-20), (gx+18, gy-25)],
                 fill=(80, 80, 80), width=2)

    # The mountains acknowledge - peaks align
    for angle in [30, 60, 120, 150]:
        rad = math.radians(angle)
        px = fig_x + int(100 * math.cos(rad))
        py = 100
        draw.line([(fig_x, fig_y-60), (px, py)],
                 fill=MountainsColors.ACCENT, width=2)

    # Border of ancient stone
    draw.rectangle([10, 10, CARD_WIDTH-10, CARD_HEIGHT-10],
                  outline=MountainsColors.PRIMARY, width=6)

    return img


# Generate Mountains cards!
if __name__ == '__main__':
    print("🏔️ ANCIENT PERMANENCE! Creating Mountains suit! 🏔️\n")

    cards_to_generate = [
        ("mountains-00", draw_ace_of_mountains),
        ("mountains-02", draw_three_of_mountains),
        ("mountains-06", draw_seven_of_mountains),
        ("mountains-09", draw_ten_of_mountains),
        ("mountains-12", draw_goatherd_of_mountains),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} Mountains cards! ✨")
    print("⛰️  What endures, what is transmitted, what mountains remember... ⛰️")
