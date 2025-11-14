#!/usr/bin/env python3
"""
Generate Whistles suit cards
Instrumental/Transmissive - discipline, order, structure

Geometric precision, Bauhaus clarity - can be protective or oppressive
Each card explores the dialectic of necessary structure vs. crushing control
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

def draw_ace_of_whistles():
    """Ace: Discipline first entering - the first whistle blown"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_whistles_background(draw)

    # A single WHISTLE in center - gleaming, perfect
    whistle_x, whistle_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Glow of authority/order
    for r in range(50, 0, -3):
        alpha = 255 - r * 4
        draw.ellipse([whistle_x-r, whistle_y-r, whistle_x+r, whistle_y+r],
                    fill=(100, 100, 150), outline=(100, 100, 150))

    # The whistle itself - brass and important
    draw_whistle(draw, whistle_x, whistle_y, 25, WhistlesColors.ACCENT)

    # Sound waves emanating - the FIRST command
    for r in [40, 60, 80, 100, 120]:
        draw.ellipse([whistle_x-r, whistle_y-r, whistle_x+r, whistle_y+r],
                    outline=(200, 200, 255), width=3)

    # Small figure in distance - just beginning to respond
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT - 80
    draw.rectangle([fig_x-8, fig_y-20, fig_x+8, fig_y],
                  fill=(180, 180, 200))
    draw.ellipse([fig_x-6, fig_y-30, fig_x+6, fig_y-20],
                fill=(200, 200, 220))

    # Geometric lines - beginning of structure
    for y in [100, 150, 200, 250]:
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(45, 45, 132), width=2)

    return img


def draw_four_of_whistles():
    """Four: Sanctuary that rules build - structure as protection"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Navy background
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=WhistlesColors.PRIMARY)

    # A FORTRESS of order - geometric, precise, SAFE
    fortress_y = CARD_HEIGHT // 3

    # Strong vertical walls
    draw.rectangle([50, fortress_y, 90, CARD_HEIGHT-40],
                  fill=(180, 180, 200))
    draw.rectangle([CARD_WIDTH-90, fortress_y, CARD_WIDTH-50, CARD_HEIGHT-40],
                  fill=(180, 180, 200))

    # Horizontal structure
    draw.rectangle([50, fortress_y, CARD_WIDTH-50, fortress_y+30],
                  fill=(200, 200, 220))
    draw.rectangle([50, CARD_HEIGHT-70, CARD_WIDTH-50, CARD_HEIGHT-40],
                  fill=(200, 200, 220))

    # Grid of windows - order visible
    for wx in range(100, CARD_WIDTH-100, 40):
        for wy in range(fortress_y+50, CARD_HEIGHT-100, 50):
            draw.rectangle([wx, wy, wx+25, wy+30],
                          fill=(255, 255, 220))
            # Small figures visible - safe inside structure
            draw.ellipse([wx+8, wy+8, wx+17, wy+17],
                        fill=(100, 100, 120))

    # Geometric perfection - the beauty of order
    for i in range(5):
        y = fortress_y - (i+1) * 15
        draw.line([(70 + i*10, y), (CARD_WIDTH-70-i*10, y)],
                 fill=(150, 150, 170), width=2)

    # Protective boundary
    draw.rectangle([45, fortress_y-5, CARD_WIDTH-45, CARD_HEIGHT-35],
                  outline=WhistlesColors.ACCENT, width=4)

    return img


def draw_seven_of_whistles():
    """Seven: Choice to obey or resist - the whistle waits for answer"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Split composition - obedience vs resistance
    # Left: ordered, geometric, safe
    draw.rectangle([0, 0, CARD_WIDTH//2, CARD_HEIGHT],
                  fill=(35, 35, 122))

    # Geometric grid on left
    for x in range(20, CARD_WIDTH//2, 30):
        draw.line([(x, 0), (x, CARD_HEIGHT)],
                 fill=(45, 45, 132), width=1)
    for y in range(0, CARD_HEIGHT, 30):
        draw.line([(0, y), (CARD_WIDTH//2, y)],
                 fill=(45, 45, 132), width=1)

    # Right: darker, less structured, unknown
    draw.rectangle([CARD_WIDTH//2, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(20, 20, 80))

    # Breaking grid on right - freedom or chaos?
    for i in range(10):
        x = random.randint(CARD_WIDTH//2, CARD_WIDTH)
        y = random.randint(0, CARD_HEIGHT)
        draw.line([(x-20, y), (x+20, y)],
                 fill=(40, 40, 100), width=1)

    # Figure at CENTER - exactly between
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # The figure - torn
    draw.ellipse([fig_x-15, fig_y-50, fig_x+15, fig_y-20],
                fill=(180, 180, 200))
    draw.rectangle([fig_x-20, fig_y-20, fig_x+20, fig_y+30],
                  fill=(100, 100, 140))

    # One arm reaching toward order
    draw.line([(fig_x-20, fig_y), (fig_x-60, fig_y-20)],
             fill=(180, 180, 200), width=6)

    # One arm reaching toward freedom
    draw.line([(fig_x+20, fig_y), (fig_x+60, fig_y-20)],
             fill=(180, 180, 200), width=6)

    # WHISTLE ABOVE - waiting, commanding
    whistle_y = CARD_HEIGHT // 3
    draw_whistle(draw, fig_x, whistle_y, 20, WhistlesColors.ACCENT)

    # Sound waves - the command issued
    for r in [30, 45, 60]:
        draw.ellipse([fig_x-r, whistle_y-r//2, fig_x+r, whistle_y+r//2],
                    outline=(200, 200, 255), width=2)

    return img


def draw_ten_of_whistles():
    """Ten: Discipline complete - order fulfilled perfectly (for good or ill)"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Perfect geometric background - order at maximum
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=WhistlesColors.PRIMARY)

    # PERFECT FORMATION - could be triumph or horror
    # Grid of figures in exact precision
    fig_size = 20
    spacing = 35

    for row in range(3, 10):
        for col in range(2, 7):
            fx = col * spacing
            fy = row * spacing

            # Each figure identical, perfectly placed
            # Head
            draw.ellipse([fx-6, fy-15, fx+6, fy-5],
                        fill=(180, 180, 200))
            # Body - in formation
            draw.rectangle([fx-7, fy-5, fx+7, fy+10],
                          fill=WhistlesColors.SECONDARY)

    # Geometric perfection lines
    for i in range(10):
        y = i * (CARD_HEIGHT // 10)
        # Horizontal precision
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(45, 45, 132), width=1)

    for i in range(8):
        x = i * (CARD_WIDTH // 8)
        # Vertical precision
        draw.line([(x, 0), (x, CARD_HEIGHT)],
                 fill=(45, 45, 132), width=1)

    # Central whistle - at rest, purpose served
    center_y = CARD_HEIGHT // 4
    draw_whistle(draw, CARD_WIDTH//2, center_y, 30,
                WhistlesColors.ACCENT)

    # Brass gleam
    for r in range(40, 0, -3):
        draw.ellipse([CARD_WIDTH//2-r, center_y-r//2,
                     CARD_WIDTH//2+r, center_y+r//2],
                    fill=(220, 180, 100), outline=(220, 180, 100))

    # The question: is this beautiful order or perfect oppression?
    # Border - could be frame or cage
    draw.rectangle([10, 10, CARD_WIDTH-10, CARD_HEIGHT-10],
                  outline=WhistlesColors.ACCENT, width=6)

    return img


def draw_officer_of_whistles():
    """Officer of Whistles - discipline embodied, authority complete"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Maximum geometric precision
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=WhistlesColors.PRIMARY)

    # PERFECT GRID - order incarnate
    for x in range(0, CARD_WIDTH, 20):
        draw.line([(x, 0), (x, CARD_HEIGHT)],
                 fill=(35, 35, 122), width=1)
    for y in range(0, CARD_HEIGHT, 20):
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(35, 35, 122), width=1)

    # THE OFFICER - center, commanding
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Aura of AUTHORITY
    for r in range(80, 0, -4):
        draw.ellipse([fig_x-r, fig_y-r-30, fig_x+r, fig_y+r+30],
                    fill=(40, 40, 140), outline=(40, 40, 140))

    # Perfect uniform - WHITE and NAVY
    # Head
    draw.ellipse([fig_x-20, fig_y-70, fig_x+20, fig_y-30],
                fill=(200, 200, 220))

    # Uniform jacket - precise, formal
    draw.rectangle([fig_x-30, fig_y-30, fig_x+30, fig_y+40],
                  fill=WhistlesColors.SECONDARY)

    # Brass buttons - perfectly aligned
    for by in range(fig_y-20, fig_y+30, 12):
        draw.ellipse([fig_x-3, by-3, fig_x+3, by+3],
                    fill=WhistlesColors.ACCENT)

    # Cap/hat - authority symbol
    draw.rectangle([fig_x-22, fig_y-80, fig_x+22, fig_y-70],
                  fill=WhistlesColors.PRIMARY)
    draw.rectangle([fig_x-18, fig_y-85, fig_x+18, fig_y-80],
                  fill=WhistlesColors.ACCENT)

    # THE WHISTLE - at the ready
    whistle_y = fig_y + 60
    draw_whistle(draw, fig_x, whistle_y, 25, WhistlesColors.ACCENT)

    # Chain/lanyard
    draw.line([(fig_x, fig_y+40), (fig_x, whistle_y-15)],
             fill=(150, 150, 150), width=3)

    # Geometric rays of command emanating
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = fig_x + int(90 * math.cos(rad))
        y1 = fig_y + int(90 * math.sin(rad))
        x2 = fig_x + int(120 * math.cos(rad))
        y2 = fig_y + int(120 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)],
                 fill=WhistlesColors.ACCENT, width=4)

    # Perfect border - the frame of discipline
    draw.rectangle([5, 5, CARD_WIDTH-5, CARD_HEIGHT-5],
                  outline=WhistlesColors.SECONDARY, width=8)
    draw.rectangle([15, 15, CARD_WIDTH-15, CARD_HEIGHT-15],
                  outline=WhistlesColors.ACCENT, width=3)

    return img


# Generate Whistles cards!
if __name__ == '__main__':
    print("📯 ORDER AND DISCIPLINE! Creating Whistles suit! 📯\n")

    cards_to_generate = [
        ("whistles-00", draw_ace_of_whistles),
        ("whistles-03", draw_four_of_whistles),
        ("whistles-06", draw_seven_of_whistles),
        ("whistles-09", draw_ten_of_whistles),
        ("whistles-13", draw_officer_of_whistles),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} Whistles cards! ✨")
    print("⚖️ Structure can protect or oppress - the dialectic made visible... ⚖️")
