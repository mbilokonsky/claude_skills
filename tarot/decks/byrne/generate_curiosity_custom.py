#!/usr/bin/env python3
"""
Custom pixel art generation for the Curiosity suit
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
PALETTE = bvt.SuitColors.CURIOSITY


def draw_question_mark(draw, x, y, size, color, width=3):
    """Helper to draw a question mark"""
    # Arc for the hook
    arc_size = size * 0.6
    draw.arc([x - arc_size//2, y, x + arc_size//2, y + arc_size],
             180, 360, fill=color, width=width)

    # Vertical stem
    stem_start_y = y + arc_size * 0.7
    stem_end_y = y + arc_size * 1.1
    draw.line([(x, stem_start_y), (x, stem_end_y)], fill=color, width=width)

    # Dot
    dot_y = y + arc_size * 1.3
    dot_size = size // 8
    draw.ellipse([x - dot_size, dot_y - dot_size, x + dot_size, dot_y + dot_size], fill=color)


def draw_curiosity_0_ace(img, draw):
    """
    Ace of Curiosity: the first question, pure inquiry spark
    Content: A single question mark glowing, the first wonder

    Visual: One large radiant question mark in the center
    """
    # Gradient background - bright to slightly darker
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Large central question mark
    draw_question_mark(draw, WIDTH//2, HEIGHT//2 - 40, 120, PALETTE['text'], width=12)

    # Subtle glow circles around it
    for radius in [70, 85, 100]:
        draw.ellipse([WIDTH//2 - radius, HEIGHT//2 - radius,
                     WIDTH//2 + radius, HEIGHT//2 + radius],
                    outline=PALETTE['accent'], width=1)


def draw_curiosity_1_two(img, draw):
    """
    Two of Curiosity: dialogue begins, mutual inquiry, questions in conversation
    Content: Two question marks facing each other, speech bubbles interweaving

    Visual: Two question marks with connecting dialogue lines
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Two question marks facing each other
    left_x = WIDTH // 3
    right_x = 2 * WIDTH // 3
    center_y = HEIGHT // 2

    draw_question_mark(draw, left_x, center_y - 30, 80, PALETTE['accent'], width=8)
    draw_question_mark(draw, right_x, center_y - 30, 80, PALETTE['text'], width=8)

    # Dialogue connection lines (speech bubble shapes)
    # Left bubble
    bubble1 = [
        (left_x + 30, center_y - 20),
        (left_x + 80, center_y - 10),
        (left_x + 75, center_y + 20),
        (left_x + 40, center_y + 10)
    ]
    draw.polygon(bubble1, outline=PALETTE['dialogue'], width=2)

    # Right bubble
    bubble2 = [
        (right_x - 30, center_y + 10),
        (right_x - 80, center_y + 20),
        (right_x - 75, center_y + 50),
        (right_x - 40, center_y + 40)
    ]
    draw.polygon(bubble2, outline=PALETTE['dialogue'], width=2)

    # Connecting line showing conversation
    draw.line([(left_x + 60, center_y), (right_x - 60, center_y + 30)],
             fill=PALETTE['text'], width=2)


def draw_curiosity_2_three(img, draw):
    """
    Three of Curiosity: inquiry developing, questions multiplying productively
    Content: Three figures or three question marks forming investigation

    Visual: Three question marks in triangular arrangement, forming collaborative space
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Three question marks in triangle
    top_x, top_y = WIDTH // 2, 120
    left_x, left_y = WIDTH // 3, 280
    right_x, right_y = 2 * WIDTH // 3, 280

    draw_question_mark(draw, top_x, top_y, 70, PALETTE['accent'], width=7)
    draw_question_mark(draw, left_x, left_y, 70, PALETTE['text'], width=7)
    draw_question_mark(draw, right_x, right_y, 70, PALETTE['dialogue'], width=7)

    # Connecting lines forming investigation triangle
    draw.line([(top_x, top_y + 60), (left_x, left_y + 20)], fill=PALETTE['text'], width=2)
    draw.line([(top_x, top_y + 60), (right_x, right_y + 20)], fill=PALETTE['text'], width=2)
    draw.line([(left_x, left_y + 50), (right_x, right_y + 50)], fill=PALETTE['text'], width=2)


def draw_curiosity_3_four(img, draw):
    """
    Four of Curiosity: inquiry framework stable, questions organized, civic structure formed
    Content: Four corners of a public forum, organized inquiry space

    Visual: Four pillars or corners defining a civic space
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Four corners/pillars defining civic space
    margin = 50
    pillar_width = 30
    pillar_height = 140

    # Top-left pillar
    draw.rectangle([margin, 100, margin + pillar_width, 100 + pillar_height],
                   fill=PALETTE['accent'])
    draw_question_mark(draw, margin + pillar_width//2, 110, 40, PALETTE['primary'], width=4)

    # Top-right pillar
    draw.rectangle([WIDTH - margin - pillar_width, 100,
                   WIDTH - margin, 100 + pillar_height],
                   fill=PALETTE['accent'])
    draw_question_mark(draw, WIDTH - margin - pillar_width//2, 110, 40, PALETTE['primary'], width=4)

    # Bottom-left pillar
    draw.rectangle([margin, 280, margin + pillar_width, 280 + pillar_height],
                   fill=PALETTE['accent'])
    draw_question_mark(draw, margin + pillar_width//2, 290, 40, PALETTE['primary'], width=4)

    # Bottom-right pillar
    draw.rectangle([WIDTH - margin - pillar_width, 280,
                   WIDTH - margin, 280 + pillar_height],
                   fill=PALETTE['accent'])
    draw_question_mark(draw, WIDTH - margin - pillar_width//2, 290, 40, PALETTE['primary'], width=4)

    # Floor/platform in the center
    platform = [
        (margin + pillar_width, 260),
        (WIDTH - margin - pillar_width, 260),
        (WIDTH - margin - pillar_width - 10, 300),
        (margin + pillar_width + 10, 300)
    ]
    draw.polygon(platform, fill=PALETTE['dialogue'], outline=PALETTE['text'], width=2)


def draw_curiosity_4_five(img, draw):
    """
    Five of Curiosity: inquiry challenged, hard questions arrive
    Content: Question marks clashing, difficult inquiry

    Visual: Question marks in tension, conflicting angles
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Five question marks in tension
    positions = [
        (70, 150),
        (210, 150),
        (140, 220),
        (90, 310),
        (190, 310)
    ]

    for i, (x, y) in enumerate(positions):
        draw_question_mark(draw, x, y, 60, PALETTE['text'], width=6)

    # Tension lines crossing between them
    draw.line([(70, 200), (210, 200)], fill=PALETTE['shadow'], width=3)
    draw.line([(140, 150), (140, 320)], fill=PALETTE['shadow'], width=3)
    draw.line([(80, 170), (200, 330)], fill=PALETTE['shadow'], width=2)
    draw.line([(200, 170), (80, 330)], fill=PALETTE['shadow'], width=2)


def draw_curiosity_5_six(img, draw):
    """
    Six of Curiosity: dialogue restored, inquiry finding new ground
    Content: Question marks in new arrangement, conversation restored with more depth

    Visual: Six question marks in balanced hexagonal arrangement
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Six question marks in hexagonal arrangement
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    radius = 90

    for i in range(6):
        angle = (i * 60 - 90) * math.pi / 180
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))

        draw_question_mark(draw, x, y, 55, PALETTE['accent'], width=5)

    # Connecting lines showing restored dialogue
    for i in range(6):
        angle1 = (i * 60 - 90) * math.pi / 180
        angle2 = ((i + 1) * 60 - 90) * math.pi / 180
        x1 = center_x + int(radius * math.cos(angle1))
        y1 = center_y + int(radius * math.sin(angle1))
        x2 = center_x + int(radius * math.cos(angle2))
        y2 = center_y + int(radius * math.sin(angle2))
        draw.line([(x1, y1 + 40), (x2, y2 + 40)], fill=PALETTE['dialogue'], width=1)


def draw_curiosity_6_seven(img, draw):
    """
    Seven of Curiosity: examining the questions, meta-inquiry, wondering about wondering
    Content: A figure examining multiple questions, inquiry paths mapped out

    Visual: Figure surrounded by question marks, contemplating which path to follow
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Figure in center
    fig_x, fig_y = WIDTH // 2, HEIGHT // 2 + 40

    # Head
    draw.ellipse([fig_x - 18, fig_y - 80, fig_x + 18, fig_y - 44], fill=PALETTE['accent'])

    # Body
    body_points = [
        (fig_x, fig_y - 44),
        (fig_x - 30, fig_y - 20),
        (fig_x - 30, fig_y + 40),
        (fig_x + 30, fig_y + 40),
        (fig_x + 30, fig_y - 20)
    ]
    draw.polygon(body_points, fill=PALETTE['text'])

    # Seven question marks around the figure
    positions = [
        (fig_x - 80, fig_y - 120), (fig_x, fig_y - 140), (fig_x + 80, fig_y - 120),
        (fig_x - 100, fig_y - 20), (fig_x + 100, fig_y - 20),
        (fig_x - 70, fig_y + 80), (fig_x + 70, fig_y + 80)
    ]

    for x, y in positions:
        draw_question_mark(draw, x, y, 45, PALETTE['dialogue'], width=4)

    # Lines connecting figure to questions (examining them)
    for x, y in positions[:4]:
        draw.line([(fig_x, fig_y - 20), (x, y + 30)], fill=PALETTE['shadow'], width=1)


def draw_curiosity_7_eight(img, draw):
    """
    Eight of Curiosity: inquiry in action, questions implemented, doing the right thing
    Content: Questions actively being investigated, inquiry transforming reality

    Visual: Question marks becoming actions, transformation in progress
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Eight question marks transforming into action symbols
    # Left side: questions
    for i, y in enumerate([100, 170, 240, 310]):
        draw_question_mark(draw, 60, y, 50, PALETTE['text'], width=5)

        # Arrow pointing right (transformation)
        arrow_y = y + 25
        draw.line([(100, arrow_y), (150, arrow_y)], fill=PALETTE['accent'], width=3)
        draw.polygon([(150, arrow_y), (140, arrow_y - 6), (140, arrow_y + 6)],
                    fill=PALETTE['accent'])

    # Right side: actions (exclamation marks - rotated question marks essentially)
    for i, y in enumerate([100, 170, 240, 310]):
        x = 220
        # Exclamation: vertical line + dot
        draw.line([(x, y), (x, y + 40)], fill=PALETTE['dialogue'], width=6)
        draw.ellipse([x - 6, y + 48, x + 6, y + 60], fill=PALETTE['dialogue'])


def draw_curiosity_8_nine(img, draw):
    """
    Nine of Curiosity: rich inquiry, deep investigation fulfilled, collaborative intelligence
    Content: Nine question marks in beautiful conversation, abundant investigation

    Visual: Nine question marks in harmonious arrangement, dialogue flowing
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Nine question marks in 3x3 grid, but with connecting dialogue
    for row in range(3):
        for col in range(3):
            x = 50 + col * 90
            y = 90 + row * 110

            color = [PALETTE['accent'], PALETTE['text'], PALETTE['dialogue']][(row + col) % 3]
            draw_question_mark(draw, x, y, 50, color, width=5)

    # Dialogue lines connecting them
    # Horizontal connections
    for row in range(3):
        y = 120 + row * 110
        draw.line([(80, y), (200, y)], fill=PALETTE['shadow'], width=1)

    # Vertical connections
    for col in range(3):
        x = 50 + col * 90
        draw.line([(x, 140), (x, 330)], fill=PALETTE['shadow'], width=1)


def draw_curiosity_9_ten(img, draw):
    """
    Ten of Curiosity: inquiry at overflow, questions exhausted or exhausting
    Content: Ten question marks filling all space, inquiry at maximum

    Visual: Too many questions, overwhelming inquiry
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Ten question marks overlapping, crowding the space
    positions = [
        (50, 80), (140, 70), (220, 90),
        (60, 170), (180, 160),
        (100, 250), (200, 240),
        (70, 330), (150, 340), (230, 320)
    ]

    sizes = [60, 55, 58, 62, 54, 61, 57, 59, 56, 60]

    for (x, y), size in zip(positions, sizes):
        draw_question_mark(draw, x, y, size, PALETTE['text'], width=5)

    # Overlapping lines showing the overwhelming nature
    for i in range(len(positions)):
        for j in range(i + 1, min(i + 3, len(positions))):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            draw.line([(x1, y1 + 40), (x2, y2 + 40)], fill=PALETTE['shadow'], width=1)


def draw_curiosity_10_observer(img, draw):
    """
    Observer of Curiosity: watching others ask, documenting inquiry, studying questions from outside
    Content: Figure watching town hall meeting, documenting others' questions

    Visual: Figure with notebook watching others in dialogue
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Background: other people in dialogue (small figures with question marks)
    # Three groups having conversations
    for group_x in [180, 220]:
        # Small figures
        draw.ellipse([group_x - 8, 140, group_x + 8, 156], fill=PALETTE['dialogue'])
        draw.rectangle([group_x - 6, 156, group_x + 6, 180], fill=PALETTE['shadow'])
        # Question mark above them
        draw_question_mark(draw, group_x, 110, 35, PALETTE['text'], width=3)

    # More figures lower
    for group_x in [160, 200, 240]:
        draw.ellipse([group_x - 6, 240, group_x + 6, 252], fill=PALETTE['dialogue'])
        draw.rectangle([group_x - 5, 252, group_x + 5, 272], fill=PALETTE['shadow'])

    # THE OBSERVER - figure in foreground with notebook
    obs_x, obs_y = 70, 280

    # Head
    draw.ellipse([obs_x - 16, obs_y, obs_x + 16, obs_y + 32], fill=PALETTE['accent'])

    # Body
    body_points = [
        (obs_x, obs_y + 32),
        (obs_x - 28, obs_y + 55),
        (obs_x - 28, obs_y + 120),
        (obs_x + 28, obs_y + 120),
        (obs_x + 28, obs_y + 55)
    ]
    draw.polygon(body_points, fill=PALETTE['text'])

    # Notebook
    draw.rectangle([obs_x - 20, obs_y + 70, obs_x + 5, obs_y + 100],
                   fill=PALETTE['primary'], outline=PALETTE['shadow'], width=2)
    # Lines on notebook
    for line_y in [obs_y + 77, obs_y + 84, obs_y + 91]:
        draw.line([(obs_x - 16, line_y), (obs_x + 1, line_y)], fill=PALETTE['shadow'], width=1)

    # Pencil
    draw.line([(obs_x + 5, obs_y + 85), (obs_x + 18, obs_y + 80)],
             fill=PALETTE['shadow'], width=3)


def draw_curiosity_11_pretender(img, draw):
    """
    Pretender of Curiosity: performing inquiry, theatrical questioning
    Content: Figure making grand questioning gestures, dramatic presentation

    Visual: Big suit figure with theatrical questioning gesture
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Theatrical question marks in background
    for x, y in [(60, 80), (220, 100), (190, 280)]:
        draw_question_mark(draw, x, y, 45, PALETTE['dialogue'], width=4)

    # THE PRETENDER - big suit with dramatic gesture
    fig_x, fig_y = 140, 150

    # Small head
    draw.ellipse([fig_x - 12, fig_y, fig_x + 12, fig_y + 24], fill=PALETTE['accent'])

    # HUGE theatrical suit
    suit_points = [
        (fig_x, fig_y + 24),
        (fig_x - 70, fig_y + 55),
        (fig_x - 68, fig_y + 130),
        (fig_x - 55, fig_y + 230),
        (fig_x - 20, fig_y + 310),
        (fig_x + 20, fig_y + 310),
        (fig_x + 55, fig_y + 230),
        (fig_x + 68, fig_y + 130),
        (fig_x + 70, fig_y + 55)
    ]
    draw.polygon(suit_points, fill=PALETTE['text'])

    # Arm in grand gesture holding giant question mark
    arm_points = [
        (fig_x + 70, fig_y + 80),
        (fig_x + 110, fig_y + 50),
        (fig_x + 115, fig_y + 60),
        (fig_x + 75, fig_y + 90)
    ]
    draw.polygon(arm_points, fill=PALETTE['text'])

    # Giant question mark being held
    draw_question_mark(draw, fig_x + 130, fig_y + 30, 70, PALETTE['accent'], width=8)


def draw_curiosity_12_exile(img, draw):
    """
    Exile of Curiosity: alone with hard questions, inquiry in isolation
    Content: Solitary figure with question marks in empty space, isolated inquiry

    Visual: Lone figure surrounded by unanswered questions
    """
    # Background gradient - more subdued
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Isolated question marks floating around - unanswered
    positions = [
        (60, 100), (210, 120), (100, 180), (200, 200), (80, 280), (220, 300)
    ]

    for x, y in positions:
        draw_question_mark(draw, x, y, 40, PALETTE['shadow'], width=4)

    # THE EXILE - figure hunched in center
    fig_x, fig_y = WIDTH // 2, HEIGHT // 2 + 40

    # Head bowed
    draw.ellipse([fig_x - 16, fig_y - 60, fig_x + 16, fig_y - 28], fill=PALETTE['accent'])

    # Body hunched
    body_points = [
        (fig_x, fig_y - 28),
        (fig_x - 32, fig_y - 10),
        (fig_x - 35, fig_y + 40),
        (fig_x + 35, fig_y + 40),
        (fig_x + 32, fig_y - 10)
    ]
    draw.polygon(body_points, fill=PALETTE['text'])

    # Arms wrapped around self
    # Left arm
    draw.line([(fig_x - 32, fig_y), (fig_x - 10, fig_y + 20)],
             fill=PALETTE['text'], width=8)
    # Right arm
    draw.line([(fig_x + 32, fig_y), (fig_x + 10, fig_y + 20)],
             fill=PALETTE['text'], width=8)


def draw_curiosity_13_giant(img, draw):
    """
    Giant of Curiosity: authentic inquiry leadership, convening questions
    Content: Figure at full height facilitating dialogue with others visible

    Visual: Tall figure with arms open, facilitating conversation between others
    """
    # Background gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(PALETTE['secondary'][0] + (PALETTE['primary'][0] - PALETTE['secondary'][0]) * t)
        g = int(PALETTE['secondary'][1] + (PALETTE['primary'][1] - PALETTE['secondary'][1]) * t)
        b = int(PALETTE['secondary'][2] + (PALETTE['primary'][2] - PALETTE['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Other figures with question marks (the community)
    # Left figure
    draw.ellipse([55, 300, 70, 315], fill=PALETTE['dialogue'])
    draw.rectangle([57, 315, 68, 345], fill=PALETTE['shadow'])
    draw_question_mark(draw, 62, 260, 40, PALETTE['accent'], width=4)

    # Right figure
    draw.ellipse([210, 310, 225, 325], fill=PALETTE['dialogue'])
    draw.rectangle([212, 325, 223, 355], fill=PALETTE['shadow'])
    draw_question_mark(draw, 217, 270, 40, PALETTE['accent'], width=4)

    # Center-left figure
    draw.ellipse([100, 340, 115, 355], fill=PALETTE['dialogue'])
    draw.rectangle([102, 355, 113, 385], fill=PALETTE['shadow'])

    # Center-right figure
    draw.ellipse([165, 340, 180, 355], fill=PALETTE['dialogue'])
    draw.rectangle([167, 355, 178, 385], fill=PALETTE['shadow'])

    # THE GIANT - tall facilitating figure
    fig_x, fig_y = WIDTH // 2, 150

    # Head proportional
    draw.ellipse([fig_x - 16, fig_y, fig_x + 16, fig_y + 32], fill=PALETTE['accent'])

    # Body upright, facilitating
    body_points = [
        (fig_x, fig_y + 32),
        (fig_x - 35, fig_y + 60),
        (fig_x - 38, fig_y + 140),
        (fig_x - 35, fig_y + 210),
        (fig_x - 15, fig_y + 310),
        (fig_x + 15, fig_y + 310),
        (fig_x + 35, fig_y + 210),
        (fig_x + 38, fig_y + 140),
        (fig_x + 35, fig_y + 60)
    ]
    draw.polygon(body_points, fill=PALETTE['text'])

    # Arms outstretched, facilitating/inviting
    # Left arm reaching toward left figure
    left_arm = [
        (fig_x - 35, fig_y + 80),
        (fig_x - 75, fig_y + 110),
        (fig_x - 78, fig_y + 120),
        (fig_x - 38, fig_y + 90)
    ]
    draw.polygon(left_arm, fill=PALETTE['text'])

    # Right arm reaching toward right figure
    right_arm = [
        (fig_x + 35, fig_y + 80),
        (fig_x + 75, fig_y + 110),
        (fig_x + 78, fig_y + 120),
        (fig_x + 38, fig_y + 90)
    ]
    draw.polygon(right_arm, fill=PALETTE['text'])

    # Large question mark above - the shared inquiry
    draw_question_mark(draw, fig_x, 60, 60, PALETTE['dialogue'], width=6)


# Main generation function
def generate_card(rank):
    """Generate a specific Curiosity card by rank (0-13)"""
    img = Image.new('RGB', (WIDTH, HEIGHT), PALETTE['primary'])
    draw = ImageDraw.Draw(img)

    # Draw the specific card
    card_functions = [
        draw_curiosity_0_ace,
        draw_curiosity_1_two,
        draw_curiosity_2_three,
        draw_curiosity_3_four,
        draw_curiosity_4_five,
        draw_curiosity_5_six,
        draw_curiosity_6_seven,
        draw_curiosity_7_eight,
        draw_curiosity_8_nine,
        draw_curiosity_9_ten,
        draw_curiosity_10_observer,
        draw_curiosity_11_pretender,
        draw_curiosity_12_exile,
        draw_curiosity_13_giant,
    ]

    if 0 <= rank <= 13:
        card_functions[rank](img, draw)

    return img


def main():
    """Generate all 14 Curiosity cards with custom pixel art"""
    print("Generating custom Curiosity suit cards...\n")

    output_dir = '/home/user/claude_skills/tarot/decks/byrne/cards'
    os.makedirs(output_dir, exist_ok=True)

    card_names = [
        "Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
        "Eight", "Nine", "Ten", "Observer", "Pretender", "Exile", "Giant"
    ]

    for rank in range(14):
        print(f"  [{rank + 1}/14] {card_names[rank]} of Curiosity...")
        img = generate_card(rank)
        output_path = os.path.join(output_dir, f'curiosity-{rank:02d}.png')
        img.save(output_path)

    print(f"\n✓ All 14 Curiosity cards generated!")
    print(f"  Location: {output_dir}/curiosity-*.png")


if __name__ == '__main__':
    main()
