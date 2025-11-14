#!/usr/bin/env python3
"""
Generate the final cards to complete the Sound of Music Tarot deck!
Completing all minor suits and adding more Major Arcana
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw
import math
import random

from som_visual_toolkit import *

# === COMPLETING MINOR SUITS ===

def draw_six_of_songs():
    """Six of Songs: Harmonic convergence, voices blending"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_songs_background(draw)

    # SIX voices forming perfect harmony
    center_x, center_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        fx = center_x + int(70 * math.cos(rad))
        fy = center_y + int(70 * math.sin(rad))

        # Singer
        draw.ellipse([fx-10, fy-25, fx+10, fy-10],
                    fill=(220, 200, 180))
        draw.rectangle([fx-12, fy-10, fx+12, fy+15],
                      fill=(random.choice([SongsColors.ACCENT_1, SongsColors.ACCENT_2])))

        # Musical note from each
        note_angle = angle + 90
        note_rad = math.radians(note_angle)
        nx = fx + int(30 * math.cos(note_rad))
        ny = fy + int(30 * math.sin(note_rad))
        draw_musical_note(draw, nx, ny, 8, SongsColors.ACCENT_3)

    # Center - where harmony meets
    draw.ellipse([center_x-15, center_y-15, center_x+15, center_y+15],
                fill=SongsColors.HIGHLIGHT)

    return img


def draw_nine_of_songs():
    """Nine of Songs: Joy almost complete, penultimate verse"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_songs_background(draw)

    # NINE musical notes rising - almost there
    for i in range(9):
        x = 40 + i * 30
        y = CARD_HEIGHT - 80 - i * 35

        # Note rising
        draw_musical_note(draw, x, y, 10, SongsColors.PRIMARY)

        # Trail behind it
        for j in range(5):
            draw.ellipse([x-2, y+10+j*8, x+2, y+14+j*8],
                        fill=(135+j*20, 206-j*10, 250-j*10))

    # Tenth position - empty, waiting
    final_x = 40 + 9 * 30
    final_y = CARD_HEIGHT - 80 - 9 * 35

    # Empty space glowing
    for r in range(20, 0, -2):
        draw.ellipse([final_x-r, final_y-r, final_x+r, final_y+r],
                    outline=SongsColors.HIGHLIGHT, width=1)

    return img


def draw_eleven_of_songs():
    """Eleven of Songs: Joy sustained, enduring music"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_songs_background(draw)

    # ELEVEN musical notes sustained in air - continuing
    for i in range(11):
        angle = i * 33
        rad = math.radians(angle)
        radius = 60 + (i % 3) * 20

        nx = CARD_WIDTH//2 + int(radius * math.cos(rad))
        ny = CARD_HEIGHT//2 + int(radius * math.sin(rad))

        # Note glowing with sustained joy
        draw_musical_note(draw, nx, ny, 9, SongsColors.PRIMARY)

        # Glow
        for r in range(15, 0, -2):
            draw.ellipse([nx-r, ny-r, nx+r, ny+r],
                        outline=SongsColors.HIGHLIGHT, width=1)

    # Center - source of continuing joy
    center_x, center_y = CARD_WIDTH // 2, CARD_HEIGHT // 2
    draw.ellipse([center_x-20, center_y-20, center_x+20, center_y+20],
                fill=SongsColors.ACCENT_3)

    return img


def draw_three_of_whistles():
    """Three of Whistles: Learning discipline, forming order"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_whistles_background(draw)

    # THREE figures - learning formation
    positions = [(CARD_WIDTH//4, CARD_HEIGHT*2//3),
                 (CARD_WIDTH//2, CARD_HEIGHT*2//3 - 30),
                 (3*CARD_WIDTH//4, CARD_HEIGHT*2//3)]

    for i, (fx, fy) in enumerate(positions):
        # Figure learning
        draw.ellipse([fx-12, fy-30, fx+12, fy-15],
                    fill=(200, 200, 220))
        draw.rectangle([fx-14, fy-15, fx+14, fy+20],
                      fill=WhistlesColors.SECONDARY)

        # Whistle being taught
        draw_whistle(draw, fx, fy+35, 12, WhistlesColors.ACCENT)

    # Lines connecting - learning coordination
    draw.line([positions[0], positions[1]],
             fill=WhistlesColors.ACCENT, width=2)
    draw.line([positions[1], positions[2]],
             fill=WhistlesColors.ACCENT, width=2)

    return img


def draw_six_of_whistles():
    """Six of Whistles: Order harmonizing, discipline as beauty"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_whistles_background(draw)

    # SIX figures in perfect hexagonal formation
    center_x, center_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        fx = center_x + int(70 * math.cos(rad))
        fy = center_y + int(70 * math.sin(rad))

        # Figure
        draw.ellipse([fx-10, fy-25, fx+10, fy-12],
                    fill=(200, 200, 220))
        draw.rectangle([fx-12, fy-12, fx+12, fy+15],
                      fill=WhistlesColors.SECONDARY)

        # Whistle
        draw_whistle(draw, fx, fy+25, 10, WhistlesColors.ACCENT)

    # Perfect geometric center
    draw.ellipse([center_x-12, center_y-12, center_x+12, center_y+12],
                fill=WhistlesColors.ACCENT)

    # Connecting lines - perfect geometry
    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        fx = center_x + int(70 * math.cos(rad))
        fy = center_y + int(70 * math.sin(rad))
        draw.line([(center_x, center_y), (fx, fy)],
                 fill=WhistlesColors.ACCENT, width=2)

    return img


def draw_eight_of_whistles():
    """Eight of Whistles: Discipline hardening, order ossifying"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Very rigid grid background
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=(20, 20, 90))

    # Perfect grid - oppressive
    for x in range(0, CARD_WIDTH, 30):
        draw.line([(x, 0), (x, CARD_HEIGHT)],
                 fill=(30, 30, 100), width=2)
    for y in range(0, CARD_HEIGHT, 30):
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(30, 30, 100), width=2)

    # EIGHT figures in rigid grid
    for row in range(2):
        for col in range(4):
            fx = 50 + col * 60
            fy = CARD_HEIGHT//3 + row * 100

            # Identical figures
            draw.ellipse([fx-10, fy-25, fx+10, fy-13],
                        fill=(180, 180, 200))
            draw.rectangle([fx-12, fy-13, fx+12, fy+18],
                          fill=WhistlesColors.SECONDARY)

            # Same whistle
            draw_whistle(draw, fx, fy+30, 10, WhistlesColors.ACCENT)

    return img


def draw_nine_of_whistles():
    """Nine of Whistles: Order almost absolute, discipline nearly complete"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_whistles_background(draw)

    # NINE whistles arranged in perfect 3x3 grid
    for row in range(3):
        for col in range(3):
            wx = 70 + col * 70
            wy = 100 + row * 90

            # Whistle on stand
            draw.rectangle([wx-3, wy-50, wx+3, wy],
                          fill=(150, 150, 150))
            draw_whistle(draw, wx, wy-50, 15, WhistlesColors.ACCENT)

            # Each whistle glowing with authority
            for r in range(30, 0, -3):
                draw.ellipse([wx-r, wy-50-r, wx+r, wy-50+r],
                            outline=WhistlesColors.ACCENT, width=1)

    # Perfect grid lines connecting them
    for row in range(3):
        wy = 100 + row * 90 - 50
        draw.line([(70, wy), (70+140, wy)],
                 fill=WhistlesColors.ACCENT, width=2)

    for col in range(3):
        wx = 70 + col * 70
        draw.line([(wx, 100-50), (wx, 100+180-50)],
                 fill=WhistlesColors.ACCENT, width=2)

    return img


def draw_eleven_of_whistles():
    """Goatherd of Whistles: Paradox - discipline in service of freedom"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    # Blended background - structure and nature
    for y in range(CARD_HEIGHT):
        t = y / CARD_HEIGHT
        r = int(25 + (100 - 25) * t)
        g = int(25 + (149 - 25) * t)
        b = int(112 + (237 - 112) * t)
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

    # Geometric grid fading to organic
    for i in range(8):
        y = i * 50
        opacity = 1 - (i * 0.12)
        gray = int(45 * opacity)
        draw.line([(0, y), (CARD_WIDTH, y)],
                 fill=(gray, gray, gray+80), width=1)

    # FIGURE - both disciplined and free
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    # Head
    draw.ellipse([fig_x-18, fig_y-55, fig_x+18, fig_y-25],
                fill=(200, 200, 220))

    # Mixed clothing - uniform jacket with Tyrolean touches
    draw.rectangle([fig_x-28, fig_y-25, fig_x+28, fig_y+35],
                  fill=WhistlesColors.PRIMARY)

    # But decorated with folk embroidery (colorful accents)
    for ey in [fig_y-15, fig_y, fig_y+15]:
        draw.line([(fig_x-20, ey), (fig_x+20, ey)],
                 fill=(180, 60, 60), width=2)

    # Whistle AND edelweiss
    draw_whistle(draw, fig_x-30, fig_y+50, 12, WhistlesColors.ACCENT)
    draw_edelweiss(draw, fig_x+30, fig_y+50, 12)

    return img


def draw_three_of_puppets():
    """Three of Puppets: Learning craft, first lessons in making"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # THREE puppets - student, journeyman, master
    sizes = [20, 30, 40]
    positions = [(70, CARD_HEIGHT-100), (CARD_WIDTH//2, CARD_HEIGHT-120),
                 (CARD_WIDTH-70, CARD_HEIGHT-100)]

    for i, (px, py) in enumerate(positions):
        size = sizes[i]

        # Puppet
        draw.ellipse([px-size//3, py-size, px+size//3, py-size//2],
                    fill=(200, 180, 150))
        draw.polygon([
            (px, py-size//2),
            (px-size//2, py+size//3),
            (px+size//2, py+size//3)
        ], fill=(180, 140, 60))

        # Control bar
        control_y = py - size*2
        draw.rectangle([px-size//2, control_y-4, px+size//2, control_y+4],
                      fill=PuppetsColors.SECONDARY)

        # Strings
        draw_puppet_strings(draw, px, control_y+4, px, py-size,
                           PuppetsColors.STRING)

    # Spotlight on learning
    for x in range(CARD_WIDTH):
        for y in range(CARD_HEIGHT*2//3, CARD_HEIGHT):
            dist_y = abs(y - (CARD_HEIGHT - 110))
            brightness = max(0, 50 - dist_y//3)
            draw.point((x, y), fill=(brightness, brightness//2, 0))

    return img


def draw_six_of_puppets():
    """Six of Puppets: Craft in harmony, performers united"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # SIX puppets in choreographed performance
    puppet_y = CARD_HEIGHT * 2 // 3

    for i in range(6):
        px = 40 + i * 45
        py = puppet_y + int(20 * math.sin(i * math.pi / 2.5))

        # Puppet in motion
        draw.ellipse([px-8, py-25, px+8, py-15],
                    fill=(200, 180, 150))
        draw.polygon([
            (px, py-15),
            (px-10, py+8),
            (px+10, py+8)
        ], fill=(random.choice([(180, 60, 60), (60, 80, 180),
                                (180, 140, 60), (140, 60, 180)])))

        # Control bar
        control_y = CARD_HEIGHT//3
        draw.rectangle([px-12, control_y-3, px+12, control_y+3],
                      fill=PuppetsColors.SECONDARY)

        # Strings
        draw_puppet_strings(draw, px, control_y+3, px, py-25,
                           PuppetsColors.STRING)

    # Golden stage floor
    draw.rectangle([30, puppet_y+15, CARD_WIDTH-30, puppet_y+25],
                  fill=PuppetsColors.SECONDARY)

    return img


def draw_nine_of_puppets():
    """Nine of Puppets: Performance almost complete, final act"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # NINE puppets - curtain almost closing
    for i in range(9):
        col = i % 3
        row = i // 3

        px = 80 + col * 70
        py = CARD_HEIGHT//2 + row * 70

        # Puppet
        draw.ellipse([px-7, py-22, px+7, py-14],
                    fill=(200, 180, 150))
        draw.polygon([
            (px, py-14),
            (px-9, py+6),
            (px+9, py+6)
        ], fill=(random.choice([(180, 60, 60), (60, 80, 180)])))

        # Strings
        control_y = py - 45
        for sx in [px-4, px+4]:
            draw.line([(sx, control_y), (sx, py-22)],
                     fill=PuppetsColors.STRING, width=1)

    # Curtains starting to close
    draw.polygon([
        (0, 0),
        (60, 80),
        (60, CARD_HEIGHT),
        (0, CARD_HEIGHT)
    ], fill=PuppetsColors.PRIMARY)

    draw.polygon([
        (CARD_WIDTH, 0),
        (CARD_WIDTH-60, 80),
        (CARD_WIDTH-60, CARD_HEIGHT),
        (CARD_WIDTH, CARD_HEIGHT)
    ], fill=PuppetsColors.PRIMARY)

    return img


def draw_eleven_of_puppets():
    """Goatherd of Puppets: Playful craft, art as joy"""
    # Return to the Goatherd archetype - puppet show as pure delight
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_puppets_background(draw)

    # PUPPET SHOW - delightful, charming
    theater_x = CARD_WIDTH // 2
    theater_y = CARD_HEIGHT * 2 // 3

    # Little theater stage
    draw.rectangle([theater_x-60, theater_y-50, theater_x+60, theater_y+10],
                  fill=(139, 69, 19))

    # Colorful curtains
    draw.rectangle([theater_x-60, theater_y-50, theater_x-50, theater_y+10],
                  fill=PuppetsColors.PRIMARY)
    draw.rectangle([theater_x+50, theater_y-50, theater_x+60, theater_y+10],
                  fill=PuppetsColors.PRIMARY)

    # THREE joyful puppets performing
    for i, px in enumerate([theater_x-30, theater_x, theater_x+30]):
        py = theater_y - 20 + int(10 * math.sin(i * 2))

        # Colorful puppet
        color = random.choice([(255, 150, 150), (150, 255, 150),
                              (150, 150, 255), (255, 255, 150)])

        draw.ellipse([px-6, py-18, px+6, py-10],
                    fill=(220, 200, 180))
        draw.polygon([
            (px, py-10),
            (px-7, py+5),
            (px+7, py+5)
        ], fill=color)

        # Visible strings - but this is FUN
        draw.line([(px-3, theater_y-50), (px-3, py-18)],
                 fill=(200, 200, 200), width=1)
        draw.line([(px+3, theater_y-50), (px+3, py-18)],
                 fill=(200, 200, 200), width=1)

    # OPERATOR visible above - smiling, delighting
    operator_y = theater_y - 80
    draw.ellipse([theater_x-12, operator_y-25, theater_x+12, operator_y-10],
                fill=(220, 200, 180))

    # Big smile
    draw.arc([theater_x-8, operator_y-22, theater_x+8, operator_y-14],
            start=0, end=180, fill=(100, 50, 50), width=2)

    return img


def draw_two_of_mountains():
    """Two of Mountains: Partnership in tradition, shared heritage"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # TWO figures - teaching and learning
    teacher_x = CARD_WIDTH // 3
    student_x = 2 * CARD_WIDTH // 3
    fig_y = CARD_HEIGHT * 2 // 3

    # Teacher
    draw.ellipse([teacher_x-14, fig_y-40, teacher_x+14, fig_y-18],
                fill=(160, 140, 120))
    draw.polygon([
        (teacher_x, fig_y-18),
        (teacher_x-22, fig_y+25),
        (teacher_x+22, fig_y+25)
    ], fill=(80, 60, 40))

    # Student
    draw.ellipse([student_x-12, fig_y-35, student_x+12, fig_y-15],
                fill=(180, 160, 140))
    draw.polygon([
        (student_x, fig_y-15),
        (student_x-18, fig_y+20),
        (student_x+18, fig_y+20)
    ], fill=(100, 80, 60))

    # Teacher's hand extended - giving
    draw.line([(teacher_x+22, fig_y), (teacher_x+50, fig_y-10)],
             fill=(160, 140, 120), width=8)

    # Student's hands receiving
    draw.line([(student_x-18, fig_y), (student_x-40, fig_y-8)],
             fill=(180, 160, 140), width=7)

    # EDELWEISS passing between them - knowledge transfer
    exchange_x = (teacher_x + student_x) // 2
    draw_edelweiss(draw, exchange_x, fig_y-15, 18)

    # Connection line
    draw.line([(teacher_x+30, fig_y-5), (student_x-30, fig_y-5)],
             fill=MountainsColors.ACCENT, width=3)

    return img


def draw_six_of_mountains():
    """Six of Mountains: Harmonious transmission, wisdom flowing"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # SIX figures in circle - oral tradition
    center_x, center_y = CARD_WIDTH // 2, CARD_HEIGHT * 2 // 3

    for i in range(6):
        angle = i * 60
        rad = math.radians(angle)
        fx = center_x + int(65 * math.cos(rad))
        fy = center_y + int(65 * math.sin(rad))

        # Figure
        draw.ellipse([fx-10, fy-25, fx+10, fy-12],
                    fill=(180, 160, 140))
        draw.rectangle([fx-12, fy-12, fx+12, fy+15],
                      fill=(100, 80, 60))

    # CENTER - fire, story circle
    for r in range(18, 0, -2):
        color = (255 - r*8, 200 - r*6, 0)
        draw.ellipse([center_x-r, center_y-r, center_x+r, center_y+r],
                    fill=color)

    # Edelweiss around the circle
    for i in range(6):
        angle = i * 60 + 30
        rad = math.radians(angle)
        fx = center_x + int(50 * math.cos(rad))
        fy = center_y + int(50 * math.sin(rad))
        draw_edelweiss(draw, fx, fy, 10)

    return img


def draw_nine_of_mountains():
    """Nine of Mountains: Wisdom almost complete, heritage nearly passed"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # NINE stones in path leading upward
    for i in range(9):
        sx = 40 + i * 25
        sy = CARD_HEIGHT - 60 - i * 30

        # Stone marker
        draw.rectangle([sx-10, sy-30, sx+10, sy],
                      fill=MountainsColors.PRIMARY)

        # Edelweiss at each stone
        draw_edelweiss(draw, sx+15, sy-15, 8)

    # TENTH position at peak - empty, glowing, waiting
    final_x = 40 + 9 * 25
    final_y = CARD_HEIGHT - 60 - 9 * 30

    for r in range(25, 0, -2):
        draw.ellipse([final_x-r, final_y-r, final_x+r, final_y+r],
                    outline=MountainsColors.ACCENT, width=1)

    # Figure climbing - almost there
    climber_x = 40 + 8 * 25
    climber_y = CARD_HEIGHT - 60 - 8 * 30 + 20

    draw.ellipse([climber_x-8, climber_y-22, climber_x+8, climber_y-12],
                fill=(180, 160, 140))

    return img


def draw_eleven_of_mountains():
    """Officer of Mountains: Authority from tradition, command through heritage"""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    get_mountains_background(draw, with_peaks=True)

    # FIGURE - bearing authority of ancestors
    fig_x, fig_y = CARD_WIDTH // 2, CARD_HEIGHT // 2

    # Mountain-stone aura
    for r in range(100, 0, -5):
        gray = 110 + r//3
        draw.ellipse([fig_x-r, fig_y-r, fig_x+r, fig_y+r],
                    fill=(gray, gray-10, gray-20), outline=(gray, gray-10, gray-20))

    # Head - stern, weathered
    draw.ellipse([fig_x-20, fig_y-65, fig_x+20, fig_y-30],
                fill=(160, 140, 120))

    # Traditional robes mixed with authority
    draw.polygon([
        (fig_x, fig_y-30),
        (fig_x-38, fig_y+50),
        (fig_x+38, fig_y+50)
    ], fill=(60, 50, 40))

    # Staff of office
    staff_x = fig_x + 45
    draw.line([(staff_x, fig_y-55), (staff_x, fig_y+65)],
             fill=(80, 60, 40), width=10)

    # Ancient stone at top of staff
    draw.ellipse([staff_x-10, fig_y-70, staff_x+10, fig_y-55],
                fill=MountainsColors.PRIMARY)

    # Edelweiss crown - heritage
    for offset in [-20, 0, 20]:
        draw_edelweiss(draw, fig_x+offset, fig_y-75, 10)

    # Ancient symbols at feet - tradition
    for i, sx in enumerate([fig_x-30, fig_x, fig_x+30]):
        sy = CARD_HEIGHT - 60
        draw.rectangle([sx-8, sy-16, sx+8, sy],
                      fill=MountainsColors.SHADOW)

    return img


# Generate all final cards!
if __name__ == '__main__':
    print("🎊 COMPLETING THE DECK! Final cards! 🎊\n")

    cards_to_generate = [
        # Songs completion
        ("songs-05", draw_six_of_songs),
        ("songs-08", draw_nine_of_songs),
        ("songs-11", draw_eleven_of_songs),

        # Whistles completion
        ("whistles-02", draw_three_of_whistles),
        ("whistles-05", draw_six_of_whistles),
        ("whistles-07", draw_eight_of_whistles),
        ("whistles-08", draw_nine_of_whistles),
        ("whistles-11", draw_eleven_of_whistles),

        # Puppets completion
        ("puppets-02", draw_three_of_puppets),
        ("puppets-05", draw_six_of_puppets),
        ("puppets-08", draw_nine_of_puppets),
        ("puppets-11", draw_eleven_of_puppets),

        # Mountains completion
        ("mountains-01", draw_two_of_mountains),
        ("mountains-05", draw_six_of_mountains),
        ("mountains-08", draw_nine_of_mountains),
        ("mountains-11", draw_eleven_of_mountains),
    ]

    for slug, generator_func in cards_to_generate:
        card_name = generator_func.__doc__.split('\n')[0] if generator_func.__doc__ else slug
        print(f"Creating {card_name}...")
        img = generator_func()
        filepath = os.path.join("..", "cards", f"{slug}.png")
        img.save(filepath)
        print(f"  ✓ Saved to {filepath}")

    print(f"\n✨ Created {len(cards_to_generate)} cards! ✨")
    print("🎯 All minor suits complete! Now for the Major Arcana... 🎯")
