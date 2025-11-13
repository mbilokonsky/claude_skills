#!/usr/bin/env python3
"""
Custom pixel art generation for the Dance suit
Each card is hand-crafted to tell its unique story
"""

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

# Color palette
PALETTE = bvt.SuitColors.DANCE


def draw_dance_0_ace(img, draw):
    """
    Ace of Dance: the first move, pure movement potential, rhythm spark in the body
    Content: A single gesture beginning, the first movement impulse

    Visual: One figure in the moment of first movement, radial energy beginning
    """
    # Radial gradient from center - the spark of movement
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 120, PALETTE['heat'], PALETTE['shadow'])

    # Single figure beginning to move
    fig_x, fig_y = WIDTH // 2, HEIGHT // 2 + 60

    # Head
    draw.ellipse([fig_x - 14, fig_y - 80, fig_x + 14, fig_y - 52], fill=PALETTE['accent'])

    # Body in initial movement - one arm starting to rise
    body_points = [
        (fig_x, fig_y - 52),
        (fig_x - 25, fig_y - 30),
        (fig_x - 25, fig_y + 30),
        (fig_x + 25, fig_y + 30),
        (fig_x + 25, fig_y - 30)
    ]
    draw.polygon(body_points, fill=PALETTE['primary'])

    # One arm rising - the first gesture
    arm_points = [
        (fig_x + 25, fig_y - 20),
        (fig_x + 50, fig_y - 60),
        (fig_x + 54, fig_y - 55),
        (fig_x + 29, fig_y - 15)
    ]
    draw.polygon(arm_points, fill=PALETTE['primary'])

    # Energy burst lines radiating from the moving arm
    for angle in [30, 45, 60, 75]:
        rad = angle * math.pi / 180
        length = 40
        end_x = fig_x + 50 + int(length * math.cos(rad))
        end_y = fig_y - 60 - int(length * math.sin(rad))
        draw.line([(fig_x + 50, fig_y - 60), (end_x, end_y)],
                 fill=PALETTE['electric'], width=2)


def draw_dance_1_two(img, draw):
    """
    Two of Dance: dancing together, movement dialogue, bodies in conversation
    Content: Two bodies in motion together, mirroring or complementing

    Visual: Two figures in complementary movement
    """
    # Radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2 + 20, 140, PALETTE['heat'], PALETTE['shadow'])

    # Two figures dancing together
    # Left figure
    left_x, left_y = 80, HEIGHT - 100

    draw.ellipse([left_x - 12, left_y - 70, left_x + 12, left_y - 46], fill=PALETTE['accent'])
    body_left = [
        (left_x, left_y - 46),
        (left_x - 22, left_y - 25),
        (left_x - 22, left_y + 35),
        (left_x + 22, left_y + 35),
        (left_x + 22, left_y - 25)
    ]
    draw.polygon(body_left, fill=PALETTE['primary'])

    # Left figure arm reaching right
    draw.polygon([
        (left_x + 22, left_y - 15),
        (left_x + 60, left_y - 10),
        (left_x + 62, left_y - 5),
        (left_x + 24, left_y - 10)
    ], fill=PALETTE['primary'])

    # Right figure
    right_x, right_y = 200, HEIGHT - 100

    draw.ellipse([right_x - 12, right_y - 70, right_x + 12, right_y - 46], fill=PALETTE['accent'])
    body_right = [
        (right_x, right_y - 46),
        (right_x - 22, right_y - 25),
        (right_x - 22, right_y + 35),
        (right_x + 22, right_y + 35),
        (right_x + 22, right_y - 25)
    ]
    draw.polygon(body_right, fill=PALETTE['secondary'])

    # Right figure arm reaching left
    draw.polygon([
        (right_x - 22, right_y - 15),
        (right_x - 60, right_y - 10),
        (right_x - 62, right_y - 5),
        (right_x - 24, right_y - 10)
    ], fill=PALETTE['secondary'])

    # Energy connection between them
    draw.line([(left_x + 60, left_y - 10), (right_x - 60, right_y - 10)],
             fill=PALETTE['electric'], width=3)


def draw_dance_2_three(img, draw):
    """
    Three of Dance: choreography emerging, group movement forming
    Content: Three dancers finding formation, initial choreography

    Visual: Three figures beginning to move in coordination
    """
    # Radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 150, PALETTE['heat'], PALETTE['shadow'])

    # Three figures in triangular formation
    positions = [
        (WIDTH//2, HEIGHT//2 - 40),  # Front
        (WIDTH//2 - 60, HEIGHT//2 + 60),  # Back left
        (WIDTH//2 + 60, HEIGHT//2 + 60)   # Back right
    ]

    for i, (x, y) in enumerate(positions):
        # Head
        draw.ellipse([x - 11, y - 50, x + 11, y - 28], fill=PALETTE['accent'])

        # Body
        body = [
            (x, y - 28),
            (x - 20, y - 10),
            (x - 20, y + 30),
            (x + 20, y + 30),
            (x + 20, y - 10)
        ]
        color = [PALETTE['primary'], PALETTE['secondary'], PALETTE['primary']][i]
        draw.polygon(body, fill=color)

        # Arms in movement
        if i == 0:  # Front dancer - arms out
            draw.line([(x - 20, y), (x - 40, y - 5)], fill=color, width=6)
            draw.line([(x + 20, y), (x + 40, y - 5)], fill=color, width=6)

    # Connecting energy lines showing formation
    draw.line([positions[0], positions[1]], fill=PALETTE['electric'], width=1)
    draw.line([positions[0], positions[2]], fill=PALETTE['electric'], width=1)
    draw.line([positions[1], positions[2]], fill=PALETTE['electric'], width=1)


def draw_dance_3_four(img, draw):
    """
    Four of Dance: choreography stable, movement established, the routine set
    Content: Four dancers in formation, stable choreography

    Visual: Four figures in square formation, synchronized
    """
    # Radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2 + 20, 160, PALETTE['heat'], PALETTE['shadow'])

    # Four figures in square formation
    spacing = 70
    center_x, center_y = WIDTH // 2, HEIGHT // 2 + 20

    positions = [
        (center_x - spacing, center_y - spacing),
        (center_x + spacing, center_y - spacing),
        (center_x - spacing, center_y + spacing),
        (center_x + spacing, center_y + spacing)
    ]

    for i, (x, y) in enumerate(positions):
        # Head
        draw.ellipse([x - 10, y - 40, x + 10, y - 20], fill=PALETTE['accent'])

        # Body
        body = [
            (x, y - 20),
            (x - 18, y - 5),
            (x - 18, y + 25),
            (x + 18, y + 25),
            (x + 18, y - 5)
        ]
        color = PALETTE['primary'] if i % 2 == 0 else PALETTE['secondary']
        draw.polygon(body, fill=color)

    # Stage floor showing the formation
    stage_points = [
        (center_x - spacing - 25, center_y + spacing + 30),
        (center_x + spacing + 25, center_y + spacing + 30),
        (center_x + spacing + 15, center_y + spacing + 50),
        (center_x - spacing - 15, center_y + spacing + 50)
    ]
    draw.polygon(stage_points, fill=PALETTE['shadow'])


def draw_dance_4_five(img, draw):
    """
    Five of Dance: choreography disrupted, unexpected movement, dance challenged
    Content: Dancers encountering obstacle, choreography meeting disruption

    Visual: Figures in disrupted formation, one fallen or off-beat
    """
    # Radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 140, PALETTE['heat'], PALETTE['shadow'])

    # Four figures still in formation
    for i, (x, y) in enumerate([(70, 200), (140, 190), (210, 200)]):
        draw.ellipse([x - 9, y - 35, x + 9, y - 17], fill=PALETTE['accent'])
        body = [
            (x, y - 17),
            (x - 16, y - 5),
            (x - 16, y + 20),
            (x + 16, y + 20),
            (x + 16, y - 5)
        ]
        draw.polygon(body, fill=PALETTE['secondary'])

    # Fifth figure FALLEN or stumbling - the disruption
    fallen_x, fallen_y = 140, 300

    # Head lower/tilted
    draw.ellipse([fallen_x - 10, fallen_y - 25, fallen_x + 10, fallen_y - 7], fill=PALETTE['accent'])

    # Body off-balance, falling
    body_fallen = [
        (fallen_x, fallen_y - 7),
        (fallen_x - 30, fallen_y + 5),
        (fallen_x - 25, fallen_y + 25),
        (fallen_x + 15, fallen_y + 25),
        (fallen_x + 20, fallen_y + 5)
    ]
    draw.polygon(body_fallen, fill=PALETTE['primary'])

    # Motion lines showing the fall
    for offset in [10, 20, 30]:
        draw.line([(fallen_x - 25 - offset, fallen_y), (fallen_x - 25 - offset - 10, fallen_y)],
                 fill=PALETTE['shadow'], width=2)


def draw_dance_5_six(img, draw):
    """
    Six of Dance: movement restored, new choreography, improvisation integrated
    Content: Dancers in new formation, choreography adapted

    Visual: Six figures in new, more complex formation
    """
    # Radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 165, PALETTE['heat'], PALETTE['shadow'])

    # Six figures in hexagonal formation - new choreography
    center_x, center_y = WIDTH // 2, HEIGHT // 2 + 20
    radius = 80

    for i in range(6):
        angle = (i * 60 - 90) * math.pi / 180
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))

        # Head
        draw.ellipse([x - 9, y - 35, x + 9, y - 17], fill=PALETTE['accent'])

        # Body
        body = [
            (x, y - 17),
            (x - 15, y - 5),
            (x - 15, y + 20),
            (x + 15, y + 20),
            (x + 15, y - 5)
        ]
        color = PALETTE['primary'] if i % 2 == 0 else PALETTE['secondary']
        draw.polygon(body, fill=color)

        # Arms reaching toward center - showing connection
        arm_angle = angle + math.pi
        arm_x = x + int(15 * math.cos(arm_angle))
        arm_y = y + int(15 * math.sin(arm_angle))
        center_reach_x = center_x - int(20 * math.cos(angle))
        center_reach_y = center_y - int(20 * math.sin(angle))

        draw.line([(arm_x, arm_y), (center_reach_x, center_reach_y)],
                 fill=color, width=5)

    # Energy center showing restored flow
    draw.ellipse([center_x - 15, center_y - 15, center_x + 15, center_y + 15],
                fill=PALETTE['electric'])


def draw_dance_6_seven(img, draw):
    """
    Seven of Dance: examining the movement, choreography review, watching yourself move
    Content: A dancer watching themselves in mirrors, choosing which movement

    Visual: Figure with mirror reflections, contemplating choreography
    """
    # Background
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 140, PALETTE['heat'], PALETTE['shadow'])

    # "Mirrors" on sides showing different choreography options
    # Left mirror
    draw.rectangle([20, 100, 70, 320], fill=PALETTE['shadow'], outline=PALETTE['secondary'], width=2)
    # Reflection - small figure
    draw.ellipse([40, 180, 50, 195], fill=PALETTE['accent'])
    draw.rectangle([42, 195, 48, 220], fill=PALETTE['shadow'])

    # Right mirror
    draw.rectangle([210, 100, 260, 320], fill=PALETTE['shadow'], outline=PALETTE['secondary'], width=2)
    # Reflection - small figure
    draw.ellipse([230, 180, 240, 195], fill=PALETTE['accent'])
    draw.rectangle([232, 195, 238, 220], fill=PALETTE['shadow'])

    # Central figure examining themselves
    fig_x, fig_y = WIDTH // 2, HEIGHT // 2 + 40

    # Head looking at mirrors
    draw.ellipse([fig_x - 14, fig_y - 70, fig_x + 14, fig_y - 46], fill=PALETTE['accent'])

    # Body in contemplative pose
    body = [
        (fig_x, fig_y - 46),
        (fig_x - 24, fig_y - 25),
        (fig_x - 24, fig_y + 30),
        (fig_x + 24, fig_y + 30),
        (fig_x + 24, fig_y - 25)
    ]
    draw.polygon(body, fill=PALETTE['primary'])

    # Hand to chin - thinking
    draw.ellipse([fig_x + 20, fig_y - 35, fig_x + 28, fig_y - 27], fill=PALETTE['primary'])


def draw_dance_7_eight(img, draw):
    """
    Eight of Dance: dance in full motion, choreography executed, I dance like this
    Content: Dancers in active transformation, choreography fully deployed

    Visual: Eight figures in dynamic motion, full choreography
    """
    # Radial gradient - maximum energy
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 180, PALETTE['heat'], PALETTE['shadow'])

    # Eight figures in full choreography
    positions = [
        (60, 140), (140, 120), (220, 140),  # Top row
        (50, 230), (230, 230),  # Middle sides
        (80, 320), (140, 340), (200, 320)  # Bottom row
    ]

    for i, (x, y) in enumerate(positions):
        # Head
        draw.ellipse([x - 9, y - 35, x + 9, y - 17], fill=PALETTE['accent'])

        # Body in dynamic pose
        body = [
            (x, y - 17),
            (x - 16, y - 5),
            (x - 14, y + 22),
            (x + 14, y + 22),
            (x + 16, y - 5)
        ]
        color = PALETTE['primary'] if i % 3 == 0 else (PALETTE['secondary'] if i % 3 == 1 else PALETTE['accent'])
        draw.polygon(body, fill=color)

        # Arms in motion
        if i % 2 == 0:
            draw.line([(x - 16, y), (x - 30, y - 10)], fill=color, width=5)
            draw.line([(x + 16, y), (x + 30, y + 10)], fill=color, width=5)

    # Heat waves showing energy
    for i in range(8):
        y = 60 + i * 35
        for x in range(0, WIDTH, 25):
            offset = 10 * math.sin((x + y) / 12)
            draw.line([(x + offset, y), (x + 20 + offset, y)],
                     fill=PALETTE['electric'], width=1)


def draw_dance_8_nine(img, draw):
    """
    Nine of Dance: dance fulfilled, choreography abundant, movement richness
    Content: Nine dancers in complex harmony, abundant choreography

    Visual: Nine figures in beautiful formation, movement fully realized
    """
    # Radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2 + 20, 190, PALETTE['heat'], PALETTE['shadow'])

    # Nine figures in 3x3 grid formation, each with unique pose
    for row in range(3):
        for col in range(3):
            x = 60 + col * 80
            y = 120 + row * 100

            # Head
            draw.ellipse([x - 8, y - 30, x + 8, y - 14], fill=PALETTE['accent'])

            # Body - each with slightly different pose
            body = [
                (x, y - 14),
                (x - 14, y),
                (x - 12, y + 20),
                (x + 12, y + 20),
                (x + 14, y)
            ]
            color = [PALETTE['primary'], PALETTE['secondary'], PALETTE['accent']][(row + col) % 3]
            draw.polygon(body, fill=color)

            # Varied arm positions
            pose = (row * 3 + col) % 4
            if pose == 0:  # Arms up
                draw.line([(x, y - 5), (x - 18, y - 15)], fill=color, width=4)
                draw.line([(x, y - 5), (x + 18, y - 15)], fill=color, width=4)
            elif pose == 1:  # Arms out
                draw.line([(x - 14, y), (x - 25, y)], fill=color, width=4)
                draw.line([(x + 14, y), (x + 25, y)], fill=color, width=4)
            elif pose == 2:  # One arm up
                draw.line([(x, y - 5), (x + 18, y - 15)], fill=color, width=4)


def draw_dance_9_ten(img, draw):
    """
    Ten of Dance: dance at overflow, movement beyond limit, everybody's dancing, the finale
    Content: Ten dancers filling all space, choreography at maximum, American Utopia finale energy

    Visual: Maximum energy - dancers everywhere, the finale moment
    """
    # Maximum radial gradient - FULL ENERGY
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 200, PALETTE['heat'], PALETTE['shadow'])

    # Ten dancers filling every available space
    positions = [
        (50, 90), (140, 80), (230, 90),  # Top
        (40, 180), (100, 170), (180, 170), (240, 180),  # Middle
        (70, 280), (140, 290), (210, 280)  # Bottom
    ]

    for i, (x, y) in enumerate(positions):
        # Head
        draw.ellipse([x - 8, y - 28, x + 8, y - 12], fill=PALETTE['accent'])

        # Body - all in motion
        body = [
            (x, y - 12),
            (x - 12, y),
            (x - 10, y + 18),
            (x + 10, y + 18),
            (x + 12, y)
        ]
        colors = [PALETTE['primary'], PALETTE['secondary'], PALETTE['accent']]
        draw.polygon(body, fill=colors[i % 3])

        # Everyone's arms are UP - finale gesture
        draw.line([(x, y - 5), (x - 15, y - 18)], fill=colors[i % 3], width=4)
        draw.line([(x, y - 5), (x + 15, y - 18)], fill=colors[i % 3], width=4)

    # MAXIMUM heat waves - the finale energy
    for i in range(15):
        y = 40 + i * 25
        for x in range(0, WIDTH, 20):
            offset = 15 * math.sin((x + y) / 10)
            draw.line([(x + offset, y), (x + 15 + offset, y)],
                     fill=PALETTE['electric'], width=2)

    # Radiating lines from center - explosive energy
    for angle in range(0, 360, 30):
        rad = angle * math.pi / 180
        length = 60
        end_x = WIDTH//2 + int(length * math.cos(rad))
        end_y = HEIGHT//2 + int(length * math.sin(rad))
        draw.line([(WIDTH//2, HEIGHT//2), (end_x, end_y)],
                 fill=PALETTE['electric'], width=2)


def draw_dance_10_observer(img, draw):
    """
    Observer of Dance: watching the dance, documenting movement, audience member
    Content: Figure watching dancers, documenting choreography

    Visual: Figure seated watching others dance on stage
    """
    # Radial gradient (stage area)
    bvt.radial_gradient(draw, WIDTH//2 + 40, 200, 120, PALETTE['heat'], PALETTE['shadow'])

    # Stage in background with dancers
    stage_floor = [(140, 240), (260, 240), (250, 270), (150, 270)]
    draw.polygon(stage_floor, fill=PALETTE['shadow'])

    # Three dancers on stage (small)
    for x in [170, 200, 230]:
        # Head
        draw.ellipse([x - 6, 190, x + 6, 202], fill=PALETTE['accent'])
        # Body
        draw.rectangle([x - 5, 202, x + 5, 230], fill=PALETTE['secondary'])
        # Arms up (dancing)
        draw.line([(x, 210), (x - 10, 200)], fill=PALETTE['secondary'], width=3)
        draw.line([(x, 210), (x + 10, 200)], fill=PALETTE['secondary'], width=3)

    # THE OBSERVER - seated in foreground
    obs_x, obs_y = 70, 300

    # Head
    draw.ellipse([obs_x - 14, obs_y, obs_x + 14, obs_y + 28], fill=PALETTE['accent'])

    # Body seated
    body = [
        (obs_x, obs_y + 28),
        (obs_x - 24, obs_y + 45),
        (obs_x - 24, obs_y + 90),
        (obs_x + 24, obs_y + 90),
        (obs_x + 24, obs_y + 45)
    ]
    draw.polygon(body, fill=PALETTE['primary'])

    # Notebook
    draw.rectangle([obs_x - 18, obs_y + 55, obs_x + 8, obs_y + 80],
                   fill=PALETTE['shadow'], outline=PALETTE['shadow'], width=2)
    # Lines on notebook
    for line_y in [obs_y + 62, obs_y + 69, obs_y + 76]:
        draw.line([(obs_x - 14, line_y), (obs_x + 4, line_y)], fill=PALETTE['shadow'], width=1)

    # Pencil
    draw.line([(obs_x + 8, obs_y + 68), (obs_x + 20, obs_y + 63)],
             fill=PALETTE['shadow'], width=3)


def draw_dance_11_pretender(img, draw):
    """
    Pretender of Dance: performing movement, theatrical dance, acting like you're dancing
    Content: Figure in oversized suit making dramatic dance moves, theatrical performance

    Visual: Big suit figure with exaggerated dance gesture
    """
    # Radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 150, PALETTE['heat'], PALETTE['shadow'])

    # Stage lights
    for x in [60, 140, 220]:
        # Spotlight beam
        beam_points = [(x, 40), (x - 30, HEIGHT - 100), (x + 30, HEIGHT - 100)]
        draw.polygon(beam_points, fill=PALETTE['electric'], outline=None)
        # Light source
        draw.ellipse([x - 10, 30, x + 10, 50], fill=PALETTE['accent'])

    # THE PRETENDER - oversized suit with dramatic gesture
    fig_x, fig_y = 140, 180

    # Small head
    draw.ellipse([fig_x - 11, fig_y, fig_x + 11, fig_y + 22], fill=PALETTE['accent'])

    # HUGE theatrical suit/costume
    suit = [
        (fig_x, fig_y + 22),
        (fig_x - 65, fig_y + 50),
        (fig_x - 62, fig_y + 120),
        (fig_x - 50, fig_y + 220),
        (fig_x - 18, fig_y + 300),
        (fig_x + 18, fig_y + 300),
        (fig_x + 50, fig_y + 220),
        (fig_x + 62, fig_y + 120),
        (fig_x + 65, fig_y + 50)
    ]
    draw.polygon(suit, fill=PALETTE['primary'])

    # Exaggerated dance pose - one arm WAY up
    arm_up = [
        (fig_x - 65, fig_y + 70),
        (fig_x - 90, fig_y - 10),
        (fig_x - 85, fig_y - 5),
        (fig_x - 60, fig_y + 75)
    ]
    draw.polygon(arm_up, fill=PALETTE['primary'])

    # Other arm out
    arm_out = [
        (fig_x + 65, fig_y + 80),
        (fig_x + 110, fig_y + 85),
        (fig_x + 112, fig_y + 92),
        (fig_x + 67, fig_y + 87)
    ]
    draw.polygon(arm_out, fill=PALETTE['primary'])

    # Motion lines showing the theatrical movement
    for offset in [5, 15, 25]:
        draw.line([(fig_x - 90 - offset, fig_y - 10), (fig_x - 90 - offset - 8, fig_y - 10)],
                 fill=PALETTE['electric'], width=2)


def draw_dance_12_exile(img, draw):
    """
    Exile of Dance: dancing alone, movement in isolation, rhythm without community
    Content: Solitary figure dancing in empty space, isolated movement

    Visual: Single figure dancing in vast empty space
    """
    # Muted gradient - still has energy but isolated
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2 + 40, 100, PALETTE['heat'], PALETTE['shadow'])

    # Empty space emphasized - just horizon line
    draw.line([(0, 290), (WIDTH, 290)], fill=PALETTE['shadow'], width=2)

    # THE EXILE - dancing alone
    fig_x, fig_y = WIDTH // 2, HEIGHT // 2 + 60

    # Head
    draw.ellipse([fig_x - 14, fig_y - 70, fig_x + 14, fig_y - 42], fill=PALETTE['accent'])

    # Body in dance pose
    body = [
        (fig_x, fig_y - 42),
        (fig_x - 26, fig_y - 20),
        (fig_x - 24, fig_y + 30),
        (fig_x + 24, fig_y + 30),
        (fig_x + 26, fig_y - 20)
    ]
    draw.polygon(body, fill=PALETTE['primary'])

    # Arms in dance position - but no one to dance with
    draw.line([(fig_x - 26, fig_y - 10), (fig_x - 50, fig_y - 25)],
             fill=PALETTE['primary'], width=8)
    draw.line([(fig_x + 26, fig_y - 10), (fig_x + 50, fig_y)],
             fill=PALETTE['primary'], width=8)

    # Small energy lines - showing movement but isolated
    for angle in [-30, 0, 30]:
        rad = angle * math.pi / 180
        length = 35
        end_x = fig_x + int(length * math.cos(rad))
        end_y = fig_y - 40 - int(length * math.sin(rad))
        draw.line([(fig_x, fig_y - 40), (end_x, end_y)],
                 fill=PALETTE['electric'], width=1)

    # Shadow beneath - emphasizing solitude
    draw.ellipse([fig_x - 30, fig_y + 30, fig_x + 30, fig_y + 40],
                fill=PALETTE['shadow'])


def draw_dance_13_giant(img, draw):
    """
    Giant of Dance: authentic movement power, choreographing with others, dancing together
    Content: Figure at full height dancing with others visible, collaborative choreography

    Visual: Large central figure dancing with community around them
    """
    # Maximum radial gradient
    bvt.radial_gradient(draw, WIDTH//2, HEIGHT//2, 180, PALETTE['heat'], PALETTE['shadow'])

    # Other dancers in background/around
    other_positions = [
        (60, 300), (220, 300), (50, 200), (230, 200)
    ]

    for x, y in other_positions:
        # Head
        draw.ellipse([x - 8, y - 30, x + 8, y - 14], fill=PALETTE['accent'])
        # Body
        body = [
            (x, y - 14),
            (x - 14, y),
            (x - 12, y + 25),
            (x + 12, y + 25),
            (x + 14, y)
        ]
        draw.polygon(body, fill=PALETTE['secondary'])
        # Arms dancing
        draw.line([(x, y - 5), (x - 15, y - 12)], fill=PALETTE['secondary'], width=4)
        draw.line([(x, y - 5), (x + 15, y - 12)], fill=PALETTE['secondary'], width=4)

    # THE GIANT - tall figure in center, dancing at full height
    fig_x, fig_y = WIDTH // 2, 120

    # Head proportional
    draw.ellipse([fig_x - 15, fig_y, fig_x + 15, fig_y + 30], fill=PALETTE['accent'])

    # Body upright, in motion
    body = [
        (fig_x, fig_y + 30),
        (fig_x - 32, fig_y + 58),
        (fig_x - 35, fig_y + 140),
        (fig_x - 32, fig_y + 210),
        (fig_x - 14, fig_y + 300),
        (fig_x + 14, fig_y + 300),
        (fig_x + 32, fig_y + 210),
        (fig_x + 35, fig_y + 140),
        (fig_x + 32, fig_y + 58)
    ]
    draw.polygon(body, fill=PALETTE['primary'])

    # Arms in joyful dance motion
    # Left arm up and out
    left_arm = [
        (fig_x - 32, fig_y + 75),
        (fig_x - 70, fig_y + 50),
        (fig_x - 72, fig_y + 58),
        (fig_x - 34, fig_y + 83)
    ]
    draw.polygon(left_arm, fill=PALETTE['primary'])

    # Right arm up and out
    right_arm = [
        (fig_x + 32, fig_y + 75),
        (fig_x + 70, fig_y + 50),
        (fig_x + 72, fig_y + 58),
        (fig_x + 34, fig_y + 83)
    ]
    draw.polygon(right_arm, fill=PALETTE['primary'])

    # Energy radiating from the Giant - inspiring the community dance
    for angle in range(0, 360, 45):
        rad = angle * math.pi / 180
        length = 50
        start_x = fig_x + int(30 * math.cos(rad))
        start_y = fig_y + 140 + int(30 * math.sin(rad))
        end_x = fig_x + int((30 + length) * math.cos(rad))
        end_y = fig_y + 140 + int((30 + length) * math.sin(rad))
        draw.line([(start_x, start_y), (end_x, end_y)],
                 fill=PALETTE['electric'], width=2)


# Main generation function
def generate_card(rank):
    """Generate a specific Dance card by rank (0-13)"""
    img = bvt.create_canvas(PALETTE['shadow'])
    draw = ImageDraw.Draw(img)

    # Draw the specific card
    card_functions = [
        draw_dance_0_ace,
        draw_dance_1_two,
        draw_dance_2_three,
        draw_dance_3_four,
        draw_dance_4_five,
        draw_dance_5_six,
        draw_dance_6_seven,
        draw_dance_7_eight,
        draw_dance_8_nine,
        draw_dance_9_ten,
        draw_dance_10_observer,
        draw_dance_11_pretender,
        draw_dance_12_exile,
        draw_dance_13_giant,
    ]

    if 0 <= rank <= 13:
        card_functions[rank](img, draw)

    return img


def main():
    """Generate all 14 Dance cards with custom pixel art"""
    print("Generating custom Dance suit cards...\n")

    output_dir = '/home/user/claude_skills/tarot/decks/byrne/cards'
    os.makedirs(output_dir, exist_ok=True)

    card_names = [
        "Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
        "Eight", "Nine", "Ten", "Observer", "Pretender", "Exile", "Giant"
    ]

    for rank in range(14):
        print(f"  [{rank + 1}/14] {card_names[rank]} of Dance...")
        img = generate_card(rank)
        output_path = os.path.join(output_dir, f'dance-{rank:02d}.png')
        img.save(output_path)

    print(f"\n✓ All 14 Dance cards generated!")
    print(f"  Location: {output_dir}/dance-*.png")


if __name__ == '__main__':
    main()
