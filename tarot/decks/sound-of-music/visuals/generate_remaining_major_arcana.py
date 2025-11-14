#!/usr/bin/env python3
"""
Generate the remaining Major Arcana cards to complete the deck!
The final 12 songs of The Sound of Music's journey
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

def draw_02_maria():
    """II - Maria: The nuns singing - how do you solve a problem?"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Abbey interior - stone, echoing
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(80, 80, 90))

    # Light through windows
    for x in [70, 140, 210]:
        draw.rectangle([x-20, 40, x+20, 200],
                      fill=(200, 200, 220))

    # MANY NUNS in discussion - gesturing about Maria
    positions = [(50, 150), (100, 140), (150, 160), (200, 145),
                 (50, 230), (100, 240), (150, 225), (200, 235)]

    for nx, ny in positions:
        # Nun's habit
        draw.ellipse([nx-8, ny-22, nx+8, ny-12],
                    fill=(200, 190, 180))
        # Black habit
        draw.polygon([
            (nx, ny-12),
            (nx-12, ny+15),
            (nx+12, ny+15)
        ], fill=(20, 20, 20))
        # White wimple
        draw.polygon([
            (nx-10, ny-25),
            (nx, ny-28),
            (nx+10, ny-25),
            (nx+10, ny-12),
            (nx-10, ny-12)
        ], fill=(255, 255, 255))

        # Hands gesturing - confusion!
        if random.random() > 0.5:
            draw.line([(nx-12, ny), (nx-20, ny-10)],
                     fill=(200, 190, 180), width=4)

    # Musical notes of their song - questioning
    for i in range(8):
        nx = random.randint(40, CARD_WIDTH-40)
        ny = random.randint(50, 120)
        draw_musical_note(draw, nx, ny, 8, (180, 180, 200))

    # Question marks in the air
    for qx in [80, 160, 240]:
        draw.arc([qx-15, 280-15, qx+15, 280+15],
                start=45, end=315, fill=(150, 150, 170), width=5)
        draw.ellipse([qx-3, 295, qx+3, 301],
                    fill=(150, 150, 170))

    return img


def draw_03_i_have_confidence():
    """III - I Have Confidence: Maria's journey to the villa"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Path from mountain to city
    # Top: mountain (past)
    draw_gradient_sky(draw, 0, CARD_HEIGHT//3,
                     SongsColors.HIGHLIGHT, SongsColors.PRIMARY)

    # Middle: transitional
    draw.rectangle([0, CARD_HEIGHT//3, CARD_WIDTH, 2*CARD_HEIGHT//3],
                  fill=(120, 140, 120))

    # Bottom: approaching villa
    draw.rectangle([0, 2*CARD_HEIGHT//3, CARD_WIDTH, CARD_HEIGHT],
                  fill=(100, 100, 110))

    # MARIA walking forward - determined, nervous
    maria_x, maria_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Walking posture
    draw.ellipse([maria_x-15, maria_y-50, maria_x+15, maria_y-22],
                fill=(220, 200, 180))

    # Postulant dress
    draw.polygon([
        (maria_x, maria_y-22),
        (maria_x-25, maria_y+35),
        (maria_x+25, maria_y+35)
    ], fill=(60, 60, 80))

    # Legs mid-stride
    draw.line([(maria_x-8, maria_y+35), (maria_x-15, maria_y+60)],
             fill=(60, 60, 80), width=8)
    draw.line([(maria_x+8, maria_y+35), (maria_x+12, maria_y+60)],
             fill=(60, 60, 80), width=8)

    # GUITAR case swinging
    guitar_x = maria_x + 40
    guitar_y = maria_y + 20
    draw.rectangle([guitar_x-10, guitar_y-35, guitar_x+10, guitar_y+35],
                  fill=(80, 60, 40))

    # Musical notes - singing to bolster courage
    for i in range(6):
        angle = i * 60 + 120
        rad = math.radians(angle)
        nx = maria_x + int(50 * math.cos(rad))
        ny = maria_y + int(50 * math.sin(rad))
        draw_musical_note(draw, nx, ny, 9,
                         (random.choice([SongsColors.ACCENT_1, SongsColors.ACCENT_2])))

    # Path ahead - unknown
    for y in range(maria_y+65, CARD_HEIGHT, 15):
        draw.line([(CARD_WIDTH//2-30, y), (CARD_WIDTH//2+30, y+10)],
                 fill=(120, 120, 130), width=3)

    # Villa looming in distance
    draw.rectangle([CARD_WIDTH-100, CARD_HEIGHT-140, CARD_WIDTH-40, CARD_HEIGHT-80],
                  fill=(60, 60, 70))

    return img


def draw_04_sixteen_going_on_seventeen():
    """IV - Sixteen Going on Seventeen: Liesl and Rolf, young love"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Gazebo at twilight - romantic, but ominous undertones
    # Sky - twilight
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     (100, 80, 140), (180, 160, 200))

    # Gazebo structure
    gazebo_y = CARD_HEIGHT // 3

    # Pillars
    for px in [60, 130, 200, 270]:
        draw.rectangle([px-8, gazebo_y, px+8, CARD_HEIGHT-60],
                      fill=(220, 220, 230))

    # Roof
    draw.polygon([
        (30, gazebo_y),
        (CARD_WIDTH//2, gazebo_y-50),
        (CARD_WIDTH-30, gazebo_y)
    ], fill=(200, 200, 210))

    # LIESL and ROLF dancing
    liesl_x, rolf_x = CARD_WIDTH//2 - 25, CARD_WIDTH//2 + 25
    fig_y = CARD_HEIGHT * 2 // 3

    # Liesl - innocent, hopeful
    draw.ellipse([liesl_x-12, fig_y-40, liesl_x+12, fig_y-18],
                fill=(220, 200, 180))
    draw.polygon([
        (liesl_x, fig_y-18),
        (liesl_x-22, fig_y+30),
        (liesl_x+22, fig_y+30)
    ], fill=(200, 220, 240))  # Light dress

    # Rolf - young, uniformed (ominous)
    draw.ellipse([rolf_x-12, fig_y-40, rolf_x+12, fig_y-18],
                fill=(200, 180, 160))
    draw.rectangle([rolf_x-18, fig_y-18, rolf_x+18, fig_y+30],
                  fill=(100, 100, 120))  # Dark clothing

    # Hands reaching - touching
    draw.line([(liesl_x+22, fig_y), (rolf_x-18, fig_y)],
             fill=(220, 200, 180), width=6)

    # Musical notes - sweet melody
    for i in range(6):
        nx = random.randint(80, CARD_WIDTH-80)
        ny = random.randint(100, 200)
        draw_musical_note(draw, nx, ny, 8, (255, 200, 220))

    # But: rain starting - danger foreshadowed
    for i in range(15):
        rx = random.randint(0, CARD_WIDTH)
        ry = random.randint(0, CARD_HEIGHT//2)
        draw.line([(rx, ry), (rx+3, ry+10)],
                 fill=(150, 150, 170), width=1)

    return img


def draw_05_my_favorite_things():
    """V - My Favorite Things: Comfort in the storm"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Dark bedroom - thunderstorm outside
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(30, 30, 50))

    # Lightning flash through window
    window_x = 200
    draw.rectangle([window_x-30, 40, window_x+30, 160],
                  fill=(200, 200, 220))

    # Lightning
    draw.line([(window_x, 40), (window_x-15, 90)],
             fill=(255, 255, 200), width=6)
    draw.line([(window_x-15, 90), (window_x+10, 140)],
             fill=(255, 255, 200), width=6)

    # MARIA and CHILDREN huddled together
    maria_x = CARD_WIDTH // 2
    maria_y = CARD_HEIGHT * 2 // 3

    # Maria - comforting
    draw.ellipse([maria_x-15, maria_y-50, maria_x+15, maria_y-25],
                fill=(220, 200, 180))
    draw.polygon([
        (maria_x, maria_y-25),
        (maria_x-30, maria_y+25),
        (maria_x+30, maria_y+25)
    ], fill=(180, 200, 220))

    # Arms OUT - gathering children
    draw.line([(maria_x-30, maria_y-10), (maria_x-60, maria_y-5)],
             fill=(220, 200, 180), width=8)
    draw.line([(maria_x+30, maria_y-10), (maria_x+60, maria_y-5)],
             fill=(220, 200, 180), width=8)

    # CHILDREN clustered around - scared but comforted
    for i, (cx, cy) in enumerate([(maria_x-50, maria_y+10), (maria_x-30, maria_y+20),
                                   (maria_x+30, maria_y+20), (maria_x+50, maria_y+10)]):
        draw.ellipse([cx-7, cy-18, cx+7, cy-10],
                    fill=(200, 180, 160))
        # Nightgowns
        draw.rectangle([cx-9, cy-10, cx+9, cy+15],
                      fill=(240, 240, 250))

    # "FAVORITE THINGS" floating - whiskers, kettles, mittens
    # Snowflake
    draw.line([(60, 200), (80, 200)], fill=(200, 220, 255), width=3)
    draw.line([(70, 190), (70, 210)], fill=(200, 220, 255), width=3)
    draw.line([(63, 193), (77, 207)], fill=(200, 220, 255), width=3)
    draw.line([(77, 193), (63, 207)], fill=(200, 220, 255), width=3)

    # Rose
    draw.ellipse([100, 230, 120, 250], fill=(255, 150, 150))

    # Package (brown paper)
    draw.rectangle([240, 210, 265, 240], fill=(139, 69, 19))

    # Musical notes of the song - transforming fear
    for i in range(8):
        nx = random.randint(40, CARD_WIDTH-40)
        ny = random.randint(40, 150)
        draw_musical_note(draw, nx, ny, 8, (255, 215, 150))

    return img


def draw_07_lonely_goatherd():
    """VII - The Lonely Goatherd: Puppet show delight"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Warm indoor glow
    for y in range(CARD_HEIGHT):
        brightness = 180 - int(y * 0.15)
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(brightness, brightness-20, brightness-40))

    # PUPPET THEATER - center stage
    theater_x = CARD_WIDTH // 2
    theater_y = CARD_HEIGHT // 2

    # Theater frame - elaborate
    draw.rectangle([theater_x-80, theater_y-60, theater_x+80, theater_y+40],
                  fill=(139, 69, 19))
    # Curtains
    draw.rectangle([theater_x-80, theater_y-60, theater_x-65, theater_y+40],
                  fill=(180, 60, 60))
    draw.rectangle([theater_x+65, theater_y-60, theater_x+80, theater_y+40],
                  fill=(180, 60, 60))

    # PUPPETS performing - Tyrolean characters
    puppet_positions = [theater_x-40, theater_x, theater_x+40]

    for i, px in enumerate(puppet_positions):
        py = theater_y + int(15 * math.sin(i * 2))

        # Puppet in Lederhosen/dirndl
        draw.ellipse([px-8, py-25, px+8, py-15],
                    fill=(220, 200, 180))
        # Colorful costume
        colors = [(180, 60, 60), (60, 180, 60), (60, 60, 180)]
        draw.polygon([
            (px, py-15),
            (px-10, py+8),
            (px+10, py+8)
        ], fill=colors[i])

        # Strings visible - but joyful
        for sx in [px-4, px+4]:
            draw.line([(sx, theater_y-60), (sx, py-25)],
                     fill=(200, 200, 200), width=1)

    # CHILDREN watching - delighted
    for i, (cx, cy) in enumerate([(50, CARD_HEIGHT-80), (100, CARD_HEIGHT-70),
                                   (CARD_WIDTH-100, CARD_HEIGHT-70), (CARD_WIDTH-50, CARD_HEIGHT-80)]):
        draw.ellipse([cx-8, cx-20, cx+8, cy-10],
                    fill=(200, 180, 160))
        # Mouths open - laughing
        draw.arc([cx-5, cy-18, cx+5, cy-12],
                start=0, end=180, fill=(200, 100, 100), width=2)

    # Musical notes - YODELING
    for i in range(10):
        nx = random.randint(30, CARD_WIDTH-30)
        ny = random.randint(30, 100)
        draw_musical_note(draw, nx, ny, 8, (255, 215, 0))

    return img


def draw_09_so_long_farewell():
    """IX - So Long, Farewell: Children's goodbye, performance for guests"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Elegant party room - golden
    for y in range(CARD_HEIGHT):
        t = y / CARD_HEIGHT
        r = int(222 * (1-t) + 180 * t)
        g = int(184 * (1-t) + 160 * t)
        b = int(135 * (1-t) + 100 * t)
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

    # STAIRCASE - ascending
    for i in range(5):
        stair_y = CARD_HEIGHT - 60 - i*45
        stair_width = 180 - i*20
        stair_x = (CARD_WIDTH - stair_width) // 2

        draw.rectangle([stair_x, stair_y, stair_x+stair_width, stair_y+40],
                      fill=(160, 130, 90))

    # CHILDREN ascending - each saying goodbye
    child_positions = [
        (CARD_WIDTH//2, CARD_HEIGHT-40),
        (CARD_WIDTH//2-30, CARD_HEIGHT-85),
        (CARD_WIDTH//2+30, CARD_HEIGHT-85),
        (CARD_WIDTH//2, CARD_HEIGHT-130),
        (CARD_WIDTH//2-25, CARD_HEIGHT-175)
    ]

    for cx, cy in child_positions:
        # Child in nightclothes
        draw.ellipse([cx-7, cy-20, cx+7, cy-12],
                    fill=(200, 180, 160))
        draw.rectangle([cx-9, cy-12, cx+9, cy+10],
                      fill=(240, 240, 250))

        # Hand waving
        draw.line([(cx+9, cy-8), (cx+18, cy-15)],
                 fill=(200, 180, 160), width=4)

    # GUESTS below - watching, charmed
    for gx in [40, 80, CARD_WIDTH-80, CARD_WIDTH-40]:
        gy = CARD_HEIGHT - 50
        draw.ellipse([gx-6, gy-15, gx+6, gy-8],
                    fill=(180, 160, 140))
        # Formal attire
        draw.rectangle([gx-8, gy-8, gx+8, gy+8],
                      fill=(40, 40, 40))

    # Musical notes of their song - sweet, innocent
    for i in range(8):
        nx = random.randint(50, CARD_WIDTH-50)
        ny = random.randint(40, 140)
        draw_musical_note(draw, nx, ny, 8, (255, 235, 200))

    return img


def draw_11_something_good():
    """XI - Something Good: Maria and Georg's love, garden at night"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Night garden - romantic, starlit
    # Deep twilight sky
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     (25, 25, 80), (60, 40, 100))

    # Garden below
    draw.rectangle([0, CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT],
                  fill=(40, 60, 40))

    # STARS
    for i in range(20):
        sx = random.randint(10, CARD_WIDTH-10)
        sy = random.randint(10, CARD_HEIGHT//2 - 10)
        # Twinkling star
        draw.line([(sx-3, sy), (sx+3, sy)], fill=(255, 255, 200), width=2)
        draw.line([(sx, sy-3), (sx, sy+3)], fill=(255, 255, 200), width=2)

    # MARIA and GEORG - together, facing each other
    maria_x, georg_x = CARD_WIDTH//2 - 30, CARD_WIDTH//2 + 30
    fig_y = CARD_HEIGHT * 2 // 3

    # Maria
    draw.ellipse([maria_x-14, fig_y-45, maria_x+14, fig_y-20],
                fill=(220, 200, 180))
    draw.polygon([
        (maria_x, fig_y-20),
        (maria_x-25, fig_y+35),
        (maria_x+25, fig_y+35)
    ], fill=(200, 220, 240))  # Light dress

    # Georg
    draw.ellipse([georg_x-14, fig_y-45, georg_x+14, fig_y-20],
                fill=(200, 180, 160))
    draw.rectangle([georg_x-22, fig_y-20, georg_x+22, fig_y+35],
                  fill=(40, 40, 60))  # Dark suit

    # Hands TOUCHING - connection
    draw.line([(maria_x+25, fig_y), (georg_x-22, fig_y)],
             fill=(220, 200, 180), width=8)

    # Golden glow between them - love
    for r in range(40, 0, -3):
        gold = 200 + r
        draw.ellipse([CARD_WIDTH//2-r, fig_y-r, CARD_WIDTH//2+r, fig_y+r],
                    fill=(gold, gold-30, 0), outline=(gold, gold-30, 0))

    # Musical notes - tender melody
    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        nx = CARD_WIDTH//2 + int(70 * math.cos(rad))
        ny = fig_y + int(70 * math.sin(rad))
        draw_musical_note(draw, nx, ny, 8, (255, 235, 180))

    # Roses blooming in garden
    for rx in [50, 120, CARD_WIDTH-120, CARD_WIDTH-50]:
        ry = CARD_HEIGHT - random.randint(40, 80)
        draw.ellipse([rx-8, ry-8, rx+8, ry+8],
                    fill=(200, 100, 120))

    return img


def draw_12_processional():
    """XII - Processional/Maria: The wedding, joy and commitment"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Abbey - solemn, golden, sacred
    for y in range(CARD_HEIGHT):
        brightness = 200 - int(y * 0.15)
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(brightness, brightness-10, brightness-30))

    # AISLE - center perspective
    aisle_top = CARD_HEIGHT // 4
    draw.polygon([
        (CARD_WIDTH//2-80, CARD_HEIGHT),
        (CARD_WIDTH//2-30, aisle_top),
        (CARD_WIDTH//2+30, aisle_top),
        (CARD_WIDTH//2+80, CARD_HEIGHT)
    ], fill=(220, 220, 240))

    # MARIA - bride, radiant, CENTER
    maria_x, maria_y = CARD_WIDTH // 2, CARD_HEIGHT * 3 // 4

    # Veil and gown - white, glowing
    for r in range(50, 0, -3):
        white = 255 - r
        draw.ellipse([maria_x-r, maria_y-r-20, maria_x+r, maria_y+r+20],
                    fill=(white, white, white+20), outline=(white, white, white+20))

    # Head
    draw.ellipse([maria_x-18, maria_y-55, maria_x+18, maria_y-25],
                fill=(220, 200, 180))

    # Wedding gown
    draw.polygon([
        (maria_x, maria_y-25),
        (maria_x-45, maria_y+50),
        (maria_x+45, maria_y+50)
    ], fill=(255, 255, 255))

    # Veil
    draw.polygon([
        (maria_x-25, maria_y-60),
        (maria_x, maria_y-70),
        (maria_x+25, maria_y-60),
        (maria_x+35, maria_y+30),
        (maria_x-35, maria_y+30)
    ], fill=(245, 245, 255))

    # BOUQUET - edelweiss
    bouquet_x, bouquet_y = maria_x, maria_y + 20
    for offset in [-12, 0, 12]:
        draw_edelweiss(draw, bouquet_x+offset, bouquet_y, 12)

    # PROCESSIONAL MUSIC - organ, sacred
    for i in range(6):
        nx = random.randint(40, CARD_WIDTH-40)
        ny = random.randint(30, 100)
        draw_musical_note(draw, nx, ny, 10, (255, 235, 200))

    # Candles on sides
    for cx in [40, CARD_WIDTH-40]:
        for cy in [150, 220, 290]:
            # Candle
            draw.rectangle([cx-4, cy, cx+4, cy+35],
                          fill=(255, 250, 220))
            # Flame
            draw.ellipse([cx-6, cy-10, cx+6, cy],
                        fill=(255, 200, 0))

    return img


def draw_13_confitemini():
    """XIII - Confitemini Domino: Nuns helping escape, sacred resistance"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Abbey at night - dark, secretive
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(20, 20, 40))

    # Single candle light - conspiratorial
    candle_x = CARD_WIDTH // 4
    candle_y = CARD_HEIGHT // 3

    for r in range(80, 0, -4):
        brightness = 40 + r
        draw.ellipse([candle_x-r, candle_y-r, candle_x+r, candle_y+r],
                    fill=(brightness, brightness//2, 0), outline=(brightness, brightness//2, 0))

    # NUNS - three sisters helping
    nun_positions = [(60, CARD_HEIGHT//2), (110, CARD_HEIGHT//2 + 20),
                    (160, CARD_HEIGHT//2 + 10)]

    for nx, ny in nun_positions:
        # Nun
        draw.ellipse([nx-10, ny-28, nx+10, ny-15],
                    fill=(180, 170, 160))
        # Habit
        draw.polygon([
            (nx, ny-15),
            (nx-15, ny+20),
            (nx+15, ny+20)
        ], fill=(20, 20, 20))
        # Wimple
        draw.polygon([
            (nx-12, ny-30),
            (nx, ny-33),
            (nx+12, ny-30),
            (nx+12, ny-15),
            (nx-12, ny-15)
        ], fill=(255, 255, 255))

        # Hands holding car parts - sabotage!
        if random.random() > 0.3:
            draw.ellipse([nx+15, ny+5, nx+25, ny+15],
                        fill=(180, 170, 160))
            # Car part (distributor cap)
            draw.ellipse([nx+25, ny+8, nx+35, ny+18],
                        fill=(80, 80, 80))

    # CAR in shadows - disabled
    car_x = CARD_WIDTH - 100
    car_y = CARD_HEIGHT - 100

    draw.rectangle([car_x-40, car_y-30, car_x+40, car_y+20],
                  fill=(60, 60, 70))
    # Windows
    draw.rectangle([car_x-30, car_y-25, car_x+30, car_y-10],
                  fill=(40, 40, 50))

    # Musical notes of their chant - sacred defiance
    for i in range(5):
        nx = random.randint(180, CARD_WIDTH-40)
        ny = random.randint(50, 150)
        draw_musical_note(draw, nx, ny, 8, (200, 200, 220))

    # Latin text suggestion
    for i, lx in enumerate([50, 120, 190]):
        draw.line([(lx, CARD_HEIGHT-40), (lx+40, CARD_HEIGHT-40)],
                 fill=(150, 150, 170), width=2)

    return img


def draw_14_sixteen_reprise():
    """XIV - Sixteen Going on Seventeen Reprise: Liesl's heartbreak"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Same gazebo - but rain, darkness, betrayal
    # Storm sky
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(40, 40, 60))

    # RAIN - heavy
    for i in range(50):
        rx = random.randint(0, CARD_WIDTH)
        ry = random.randint(0, CARD_HEIGHT)
        draw.line([(rx, ry), (rx+4, ry+15)],
                 fill=(100, 100, 130), width=2)

    # Gazebo - now ominous
    gazebo_y = CARD_HEIGHT // 3
    for px in [60, 130, 200, 270]:
        draw.rectangle([px-8, gazebo_y, px+8, CARD_HEIGHT-60],
                      fill=(100, 100, 110))

    # LIESL - alone, sobbing
    liesl_x, liesl_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    draw.ellipse([liesl_x-14, liesl_y-42, liesl_x+14, liesl_y-20],
                fill=(220, 200, 180))

    # Wet dress
    draw.polygon([
        (liesl_x, liesl_y-20),
        (liesl_x-25, liesl_y+30),
        (liesl_x+25, liesl_y+30)
    ], fill=(140, 160, 180))  # Darker, wet

    # Hands to face - crying
    draw.ellipse([liesl_x-18, liesl_y-30, liesl_x-8, liesl_y-22],
                fill=(220, 200, 180))
    draw.ellipse([liesl_x+8, liesl_y-30, liesl_x+18, liesl_y-22],
                fill=(220, 200, 180))

    # MARIA arriving - comforting
    maria_x = liesl_x - 60
    maria_y = liesl_y + 10

    draw.ellipse([maria_x-12, maria_y-35, maria_x+12, maria_y-18],
                fill=(220, 200, 180))
    draw.polygon([
        (maria_x, maria_y-18),
        (maria_x-20, maria_y+20),
        (maria_x+20, maria_y+20)
    ], fill=(180, 200, 220))

    # Arm reaching to Liesl
    draw.line([(maria_x+20, maria_y-8), (liesl_x-25, liesl_y)],
             fill=(220, 200, 180), width=8)

    # Musical notes - but sad, comforting
    for i in range(4):
        nx = random.randint(80, 200)
        ny = random.randint(100, 200)
        draw_musical_note(draw, nx, ny, 8, (150, 150, 180))

    # Nazi flag in distance - the cause of betrayal
    flag_x = 250
    draw.rectangle([flag_x, 80, flag_x+40, 140],
                  fill=(200, 0, 0))
    # Black symbol
    draw.rectangle([flag_x+12, 100, flag_x+28, 120],
                  fill=(0, 0, 0))

    return img


def draw_15_do_re_mi_reprise():
    """XV - Do-Re-Mi Reprise: Family united through music at festival"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Festival stage - PUBLIC performance
    # Bright lights
    for y in range(CARD_HEIGHT):
        for x in range(CARD_WIDTH):
            dist_y = abs(y - CARD_HEIGHT//2)
            brightness = max(0, 180 - dist_y)
            draw.point((x, y), fill=(brightness, brightness-20, brightness-40))

    # FAMILY in formation - all eight
    positions = [
        (70, CARD_HEIGHT-120),   # Louisa
        (110, CARD_HEIGHT-110),  # Friedrich
        (150, CARD_HEIGHT-100),  # Liesl
        (190, CARD_HEIGHT-120),  # Brigitta
        (230, CARD_HEIGHT-130),  # Kurt
        (270, CARD_HEIGHT-120),  # Marta
        (310, CARD_HEIGHT-110),  # Gretl
    ]

    for i, (px, py) in enumerate(positions):
        # Each child
        draw.ellipse([px-9, py-28, px+9, py-15],
                    fill=(200, 180, 160))

        # Festival costume
        costume_colors = [(180, 160, 200), (200, 180, 160), (180, 200, 180),
                         (200, 180, 180), (180, 180, 200), (200, 200, 180), (200, 180, 200)]
        draw.rectangle([px-11, py-15, px+11, py+20],
                      fill=costume_colors[i])

        # Mouth open - singing
        draw.ellipse([px-4, py-22, px+4, py-18],
                    fill=(180, 100, 100))

    # MARIA and GEORG at sides - proud
    # Maria
    draw.ellipse([40, CARD_HEIGHT-140, 60, CARD_HEIGHT-120],
                fill=(220, 200, 180))
    draw.polygon([
        (50, CARD_HEIGHT-120),
        (35, CARD_HEIGHT-80),
        (65, CARD_HEIGHT-80)
    ], fill=(200, 220, 240))

    # Georg
    draw.ellipse([CARD_WIDTH-60, CARD_HEIGHT-140, CARD_WIDTH-40, CARD_HEIGHT-120],
                fill=(200, 180, 160))
    draw.rectangle([CARD_WIDTH-65, CARD_HEIGHT-120, CARD_WIDTH-35, CARD_HEIGHT-70],
                  fill=(40, 40, 60))

    # Musical notes - DO RE MI ascending
    note_positions = [60, 90, 120, 150, 180, 210, 240]
    for i, nx in enumerate(note_positions):
        ny = 80 - i * 10
        draw_musical_note(draw, nx, ny, 12, (255, 215, 0))

    # Audience silhouettes - watching
    for i in range(15):
        ax = random.randint(30, CARD_WIDTH-30)
        ay = CARD_HEIGHT - random.randint(30, 60)
        draw.ellipse([ax-4, ay-10, ax+4, ay-4],
                    fill=(60, 60, 70))

    return img


def draw_17_so_long_reprise():
    """XVII - So Long Farewell Reprise: Escape during festival"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Festival stage - but LEAVING
    # Spotlit stage left empty
    for y in range(CARD_HEIGHT):
        for x in range(0, CARD_WIDTH//2):
            dist = math.sqrt((x - CARD_WIDTH//4)**2 + (y - CARD_HEIGHT//2)**2)
            brightness = max(0, int(150 - dist * 0.6))
            draw.point((x, y), fill=(brightness, brightness//2, 0))

    # Dark escape route - right side
    draw.rectangle([CARD_WIDTH//2, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(20, 20, 40))

    # FAMILY sneaking away - silhouettes
    escape_positions = [
        (CARD_WIDTH//2 + 30, CARD_HEIGHT - 140),
        (CARD_WIDTH//2 + 50, CARD_HEIGHT - 130),
        (CARD_WIDTH//2 + 70, CARD_HEIGHT - 125),
        (CARD_WIDTH//2 + 90, CARD_HEIGHT - 120),
        (CARD_WIDTH//2 + 110, CARD_HEIGHT - 115),
        (CARD_WIDTH//2 + 130, CARD_HEIGHT - 110),
        (CARD_WIDTH//2 + 150, CARD_HEIGHT - 105),
        # Maria and Georg at back
        (CARD_WIDTH//2 + 170, CARD_HEIGHT - 100),
        (CARD_WIDTH//2 + 190, CARD_HEIGHT - 95),
    ]

    for px, py in escape_positions:
        # Dark silhouettes
        draw.ellipse([px-7, py-20, px+7, py-12],
                    fill=(60, 60, 80))
        draw.rectangle([px-9, py-12, px+9, py+15],
                      fill=(50, 50, 70))

    # EMPTY STAGE - spotlight on absence
    stage_x = CARD_WIDTH // 4
    stage_y = CARD_HEIGHT * 2 // 3

    # Microphone stand - abandoned
    draw.line([(stage_x, stage_y-50), (stage_x, stage_y+40)],
             fill=(120, 120, 120), width=6)
    draw.ellipse([stage_x-8, stage_y-60, stage_x+8, stage_y-50],
                fill=(100, 100, 100))

    # NAZI OFFICER discovering - angry
    officer_x = 60
    officer_y = CARD_HEIGHT - 90

    draw.ellipse([officer_x-12, officer_y-30, officer_x+12, officer_y-15],
                fill=(200, 180, 160))
    draw.rectangle([officer_x-15, officer_y-15, officer_x+15, officer_y+25],
                  fill=(80, 80, 60))  # Uniform

    # Arm pointing - discovering escape
    draw.line([(officer_x+15, officer_y), (officer_x+45, officer_y-15)],
             fill=(200, 180, 160), width=6)

    # Musical notes fading - song interrupted
    for i in range(4):
        nx = CARD_WIDTH//4 + random.randint(-40, 40)
        ny = 100 + i * 40
        opacity = 255 - i * 60
        draw_musical_note(draw, nx, ny, 8,
                         (opacity, opacity-50, 0))

    return img


# Generate all remaining Major Arcana!
if __name__ == '__main__':
    print("🎬 COMPLETING THE CINEMATIC JOURNEY! Final Major Arcana! 🎬\n")

    cards_to_generate = [
        ("major-02", draw_02_maria),
        ("major-03", draw_03_i_have_confidence),
        ("major-04", draw_04_sixteen_going_on_seventeen),
        ("major-05", draw_05_my_favorite_things),
        ("major-07", draw_07_lonely_goatherd),
        ("major-09", draw_09_so_long_farewell),
        ("major-11", draw_11_something_good),
        ("major-12", draw_12_processional),
        ("major-13", draw_13_confitemini),
        ("major-14", draw_14_sixteen_reprise),
        ("major-15", draw_15_do_re_mi_reprise),
        ("major-17", draw_17_so_long_reprise),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} Major Arcana cards! ✨")
    print("🎊 THE SOUND OF MUSIC TAROT IS COMPLETE! 🎊")
    print("🏔️  From mountain to love to defiance to freedom... 🏔️")
