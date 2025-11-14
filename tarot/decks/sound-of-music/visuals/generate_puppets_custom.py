#!/usr/bin/env python3
"""
Generate Puppets suit cards
Instrumental/Creative - purposeful staging, craft, spectacle

Theatrical lighting, Art Deco drama - can delight or manipulate
Each card explores craft in service of teaching or control
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

def draw_ace_of_puppets():
    """Ace: Craft first entering - learning to make, to stage"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # A single PUPPET - the first one, the gift
    puppet_x, puppet_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # Spotlight from above
    for r in range(100, 0, -5):
        alpha = 255 - r * 2
        draw.ellipse([puppet_x-r, puppet_y-r*1.5, puppet_x+r, puppet_y+30],
                    fill=(100, 80, 40), outline=(100, 80, 40))

    # GOLDEN SPOTLIGHT at puppet's feet
    draw.ellipse([puppet_x-40, puppet_y+20, puppet_x+40, puppet_y+35],
                fill=PuppetsColors.HIGHLIGHT)

    # Simple marionette - charming, new
    # Head
    draw.ellipse([puppet_x-12, puppet_y-40, puppet_x+12, puppet_y-15],
                fill=(200, 160, 120))

    # Body - Tyrolean costume
    draw.polygon([
        (puppet_x, puppet_y-15),
        (puppet_x-15, puppet_y+15),
        (puppet_x+15, puppet_y+15)
    ], fill=(180, 60, 60))  # Red costume

    # Little legs
    draw.line([(puppet_x-5, puppet_y+15), (puppet_x-8, puppet_y+30)],
             fill=(80, 80, 80), width=3)
    draw.line([(puppet_x+5, puppet_y+15), (puppet_x+8, puppet_y+30)],
             fill=(80, 80, 80), width=3)

    # THE STRINGS - visible but not controlling yet
    control_y = 100
    draw_puppet_strings(draw, puppet_x, control_y, puppet_x, puppet_y-40,
                       PuppetsColors.STRING)

    # Control bar above - gleaming brass
    draw.rectangle([puppet_x-30, control_y-10, puppet_x+30, control_y+10],
                  fill=PuppetsColors.SECONDARY)

    # Hands offering the control bar - the GIFT of craft
    draw.ellipse([puppet_x-50, control_y-15, puppet_x-30, control_y+5],
                fill=(220, 200, 180))
    draw.ellipse([puppet_x+30, control_y-15, puppet_x+50, control_y+5],
                fill=(220, 200, 180))

    return img


def draw_seven_of_puppets():
    """Seven: Choice to perform or refuse - the strings extended"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Stage left: warm spotlight - performance space
    draw.rectangle([0, 0, CARD_WIDTH//2, CARD_HEIGHT],
                  fill=(20, 0, 0))

    # Stage right: darkness - the exit
    draw.rectangle([CARD_WIDTH//2, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(0, 0, 0))

    # Spotlight on left
    for x in range(0, CARD_WIDTH//2):
        for y in range(CARD_HEIGHT):
            dist_from_center = math.sqrt((x - CARD_WIDTH//4)**2 + (y - CARD_HEIGHT//2)**2)
            brightness = max(0, 100 - int(dist_from_center * 0.5))
            draw.point((x, y), fill=(brightness, brightness//2, 0))

    # Figure at CENTER - between stage and exit
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # The figure
    draw.ellipse([fig_x-15, fig_y-50, fig_x+15, fig_y-20],
                fill=(200, 180, 160))
    draw.polygon([
        (fig_x, fig_y-20),
        (fig_x-20, fig_y+30),
        (fig_x+20, fig_y+30)
    ], fill=(120, 100, 140))

    # CONTROL STRINGS extended from above - the OFFER
    control_y = 80
    # Control bar hovering, waiting
    draw.rectangle([fig_x-25, control_y-8, fig_x+25, control_y+8],
                  fill=PuppetsColors.SECONDARY)

    # Strings dangling down - not attached yet
    for sx in [fig_x-15, fig_x-5, fig_x+5, fig_x+15]:
        draw.line([(sx, control_y+8), (sx, fig_y-50)],
                 fill=PuppetsColors.STRING, width=2)
        # Small hook/attachment at bottom
        draw.ellipse([sx-3, fig_y-53, sx+3, fig_y-47],
                    fill=(255, 255, 255))

    # One hand reaching toward strings (tempted)
    draw.line([(fig_x-20, fig_y), (fig_x-35, fig_y-30)],
             fill=(200, 180, 160), width=6)

    # Other hand pointing toward exit
    draw.line([(fig_x+20, fig_y), (fig_x+50, fig_y+10)],
             fill=(200, 180, 160), width=6)

    # Stage left: small puppet theater - what performance offers
    theater_x = CARD_WIDTH // 6
    draw.rectangle([theater_x-30, CARD_HEIGHT-120, theater_x+30, CARD_HEIGHT-40],
                  outline=PuppetsColors.ACCENT, width=3)
    # Tiny audience silhouettes
    for i in range(5):
        ax = theater_x - 25 + i * 12
        draw.ellipse([ax-4, CARD_HEIGHT-60, ax+4, CARD_HEIGHT-50],
                    fill=(60, 40, 40))

    return img


def draw_ten_of_puppets():
    """Ten: Performance complete - the final bow, purpose served"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # GRAND FINALE lighting
    for y in range(CARD_HEIGHT):
        for x in range(40, CARD_WIDTH-40):
            # Spotlight gradient - dramatic
            dist = abs(x - CARD_WIDTH//2)
            brightness = max(0, 200 - int(dist * 2))
            draw.point((x, y), fill=(brightness//3, brightness//4, 0))

    # THE STAGE - performance complete
    stage_y = CARD_HEIGHT * 2 // 3

    # Red curtains pulled BACK for bow
    # Left curtain
    draw.polygon([
        (0, 0),
        (50, 100),
        (50, CARD_HEIGHT),
        (0, CARD_HEIGHT)
    ], fill=PuppetsColors.PRIMARY)

    # Right curtain
    draw.polygon([
        (CARD_WIDTH, 0),
        (CARD_WIDTH-50, 100),
        (CARD_WIDTH-50, CARD_HEIGHT),
        (CARD_WIDTH, CARD_HEIGHT)
    ], fill=PuppetsColors.PRIMARY)

    # PERFORMERS in line - taking final bow
    for i, px in enumerate([80, 130, 180, 230]):
        # Each figure bowing
        draw.ellipse([px-10, stage_y-30, px+10, stage_y-10],
                    fill=(200, 180, 160))

        # Body bent in bow
        bow_angle = math.radians(45)
        body_x = px + int(15 * math.cos(bow_angle))
        body_y = stage_y + int(15 * math.sin(bow_angle))

        draw.polygon([
            (px, stage_y-10),
            (body_x-12, body_y),
            (body_x+12, body_y)
        ], fill=(random.choice([(180, 60, 60), (60, 80, 180),
                               (180, 140, 60), (140, 60, 180)])))

        # Strings VISIBLE even in triumph - craft never hidden
        control_y = 50 + i * 10
        draw.line([(px, control_y), (px, stage_y-30)],
                 fill=PuppetsColors.STRING, width=1)

    # Golden stage floor
    draw.rectangle([60, stage_y+10, CARD_WIDTH-60, stage_y+25],
                  fill=PuppetsColors.SECONDARY)

    # APPLAUSE implied - audience silhouettes
    for i in range(15):
        ax = random.randint(70, CARD_WIDTH-70)
        ay = random.randint(CARD_HEIGHT-80, CARD_HEIGHT-30)
        # Hands raised
        draw.line([(ax-5, ay), (ax-5, ay-10)],
                 fill=(80, 60, 60), width=3)
        draw.line([(ax+5, ay), (ax+5, ay-10)],
                 fill=(80, 60, 60), width=3)

    return img


def draw_puppeteer_of_puppets():
    """Puppeteer of Puppets - the archetype, craft embodied"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # MAXIMUM theatrical drama
    # Center spotlight - intense
    center_x, center_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    for r in range(150, 0, -3):
        alpha = 255 - r
        draw.ellipse([center_x-r, center_y-r, center_x+r, center_y+r],
                    fill=(60, 40, 0), outline=(60, 40, 0))

    # THE PUPPETEER - commanding, creating
    puppeteer_y = CARD_HEIGHT // 4

    # Head
    draw.ellipse([center_x-18, puppeteer_y-60, center_x+18, puppeteer_y-25],
                fill=(180, 160, 140))

    # Eyes looking DOWN at creation
    draw.ellipse([center_x-10, puppeteer_y-45, center_x-5, puppeteer_y-40],
                fill=(50, 30, 30))
    draw.ellipse([center_x+5, puppeteer_y-45, center_x+10, puppeteer_y-40],
                fill=(50, 30, 30))

    # Body - dramatic costume
    draw.polygon([
        (center_x, puppeteer_y-25),
        (center_x-35, puppeteer_y+40),
        (center_x+35, puppeteer_y+40)
    ], fill=(100, 20, 20))

    # HANDS controlling - this is key
    # Left hand with control bar
    left_hand_x = center_x - 60
    left_hand_y = puppeteer_y

    draw.ellipse([left_hand_x-12, left_hand_y-12, left_hand_x+12, left_hand_y+12],
                fill=(180, 160, 140))

    # Control bar in left hand
    draw.rectangle([left_hand_x-25, left_hand_y-5, left_hand_x+25, left_hand_y+5],
                  fill=PuppetsColors.SECONDARY)

    # Strings from left bar to left puppet
    left_puppet_x = left_hand_x
    left_puppet_y = CARD_HEIGHT - 100
    draw_puppet_strings(draw, left_hand_x, left_hand_y+5,
                       left_puppet_x, left_puppet_y, PuppetsColors.STRING)

    # Right hand with control bar
    right_hand_x = center_x + 60
    right_hand_y = puppeteer_y

    draw.ellipse([right_hand_x-12, right_hand_y-12, right_hand_x+12, right_hand_y+12],
                fill=(180, 160, 140))

    # Control bar in right hand
    draw.rectangle([right_hand_x-25, right_hand_y-5, right_hand_x+25, right_hand_y+5],
                  fill=PuppetsColors.SECONDARY)

    # Strings from right bar to right puppet
    right_puppet_x = right_hand_x
    right_puppet_y = CARD_HEIGHT - 100
    draw_puppet_strings(draw, right_hand_x, right_hand_y+5,
                       right_puppet_x, right_puppet_y, PuppetsColors.STRING)

    # THE PUPPETS - dancing, performing
    for puppet_x in [left_puppet_x, right_puppet_x]:
        # Puppet head
        draw.ellipse([puppet_x-10, left_puppet_y-35, puppet_x+10, left_puppet_y-15],
                    fill=(200, 180, 150))

        # Puppet body
        draw.polygon([
            (puppet_x, left_puppet_y-15),
            (puppet_x-12, left_puppet_y+10),
            (puppet_x+12, left_puppet_y+10)
        ], fill=(180, 140, 60))

        # Little legs
        draw.line([(puppet_x-5, left_puppet_y+10), (puppet_x-7, left_puppet_y+25)],
                 fill=(100, 100, 100), width=3)
        draw.line([(puppet_x+5, left_puppet_y+10), (puppet_x+7, left_puppet_y+25)],
                 fill=(100, 100, 100), width=3)

    # More strings extending to MORE puppets in shadows
    for i in range(4):
        shadow_x = 80 + i * 40
        shadow_y = CARD_HEIGHT - 60

        # Faint strings from above
        draw.line([(center_x, puppeteer_y+40), (shadow_x, shadow_y)],
                 fill=(100, 100, 100), width=1)

        # Tiny puppet silhouette
        draw.ellipse([shadow_x-5, shadow_y-5, shadow_x+5, shadow_y+5],
                    fill=(60, 40, 40))

    # Golden theatrical border
    draw.rectangle([10, 10, CARD_WIDTH-10, CARD_HEIGHT-10],
                  outline=PuppetsColors.SECONDARY, width=5)

    return img


# Generate Puppets cards!
if __name__ == '__main__':
    print("🎭 THEATRICAL STAGING! Creating Puppets suit! 🎭\n")

    cards_to_generate = [
        ("puppets-00", draw_ace_of_puppets),
        ("puppets-06", draw_seven_of_puppets),
        ("puppets-09", draw_ten_of_puppets),
        ("puppets-12", draw_puppeteer_of_puppets),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} Puppets cards! ✨")
    print("🎪 The strings are visible - craft can enchant or control... 🎪")
