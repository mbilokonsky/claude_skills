#!/usr/bin/env python3
"""
Generate Major Arcana cards
The cinematic journey through The Sound of Music's 19 songs

Technicolor magic - colors shift from natural outdoor to golden indoor to dramatic twilight
Each card is a musical moment, a turning point in the story
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

def draw_00_preludium():
    """0 - Preludium: Aerial majesty, the world before story begins"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Dawn sky - before everything
    draw_gradient_sky(draw, 0, CARD_HEIGHT,
                     (255, 250, 240), (135, 206, 250))

    # MOUNTAIN PANORAMA - vast, untouched
    peaks = [
        (50, CARD_HEIGHT//3, 80, 100),
        (130, CARD_HEIGHT//3 - 20, 100, 130),
        (CARD_WIDTH//2, CARD_HEIGHT//3 - 40, 120, 160),
        (CARD_WIDTH-130, CARD_HEIGHT//3 - 20, 100, 130),
        (CARD_WIDTH-50, CARD_HEIGHT//3, 80, 100),
    ]

    for px, py, pw, ph in peaks:
        draw_mountain_peak(draw, px, py, pw, ph,
                          MountainsColors.PRIMARY, snow=True)

    # Morning mist layers
    for y in range(CARD_HEIGHT//2, CARD_HEIGHT, 40):
        opacity = 255 - ((y - CARD_HEIGHT//2) * 2)
        draw.rectangle([0, y, CARD_WIDTH, y+30],
                      fill=(220, 220, 240))

    # NO HUMAN PRESENCE - pure landscape
    # The world waiting

    return img


def draw_01_sound_of_music():
    """I - The Sound of Music: Maria alone, spinning, hills alive"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # GLORIOUS meadow sky
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     SongsColors.HIGHLIGHT, SongsColors.PRIMARY)

    # Meadow - vibrant, alive
    draw.rectangle([0, CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT],
                  fill=SongsColors.GROUND)

    # Wildflowers EVERYWHERE
    for i in range(40):
        fx = random.randint(10, CARD_WIDTH-10)
        fy = random.randint(CARD_HEIGHT//2, CARD_HEIGHT-20)
        color = random.choice([SongsColors.ACCENT_1, SongsColors.ACCENT_2, SongsColors.ACCENT_3])
        draw.ellipse([fx-3, fy-3, fx+3, fy+3], fill=color)

    # MARIA - center, SPINNING
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # Motion blur effect - she's TWIRLING
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        blur_x = fig_x + int(40 * math.cos(rad))
        blur_y = fig_y + int(20 * math.sin(rad))

        # Dress fragment
        draw.ellipse([blur_x-5, blur_y-5, blur_x+5, blur_y+5],
                    fill=(100, 100, 120))

    # Maria herself - arms OUT, face UP
    # Head
    draw.ellipse([fig_x-15, fig_y-50, fig_x+15, fig_y-20],
                fill=(220, 200, 180))

    # Dress - dark postulant dress
    draw.polygon([
        (fig_x, fig_y-20),
        (fig_x-40, fig_y+40),
        (fig_x+40, fig_y+40)
    ], fill=(60, 60, 80))

    # Arms spread WIDE - joy incarnate
    draw.line([(fig_x-40, fig_y-10), (fig_x-80, fig_y-30)],
             fill=(220, 200, 180), width=10)
    draw.line([(fig_x+40, fig_y-10), (fig_x+80, fig_y-30)],
             fill=(220, 200, 180), width=10)

    # Musical notes floating around her
    for i in range(12):
        angle = i * 30
        rad = math.radians(angle)
        nx = fig_x + int(70 * math.cos(rad))
        ny = fig_y + int(70 * math.sin(rad))
        draw_musical_note(draw, nx, ny, 8, (255, 215, 0))

    # Guitar case on ground - she left it behind
    draw.rectangle([30, CARD_HEIGHT-60, 60, CARD_HEIGHT-30],
                  fill=(80, 60, 40))

    return img


def draw_06_do_re_mi():
    """VI - Do-Re-Mi: Teaching the children, music as connection"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Golden afternoon - warmth, joy
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     (255, 240, 200), (255, 218, 185))

    # City/garden background
    draw.rectangle([0, CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT],
                  fill=(120, 140, 100))

    # SEVEN CHILDREN in a line - learning
    start_x = 30
    spacing = 35

    for i in range(7):
        cx = start_x + i * spacing
        cy = CARD_HEIGHT - 120 + (i % 2) * 15  # Playful height variation

        # Each child
        # Head
        draw.ellipse([cx-8, cy-25, cx+8, cy-10],
                    fill=(200, 180, 160))

        # Simple clothes - different colors
        colors = [(180, 140, 160), (140, 160, 180), (160, 180, 140),
                 (180, 160, 140), (160, 140, 180), (140, 180, 160), (180, 180, 140)]
        draw.rectangle([cx-10, cy-10, cx+10, cy+20],
                      fill=colors[i])

        # Mouths OPEN - singing
        draw.ellipse([cx-3, cy-15, cx+3, cy-12],
                    fill=(100, 50, 50))

    # MARIA at the end - conducting
    maria_x = CARD_WIDTH - 50
    maria_y = CARD_HEIGHT - 140

    # Her head
    draw.ellipse([maria_x-12, maria_y-35, maria_x+12, maria_y-15],
                fill=(220, 200, 180))

    # Dress - lighter now, summer
    draw.polygon([
        (maria_x, maria_y-15),
        (maria_x-20, maria_y+30),
        (maria_x+20, maria_y+30)
    ], fill=(200, 220, 240))

    # Arm raised - teaching
    draw.line([(maria_x, maria_y-10), (maria_x+30, maria_y-40)],
             fill=(220, 200, 180), width=8)

    # NOTES forming DO RE MI above them
    note_y = CARD_HEIGHT // 3
    note_positions = [40, 80, 120, 160, 200, 240, 280, 320]
    for i, nx in enumerate(note_positions[:7]):
        draw_musical_note(draw, nx, note_y - i*8, 10,
                         (255, 215, 0) if i < 7 else (200, 180, 100))

    # Connection lines - they're linked by music
    for i in range(6):
        cx1 = start_x + i * spacing
        cx2 = start_x + (i+1) * spacing
        draw.line([(cx1, CARD_HEIGHT-100), (cx2, CARD_HEIGHT-100)],
                 fill=(255, 215, 0), width=2)

    return img


def draw_08_edelweiss():
    """VIII - Edelweiss: Georg's love for his country, transmission of heritage"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Warm indoor glow - evening parlor
    for y in range(CARD_HEIGHT):
        t = y / CARD_HEIGHT
        r = int(222 * (1-t) + 139 * t)
        g = int(184 * (1-t) + 69 * t)
        b = int(135 * (1-t) + 19 * t)
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

    # GEORG with guitar - center, intimate
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Golden light around him - love, vulnerability
    for r in range(100, 0, -3):
        gold = 180 + r//2
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    fill=(gold, gold-20, 0), outline=(gold, gold-20, 0))

    # Head - softened, open
    draw.ellipse([fig_x-18, fig_y-60, fig_x+18, fig_y-30],
                fill=(180, 160, 140))

    # Naval uniform - but unbuttoned, relaxed
    draw.rectangle([fig_x-28, fig_y-30, fig_x+28, fig_y+40],
                  fill=WhistlesColors.PRIMARY)

    # Guitar across body
    # Body of guitar
    draw.ellipse([fig_x-20, fig_y, fig_x+20, fig_y+50],
                fill=(120, 80, 40))
    # Neck
    draw.rectangle([fig_x-5, fig_y-40, fig_x+5, fig_y],
                  fill=(100, 70, 30))

    # Hands on guitar - gentle
    draw.ellipse([fig_x-25, fig_y+15, fig_x-15, fig_y+25],
                fill=(180, 160, 140))
    draw.ellipse([fig_x+15, fig_y-20, fig_x+25, fig_y-10],
                fill=(180, 160, 140))

    # CHILDREN gathered around - listening, learning
    for i, (cx, cy) in enumerate([(60, CARD_HEIGHT-80), (100, CARD_HEIGHT-70),
                                   (CARD_WIDTH-100, CARD_HEIGHT-70), (CARD_WIDTH-60, CARD_HEIGHT-80)]):
        # Small heads visible
        draw.ellipse([cx-6, cy-15, cx+6, cy-5],
                    fill=(200, 180, 160))

    # EDELWEISS flowers floating - memory, love of Austria
    for i in range(10):
        ex = random.randint(40, CARD_WIDTH-40)
        ey = random.randint(40, 140)
        draw_edelweiss(draw, ex, ey, 15, color=(255, 255, 240))

    # Musical notes - the song
    for nx in [80, 120, 200, 240]:
        ny = 80 + random.randint(-20, 20)
        draw_musical_note(draw, nx, ny, 8, (255, 250, 200))

    return img


def draw_10_climb_every_mountain():
    """X - Climb Ev'ry Mountain: Mother Abbess's command, quest given"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Abbey interior - stone, sacred
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(80, 80, 90))

    # LIGHT from above - divine, commanding
    for y in range(0, CARD_HEIGHT//2):
        brightness = 255 - (y * 2)
        draw.line([(CARD_WIDTH//4, y), (3*CARD_WIDTH//4, y)],
                 fill=(brightness, brightness, brightness+20))

    # MOTHER ABBESS - towering, powerful
    abbess_x, abbess_y = CARD_WIDTH // 2, CARD_HEIGHT // 3

    # Authority aura
    for r in range(120, 0, -3):
        draw.ellipse([abbess_x-r, abbess_y-r, abbess_x+r, abbess_y+r],
                    fill=(100, 100, 120), outline=(100, 100, 120))

    # Her head - strong, knowing
    draw.ellipse([abbess_x-22, abbess_y-60, abbess_x+22, abbess_y-25],
                fill=(200, 190, 180))

    # Habit - black and white, absolute
    draw.rectangle([abbess_x-35, abbess_y-25, abbess_x+35, abbess_y+50],
                  fill=(20, 20, 20))
    # White wimple
    draw.polygon([
        (abbess_x-25, abbess_y-65),
        (abbess_x, abbess_y-75),
        (abbess_x+25, abbess_y-65),
        (abbess_x+25, abbess_y-25),
        (abbess_x-25, abbess_y-25)
    ], fill=(255, 255, 255))

    # Hand raised - COMMANDING, blessing
    draw.line([(abbess_x+35, abbess_y-10), (abbess_x+70, abbess_y-50)],
             fill=(200, 190, 180), width=12)

    # MARIA below - small, receiving
    maria_x = CARD_WIDTH // 2
    maria_y = CARD_HEIGHT - 120

    draw.ellipse([maria_x-10, maria_y-30, maria_x+10, maria_y-10],
                fill=(220, 200, 180))
    draw.polygon([
        (maria_x, maria_y-10),
        (maria_x-15, maria_y+20),
        (maria_x+15, maria_y+20)
    ], fill=(40, 40, 60))

    # MOUNTAINS in the distance/vision - the quest
    vision_y = CARD_HEIGHT * 2 // 3
    for mx in [60, 120, 180, 240]:
        draw_mountain_peak(draw, mx, vision_y, 40, 50,
                          (150, 150, 170), snow=True)

    # Words made visible - "CLIMB"
    for i, letter_x in enumerate([50, 90, 130, 170, 210]):
        draw.rectangle([letter_x, abbess_y+60, letter_x+20, abbess_y+80],
                      outline=(255, 250, 240), width=3)

    # Path from Maria to mountains - the way forward
    draw.line([(maria_x, maria_y+20), (CARD_WIDTH//2, vision_y)],
             fill=(200, 200, 220), width=4)

    return img


def draw_16_edelweiss_reprise():
    """XVI - Edelweiss Reprise: Defiance at concert, last stand"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # CONCERT HALL - dramatic, dangerous
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(20, 20, 40))

    # SPOTLIGHT - harsh, exposing
    for y in range(CARD_HEIGHT):
        for x in range(CARD_WIDTH):
            dist = math.sqrt((x - CARD_WIDTH//2)**2 + (y - CARD_HEIGHT//2)**2)
            brightness = max(0, int(200 - dist))
            draw.point((x, y), fill=(brightness, brightness, brightness+20))

    # GEORG - center stage, defiant
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Head - determined, emotional
    draw.ellipse([fig_x-18, fig_y-60, fig_x+18, fig_y-30],
                fill=(180, 160, 140))

    # Full dress uniform - but this is rebellion
    draw.rectangle([fig_x-28, fig_y-30, fig_x+28, fig_y+50],
                  fill=WhistlesColors.PRIMARY)
    # Medals - his authority, his right to resist
    for my in [fig_y-20, fig_y-5, fig_y+10]:
        draw.ellipse([fig_x-20, my-4, fig_x-12, my+4],
                    fill=(218, 165, 32))

    # Guitar - weapon of memory
    draw.ellipse([fig_x-22, fig_y+30, fig_x+22, fig_y+70],
                fill=(120, 80, 40))
    draw.rectangle([fig_x-5, fig_y-20, fig_x+5, fig_y+30],
                  fill=(100, 70, 30))

    # FAMILY behind - unified
    for i, (fx, fy) in enumerate([(fig_x-60, fig_y+30), (fig_x-40, fig_y+40),
                                   (fig_x+40, fig_y+40), (fig_x+60, fig_y+30)]):
        # Silhouettes
        draw.ellipse([fx-8, fy-20, fx+8, fy-10],
                    fill=(100, 100, 120))

    # EDELWEISS - huge, glowing, defiant
    edelweiss_x = CARD_WIDTH // 2
    edelweiss_y = 80
    draw_edelweiss(draw, edelweiss_x, edelweiss_y, 35,
                  color=(255, 255, 255))

    # Austrian flag colors hidden in borders
    draw.rectangle([0, 0, CARD_WIDTH, 10],
                  fill=(255, 0, 0))  # Red
    draw.rectangle([0, CARD_HEIGHT-10, CARD_WIDTH, CARD_HEIGHT],
                  fill=(255, 0, 0))  # Red

    # Nazi flags in shadows - the threat
    for fx in [20, CARD_WIDTH-20]:
        draw.rectangle([fx-10, 40, fx+10, 100],
                      fill=(200, 0, 0))
        # Swastika implied by black square
        draw.rectangle([fx-6, 60, fx+6, 80],
                      fill=(0, 0, 0))

    # Musical notes - but these ones are POWERFUL, resistant
    for i in range(8):
        angle = i * 45
        rad = math.radians(angle)
        nx = fig_x + int(90 * math.cos(rad))
        ny = fig_y + int(90 * math.sin(rad))
        draw_musical_note(draw, nx, ny, 10, (255, 255, 255))

    return img


def draw_18_climb_reprise():
    """XVIII - Climb Ev'ry Mountain Finale: Escape over mountains, freedom"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Twilight sky - danger, but also hope
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     (72, 61, 139), (135, 206, 250))

    # MASSIVE mountain range - the escape route
    for i, (mx, mw, mh) in enumerate([
        (60, 80, 140),
        (140, 100, 180),
        (CARD_WIDTH//2, 120, 220),
        (CARD_WIDTH-140, 100, 180),
        (CARD_WIDTH-60, 80, 140)
    ]):
        draw_mountain_peak(draw, mx, CARD_HEIGHT//3, mw, mh,
                          MountainsColors.SHADOW, snow=True)

    # FAMILY climbing - small figures on mountainside
    path_points = [
        (CARD_WIDTH//2, CARD_HEIGHT-60),
        (CARD_WIDTH//2 + 30, CARD_HEIGHT-100),
        (CARD_WIDTH//2 + 50, CARD_HEIGHT-140),
        (CARD_WIDTH//2 + 60, CARD_HEIGHT-180),
        (CARD_WIDTH//2 + 50, CARD_HEIGHT-220),
    ]

    # The PATH they're climbing
    for i in range(len(path_points)-1):
        draw.line([path_points[i], path_points[i+1]],
                 fill=(200, 200, 220), width=4)

    # Each family member on the path
    for i, (px, py) in enumerate(path_points[:9]):  # 9 family members
        # Tiny figures
        draw.ellipse([px-6, py-15, px+6, py-5],
                    fill=(200, 180, 160))
        draw.rectangle([px-7, py-5, px+7, py+8],
                      fill=(80, 80, 100))

    # LIGHT breaking over the mountains - freedom ahead
    for i in range(10):
        angle = -90 + (i * 20)
        rad = math.radians(angle)
        ray_length = 150
        draw.line([
            (CARD_WIDTH//2, 60),
            (CARD_WIDTH//2 + int(ray_length * math.cos(rad)),
             60 + int(ray_length * math.sin(rad)))
        ], fill=(255, 250, 200), width=3)

    # Edelweiss at the peak - they carry Austria with them
    draw_edelweiss(draw, CARD_WIDTH//2, 60, 20, color=(255, 255, 255))

    # Dark shadows below - what they're leaving
    draw.rectangle([0, CARD_HEIGHT-40, CARD_WIDTH, CARD_HEIGHT],
                  fill=(20, 20, 40))

    # But above: stars emerging - hope
    for i in range(15):
        sx = random.randint(20, CARD_WIDTH-20)
        sy = random.randint(20, CARD_HEIGHT//3)
        draw.line([(sx-2, sy), (sx+2, sy)], fill=(255, 255, 255), width=2)
        draw.line([(sx, sy-2), (sx, sy+2)], fill=(255, 255, 255), width=2)

    return img


# Generate Major Arcana cards!
if __name__ == '__main__':
    print("🎬 TECHNICOLOR JOURNEY! Creating Major Arcana! 🎬\n")

    cards_to_generate = [
        ("major-00", draw_00_preludium),
        ("major-01", draw_01_sound_of_music),
        ("major-06", draw_06_do_re_mi),
        ("major-08", draw_08_edelweiss),
        ("major-10", draw_10_climb_every_mountain),
        ("major-16", draw_16_edelweiss_reprise),
        ("major-18", draw_18_climb_reprise),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} Major Arcana cards! ✨")
    print("🎵 From mountain to love to defiance to freedom... 🎵")
