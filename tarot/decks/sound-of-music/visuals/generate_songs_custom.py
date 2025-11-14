#!/usr/bin/env python3
"""
Generate the Songs suit cards
Authentic/Creative - the suit of spontaneous expression and joy

Each card is a small artwork interpreting the meaning through
alpine meadow aesthetics - watercolor-inspired, flowing, alive
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

# Let's make these cards SING!

def draw_ace_of_songs():
    """
    Ace of Songs: The first song entering your life

    THE MOMENT - a single note emerges from silence, birds gather,
    the hills wake up. Everything is NEW and POSSIBLE.
    """
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Dawn sky - the beginning of everything
    for y in range(CARD_HEIGHT):
        t = y / CARD_HEIGHT
        # Sunrise gradient: deep blue to golden yellow
        r = int(135 + (255 - 135) * t * t)  # Accelerating toward warmth
        g = int(206 + (250 - 206) * t * t)
        b = int(250 - 150 * t)  # Fading blue
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

    # A single hill, fresh and green
    hill_points = [
        (0, CARD_HEIGHT * 2//3),
        (CARD_WIDTH//2, CARD_HEIGHT * 2//5),
        (CARD_WIDTH, CARD_HEIGHT * 2//3),
        (CARD_WIDTH, CARD_HEIGHT),
        (0, CARD_HEIGHT)
    ]
    draw.polygon(hill_points, fill=SongsColors.SECONDARY)

    # THE MOMENT: mouth opening, about to sing
    # A simple figure, arms beginning to spread
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Head - simple circle, face lifted to sky
    draw.ellipse([fig_x-15, fig_y-60, fig_x+15, fig_y-30],
                 fill=(255, 220, 200))

    # Body - simple dress shape
    dress_points = [
        (fig_x, fig_y-30),
        (fig_x-25, fig_y+40),
        (fig_x+25, fig_y+40)
    ]
    draw.polygon(dress_points, fill=(100, 180, 220))

    # Arms just beginning to spread - the gesture of opening
    draw.line([(fig_x-25, fig_y-10), (fig_x-45, fig_y+10)],
             fill=(255, 220, 200), width=6)
    draw.line([(fig_x+25, fig_y-10), (fig_x+45, fig_y+10)],
             fill=(255, 220, 200), width=6)

    # THE FIRST NOTE - glowing, just emerged
    note_x, note_y = fig_x + 30, fig_y - 50

    # Glow around the note
    for r in range(20, 0, -2):
        alpha = 255 - r * 10
        glow_color = (255, 255, 200)
        draw.ellipse([note_x-r, note_y-r, note_x+r, note_y+r],
                    fill=glow_color, outline=glow_color)

    # The note itself
    draw_musical_note(draw, note_x, note_y, 12, (255, 200, 0))

    # Birds gathering - drawn to the first sound
    # Small V shapes, scattered but moving toward the note
    bird_positions = [
        (fig_x - 60, fig_y - 80),
        (fig_x - 40, fig_y - 90),
        (fig_x + 50, fig_y - 70),
        (fig_x + 70, fig_y - 85),
    ]

    for bx, by in bird_positions:
        # Simple V for bird
        draw.line([(bx-5, by), (bx, by+5), (bx+5, by)],
                 fill=(60, 60, 60), width=2)

    # A few wildflowers just beginning to bloom at the figure's feet
    for i in range(8):
        fx = fig_x + random.randint(-30, 30)
        fy = fig_y + 40 + random.randint(0, 20)
        flower_color = random.choice([SongsColors.ACCENT_1,
                                     SongsColors.ACCENT_2,
                                     SongsColors.ACCENT_3])
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=flower_color)

    return img


def draw_two_of_songs():
    """
    Two of Songs: Harmonizing voices

    TWO FIGURES on adjacent hills, singing toward each other.
    Their voices (visible as flowing color) meet in the middle,
    weaving together or tangling based on the reading.
    """
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Bright midday sky
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     SongsColors.HIGHLIGHT, SongsColors.PRIMARY)

    # Two gentle hills
    # Left hill
    left_hill = [
        (0, CARD_HEIGHT*3//5),
        (CARD_WIDTH*2//5, CARD_HEIGHT//3),
        (CARD_WIDTH*2//5 + 20, CARD_HEIGHT),
        (0, CARD_HEIGHT)
    ]
    draw.polygon(left_hill, fill=(120, 200, 120))

    # Right hill
    right_hill = [
        (CARD_WIDTH*3//5 - 20, CARD_HEIGHT),
        (CARD_WIDTH*3//5, CARD_HEIGHT//3),
        (CARD_WIDTH, CARD_HEIGHT*3//5),
        (CARD_WIDTH, CARD_HEIGHT)
    ]
    draw.polygon(right_hill, fill=(140, 220, 140))

    # Valley between - deeper green
    draw.polygon([
        (CARD_WIDTH*2//5, CARD_HEIGHT//3),
        (CARD_WIDTH*3//5, CARD_HEIGHT//3),
        (CARD_WIDTH*3//5 - 20, CARD_HEIGHT),
        (CARD_WIDTH*2//5 + 20, CARD_HEIGHT)
    ], fill=(80, 160, 80))

    # Left figure - singing toward the right
    left_x, left_y = CARD_WIDTH // 4, CARD_HEIGHT * 2//5
    draw.ellipse([left_x-12, left_y-50, left_x+12, left_y-25],
                fill=(255, 210, 190))
    draw.polygon([
        (left_x, left_y-25),
        (left_x-20, left_y+30),
        (left_x+20, left_y+30)
    ], fill=(200, 100, 150))

    # Right figure - singing toward the left
    right_x, right_y = CARD_WIDTH * 3 // 4, CARD_HEIGHT * 2//5
    draw.ellipse([right_x-12, right_y-50, right_x+12, right_y-25],
                fill=(255, 210, 190))
    draw.polygon([
        (right_x, right_y-25),
        (right_x-20, right_y+30),
        (right_x+20, right_y+30)
    ], fill=(150, 100, 200))

    # VOICES MEETING - flowing ribbons of sound
    # Create bezier-like curves between the singers

    # Voice from left (warm pink/orange)
    for t in range(0, 100, 2):
        progress = t / 100.0
        # Curved path from left singer to center
        x = int(left_x + (CARD_WIDTH//2 - left_x) * progress)
        y = int(left_y - 30 - 20 * math.sin(progress * math.pi))

        # Draw flowing ribbon
        size = int(8 * (1 - progress * 0.5))
        color_r = int(255 * (1 - progress * 0.3))
        color_g = int(180 + 50 * progress)
        draw.ellipse([x-size, y-size, x+size, y+size],
                    fill=(color_r, color_g, 150))

    # Voice from right (cool blue/purple)
    for t in range(0, 100, 2):
        progress = t / 100.0
        x = int(right_x - (right_x - CARD_WIDTH//2) * progress)
        y = int(right_y - 30 - 20 * math.sin(progress * math.pi))

        size = int(8 * (1 - progress * 0.5))
        color_b = int(255 * (1 - progress * 0.3))
        color_g = int(150 + 70 * progress)
        draw.ellipse([x-size, y-size, x+size, y+size],
                    fill=(150, color_g, color_b))

    # Where they meet - either harmonious blend or tangled mess
    center_x, center_y = CARD_WIDTH // 2, left_y - 40

    # Harmonious: spiral blend
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        radius = 15
        px = center_x + int(radius * math.cos(rad))
        py = center_y + int(radius * math.sin(rad))

        # Blend the two voice colors
        blend_color = (200, 200, 200)
        draw.ellipse([px-5, py-5, px+5, py+5], fill=blend_color)

    # Scatter wildflowers on both hills
    for hill_x in [CARD_WIDTH // 4, CARD_WIDTH * 3 // 4]:
        for i in range(12):
            fx = hill_x + random.randint(-40, 40)
            fy = CARD_HEIGHT * 2//5 + random.randint(20, 80)
            flower_color = random.choice([SongsColors.ACCENT_1,
                                         SongsColors.ACCENT_2,
                                         SongsColors.ACCENT_3])
            draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=flower_color)

    return img


def draw_seven_of_songs():
    """
    Seven of Songs: The choice to sing or stay silent

    A figure at a CROSSROADS in the meadow. One path leads to
    a hilltop bathed in light, notes floating in air. The other
    path leads into shadow. The mouth is closed, breath held.
    The choice is YOURS.
    """
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Split sky - one side bright, one side dimming
    for y in range(CARD_HEIGHT // 2):
        for x in range(CARD_WIDTH):
            # Left side: bright and musical
            # Right side: darker, quieter
            t_x = x / CARD_WIDTH
            t_y = y / (CARD_HEIGHT // 2)

            if x < CARD_WIDTH // 2:
                # Bright side
                r = int(135 + 120 * (1 - t_y))
                g = int(206 + 49 * (1 - t_y))
                b = int(250)
            else:
                # Dim side
                r = int(135 - 50 * t_x)
                g = int(206 - 80 * t_x)
                b = int(250 - 100 * t_x)

            draw.point((x, y), fill=(r, g, b))

    # Meadow with diverging paths
    draw.rectangle([0, CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT],
                  fill=(100, 160, 100))

    # Left path - leads upward to light and song
    left_path = [
        (CARD_WIDTH//2, CARD_HEIGHT * 3//4),
        (CARD_WIDTH//4, CARD_HEIGHT * 2//5),
        (CARD_WIDTH//4 - 30, CARD_HEIGHT * 2//5),
        (CARD_WIDTH//2 - 15, CARD_HEIGHT * 3//4)
    ]
    draw.polygon(left_path, fill=(180, 200, 120))

    # Right path - leads into shadow/silence
    right_path = [
        (CARD_WIDTH//2, CARD_HEIGHT * 3//4),
        (CARD_WIDTH * 3//4, CARD_HEIGHT * 3//5),
        (CARD_WIDTH * 3//4 + 30, CARD_HEIGHT * 3//5),
        (CARD_WIDTH//2 + 15, CARD_HEIGHT * 3//4)
    ]
    draw.polygon(right_path, fill=(80, 100, 80))

    # Figure at the crossroads - FROZEN in the moment of choice
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 3//4

    # Head
    draw.ellipse([fig_x-14, fig_y-55, fig_x+14, fig_y-27],
                fill=(255, 220, 200))

    # Face showing tension - eyes looking both ways
    # Left eye looking left
    draw.ellipse([fig_x-8, fig_y-45, fig_x-3, fig_y-40], fill=(50, 50, 50))
    # Right eye looking right
    draw.ellipse([fig_x+3, fig_y-45, fig_x+8, fig_y-40], fill=(50, 50, 50))

    # Mouth closed - the held breath
    draw.line([(fig_x-6, fig_y-33), (fig_x+6, fig_y-33)],
             fill=(180, 100, 100), width=2)

    # Body
    draw.polygon([
        (fig_x, fig_y-27),
        (fig_x-22, fig_y+25),
        (fig_x+22, fig_y+25)
    ], fill=(120, 160, 180))

    # Arms - one reaching toward each path, equally
    draw.line([(fig_x-22, fig_y), (fig_x-50, fig_y-10)],
             fill=(255, 220, 200), width=6)
    draw.line([(fig_x+22, fig_y), (fig_x+50, fig_y-10)],
             fill=(255, 220, 200), width=6)

    # Left path destination: hill with floating notes and light
    hill_top_y = CARD_HEIGHT * 2//5 - 40
    # Glow
    for r in range(40, 0, -4):
        alpha_color = (255, 255, int(200 - r * 2))
        draw.ellipse([CARD_WIDTH//4 - r, hill_top_y - r,
                     CARD_WIDTH//4 + r, hill_top_y + r],
                    fill=alpha_color, outline=alpha_color)

    # Musical notes floating free
    note_positions = [
        (CARD_WIDTH//4 - 15, hill_top_y - 20),
        (CARD_WIDTH//4 + 10, hill_top_y - 15),
        (CARD_WIDTH//4, hill_top_y + 10)
    ]
    for nx, ny in note_positions:
        draw_musical_note(draw, nx, ny, 8, (255, 200, 50))

    # Right path destination: shadow and silence
    shadow_y = CARD_HEIGHT * 3//5
    draw.ellipse([CARD_WIDTH*3//4 - 30, shadow_y - 30,
                 CARD_WIDTH*3//4 + 30, shadow_y + 30],
                fill=(60, 70, 60))

    # A few stressed wildflowers at the crossroads
    for i in range(6):
        fx = fig_x + random.randint(-25, 25)
        fy = fig_y + 20 + random.randint(0, 15)
        draw.ellipse([fx-2, fy-2, fx+2, fy+2],
                    fill=SongsColors.ACCENT_2)

    return img


def draw_three_of_songs():
    """Three: Song spreading through a household - children learning, joy multiplying"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_songs_background(draw)

    # A house/room with windows - warm interior
    house_y = CARD_HEIGHT // 3
    draw.rectangle([60, house_y, CARD_WIDTH-60, CARD_HEIGHT-80],
                   fill=(220, 200, 160))

    # Windows showing singing happening inside
    for wx in [90, 150, 210]:
        draw.rectangle([wx, house_y+30, wx+30, house_y+60],
                      fill=(255, 240, 200))
        # Musical notes visible through window
        draw_musical_note(draw, wx+15, house_y+40, 6, (255, 180, 100))

    # Three figures visible - teaching spreading
    # Adult (larger) in center window
    draw.ellipse([145, house_y+35, 155, house_y+45], fill=(255, 200, 180))
    # Two children in other windows
    draw.ellipse([95, house_y+40, 103, house_y+48], fill=(255, 210, 190))
    draw.ellipse([215, house_y+40, 223, house_y+48], fill=(255, 210, 190))

    # Sound waves radiating out from house - song spreading
    for r in [40, 60, 80, 100]:
        draw.ellipse([CARD_WIDTH//2-r, CARD_HEIGHT//2-r,
                     CARD_WIDTH//2+r, CARD_HEIGHT//2+r],
                    outline=(255, 220, 100, 150), width=2)

    # Flowers blooming in response to the music
    for i in range(20):
        fx = random.randint(10, CARD_WIDTH-10)
        fy = random.randint(CARD_HEIGHT-60, CARD_HEIGHT-10)
        draw.ellipse([fx-3, fy-3, fx+3, fy+3],
                    fill=random.choice([SongsColors.ACCENT_1,
                                       SongsColors.ACCENT_2,
                                       SongsColors.ACCENT_3]))

    return img


def draw_ten_of_songs():
    """Ten: Full voice realized - the complete song, integration of self and sound"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Glorious sunset/sunrise sky - peak moment
    for y in range(CARD_HEIGHT):
        t = y / CARD_HEIGHT
        # Radial gradient from center outward
        r = int(255 * (1 - t*0.3))
        g = int(200 + 50 * math.sin(t * math.pi))
        b = int(150 + 100 * (1-t))
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

    # Figure on peak - COMPLETE, arms fully spread, in full voice
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 3

    # Radiant glow around entire figure
    for r in range(60, 0, -3):
        alpha_val = 255 - r * 3
        draw.ellipse([fig_x-r, fig_y-r-30, fig_x+r, fig_y+r+30],
                    fill=(255, 255, 200), outline=(255, 255, 200))

    # The figure - triumphant
    draw.ellipse([fig_x-18, fig_y-70, fig_x+18, fig_y-35],
                fill=(255, 220, 200))

    # Body
    draw.polygon([
        (fig_x, fig_y-35),
        (fig_x-30, fig_y+50),
        (fig_x+30, fig_y+50)
    ], fill=(150, 100, 200))

    # Arms WIDE - complete opening
    draw.line([(fig_x-30, fig_y-10), (fig_x-80, fig_y-30)],
             fill=(255, 220, 200), width=8)
    draw.line([(fig_x+30, fig_y-10), (fig_x+80, fig_y-30)],
             fill=(255, 220, 200), width=8)

    # Musical notes EVERYWHERE - filling the entire space
    for i in range(30):
        nx = random.randint(20, CARD_WIDTH-20)
        ny = random.randint(20, CARD_HEIGHT-20)
        size = random.randint(6, 12)
        draw_musical_note(draw, nx, ny, size,
                         (255, random.randint(200,255), random.randint(100,200)))

    # Birds in flight - celebrating
    for i in range(15):
        bx = random.randint(10, CARD_WIDTH-10)
        by = random.randint(10, CARD_HEIGHT//2)
        draw.line([(bx-5, by), (bx, by+5), (bx+5, by)],
                 fill=(100, 100, 100), width=2)

    # Meadow ALIVE with flowers
    draw.rectangle([0, CARD_HEIGHT*2//3, CARD_WIDTH, CARD_HEIGHT],
                  fill=(100, 200, 100))
    for i in range(50):
        fx = random.randint(0, CARD_WIDTH)
        fy = random.randint(CARD_HEIGHT*2//3, CARD_HEIGHT)
        draw.ellipse([fx-3, fy-3, fx+3, fy+3],
                    fill=random.choice([SongsColors.ACCENT_1,
                                       SongsColors.ACCENT_2,
                                       SongsColors.ACCENT_3]))

    return img


def draw_singer_of_songs():
    """Singer of Songs - pure authentic creative voice embodied"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # This is THE SINGER - Maria on the mountain
    # The most iconic, the most pure

    # Perfect alpine day - every color at peak
    draw_gradient_sky(draw, 0, CARD_HEIGHT*2//5,
                     (180, 220, 255), (135, 206, 250))

    # Rolling green hills
    for hill_y, hill_height, green_shade in [
        (CARD_HEIGHT*3//5, 60, (120, 200, 120)),
        (CARD_HEIGHT*2//5, 80, (100, 180, 100)),
        (CARD_HEIGHT//2, 100, (140, 220, 140))
    ]:
        draw.ellipse([0, hill_y-hill_height, CARD_WIDTH, hill_y+20],
                    fill=green_shade)

    # THE SINGER - center, elevated, BEING song itself
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 3

    # Aura of pure creative energy
    for r in range(80, 0, -4):
        glow_alpha = 255 - r * 2
        draw.ellipse([fig_x-r, fig_y-r-40, fig_x+r, fig_y+r+60],
                    fill=(255, 250, 200), outline=(255, 250, 200))

    # Head thrown back in song
    draw.ellipse([fig_x-20, fig_y-80, fig_x+20, fig_y-40],
                fill=(255, 220, 200))
    # Mouth OPEN, singing
    draw.ellipse([fig_x-8, fig_y-50, fig_x+8, fig_y-42],
                fill=(220, 100, 100))

    # Dress flowing
    draw.polygon([
        (fig_x, fig_y-40),
        (fig_x-40, fig_y+70),
        (fig_x+40, fig_y+70)
    ], fill=(100, 160, 200))

    # Arms in full expression - spinning
    angle1 = math.radians(-30)
    angle2 = math.radians(210)
    arm1_x = fig_x + int(70 * math.cos(angle1))
    arm1_y = fig_y + int(70 * math.sin(angle1))
    arm2_x = fig_x + int(70 * math.cos(angle2))
    arm2_y = fig_y + int(70 * math.sin(angle2))

    draw.line([(fig_x-30, fig_y-20), (arm1_x, arm1_y)],
             fill=(255, 220, 200), width=10)
    draw.line([(fig_x+30, fig_y-20), (arm2_x, arm2_y)],
             fill=(255, 220, 200), width=10)

    # Everything responding to the voice
    # Wind visible
    for i in range(10):
        wind_y = random.randint(50, 200)
        draw.line([(0, wind_y), (CARD_WIDTH, wind_y-20)],
                 fill=(200, 220, 255), width=2)

    # Musical notes streaming from the voice
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        for dist in [30, 50, 70]:
            nx = fig_x + int(dist * math.cos(rad))
            ny = fig_y - 60 + int(dist * math.sin(rad))
            draw_musical_note(draw, nx, ny, 8, (255, 200+random.randint(-50,50), 100))

    # Wildflowers spinning around her feet
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        fx = fig_x + int(50 * math.cos(rad))
        fy = fig_y + 70 + int(20 * math.sin(rad))
        draw.ellipse([fx-4, fy-4, fx+4, fy+4],
                    fill=random.choice([SongsColors.ACCENT_1,
                                       SongsColors.ACCENT_2,
                                       SongsColors.ACCENT_3]))

    return img


# Generate ALL Songs cards!
if __name__ == '__main__':
    print("🎵 THE HILLS ARE ALIVE! Creating the complete Songs suit! 🎵\n")

    cards_to_generate = [
        ("songs-00", draw_ace_of_songs),
        ("songs-01", draw_two_of_songs),
        ("songs-02", draw_three_of_songs),
        ("songs-06", draw_seven_of_songs),
        ("songs-09", draw_ten_of_songs),
        ("songs-10", draw_singer_of_songs),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} Songs cards! Each one sings! ✨")
    print("🌸 More cards coming - the joy is just beginning... 🌸")
