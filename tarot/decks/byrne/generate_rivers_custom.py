#!/usr/bin/env python3
"""
Custom pixel art generation for the Rivers suit
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
PALETTE = bvt.SuitColors.RIVERS


def draw_river_wave(draw, x1, y, x2, wavelength, amplitude, color, width=2):
    """Helper to draw a flowing wave pattern"""
    points = []
    for x in range(x1, x2, 3):
        offset = amplitude * math.sin((x - x1) / wavelength * math.pi * 2)
        points.append((x, y + offset))

    if len(points) > 1:
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=color, width=width)


def draw_rivers_0_ace(img, draw):
    """
    Ace of Rivers: the first pulse, rhythm spark
    Content: A single wave or pulse, the first beat, concentrated rhythmic potential

    Visual: One perfect wave across the center - the primal pulse
    """
    # Single wave - the first flow
    center_y = HEIGHT // 2

    # One bold, perfect sine wave
    draw_river_wave(draw, 50, center_y, WIDTH - 50, 80, 40, PALETTE['flow'], width=6)

    # Small circular pulse at the center - the source
    pulse_size = 15
    draw.ellipse([WIDTH//2 - pulse_size, center_y - pulse_size,
                  WIDTH//2 + pulse_size, center_y + pulse_size],
                 fill=PALETTE['accent'])


def draw_rivers_1_two(img, draw):
    """
    Two of Rivers: polyrhythm emerging, two patterns interact
    Content: Two water streams meeting, flows mirroring or opposing

    Visual: Two waves intersecting, creating interference pattern
    """
    # Two waves at different wavelengths - creating rhythm dialogue
    y1 = HEIGHT // 2 - 40
    y2 = HEIGHT // 2 + 40

    # First stream - faster rhythm
    draw_river_wave(draw, 30, y1, WIDTH - 30, 50, 35, PALETTE['flow'], width=4)

    # Second stream - slower rhythm
    draw_river_wave(draw, 30, y2, WIDTH - 30, 70, 30, PALETTE['secondary'], width=4)

    # Meeting point in the middle - where they converge
    meeting_x = WIDTH // 2
    # Vertical connection showing interaction
    draw.line([(meeting_x, y1), (meeting_x, y2)], fill=PALETTE['pattern'], width=3)

    # Circles at the meeting point
    draw.ellipse([meeting_x - 8, y1 - 8, meeting_x + 8, y1 + 8], fill=PALETTE['accent'])
    draw.ellipse([meeting_x - 8, y2 - 8, meeting_x + 8, y2 + 8], fill=PALETTE['accent'])


def draw_rivers_2_three(img, draw):
    """
    Three of Rivers: complex pattern forming, polyrhythmic structure, flows braiding
    Content: Three streams weaving together, polyrhythmic notation

    Visual: Three interwoven streams creating visual complexity
    """
    # Three streams braiding together
    y1 = HEIGHT // 2 - 60
    y2 = HEIGHT // 2
    y3 = HEIGHT // 2 + 60

    # Stream 1 - top
    draw_river_wave(draw, 30, y1, WIDTH - 30, 60, 25, PALETTE['flow'], width=4)

    # Stream 2 - middle (slightly offset phase)
    draw_river_wave(draw, 30, y2, WIDTH - 30, 60, 30, PALETTE['secondary'], width=4)

    # Stream 3 - bottom
    draw_river_wave(draw, 30, y3, WIDTH - 30, 60, 28, PALETTE['pattern'], width=4)

    # Braiding points where they cross
    for x in [90, 150, 210]:
        # Vertical connections showing the braid
        draw.line([(x, y1 + 20), (x, y3 - 20)], fill=PALETTE['accent'], width=2)


def draw_rivers_3_four(img, draw):
    """
    Four of Rivers: stable rhythm, pattern established, same as it ever was
    Content: Four streams in stable flow, perfect loop, dependable cycle

    Visual: Four parallel streams in perfect synchronization
    """
    # Four streams in perfect harmony - the established groove
    spacing = (HEIGHT - 120) // 5
    start_y = 80

    for i in range(4):
        y = start_y + i * spacing
        # All same wavelength - showing synchronization
        wavelength = 65
        amplitude = 20 + (i % 2) * 5
        color = PALETTE['flow'] if i % 2 == 0 else PALETTE['secondary']
        draw_river_wave(draw, 40, y, WIDTH - 40, wavelength, amplitude, color, width=4)

    # Four circular markers on the left showing the four-beat
    for i in range(4):
        y = start_y + i * spacing
        draw.ellipse([25, y - 6, 37, y + 6], fill=PALETTE['accent'])


def draw_rivers_4_five(img, draw):
    """
    Five of Rivers: rhythm disrupted, pattern challenged, flow encountering obstacle
    Content: Flows encountering rocks, rhythm notation with rupture

    Visual: Stream hitting obstacles, flow breaking apart
    """
    # Main stream from left
    y = HEIGHT // 2

    # Smooth flow on the left
    draw_river_wave(draw, 30, y - 30, 130, 50, 25, PALETTE['flow'], width=5)
    draw_river_wave(draw, 30, y + 30, 130, 50, 25, PALETTE['secondary'], width=5)

    # OBSTACLE - large rock/barrier in center
    obstacle_points = [
        (140, y - 40),
        (170, y - 50),
        (180, y),
        (170, y + 50),
        (140, y + 40)
    ]
    draw.polygon(obstacle_points, fill=PALETTE['shadow'])

    # Broken, chaotic flow on the right - disrupted pattern
    # Upper split
    for offset in [-20, 0, 20]:
        draw_river_wave(draw, 180, y - 40 + offset, WIDTH - 30, 30, 15, PALETTE['pattern'], width=3)

    # Lower split
    for offset in [-20, 0, 20]:
        draw_river_wave(draw, 180, y + 40 + offset, WIDTH - 30, 35, 12, PALETTE['pattern'], width=3)


def draw_rivers_5_six(img, draw):
    """
    Six of Rivers: rhythm restored, new pattern integrated, flow finding new channel
    Content: Streams finding new arrangement around obstacles, rhythm adapted

    Visual: Flows gracefully moving around obstacles, more complex but coherent
    """
    # Obstacles in the middle
    draw.ellipse([120, 160, 160, 200], fill=PALETTE['shadow'])
    draw.ellipse([130, 240, 165, 275], fill=PALETTE['shadow'])

    # Six streams that flow AROUND the obstacles - adaptive pattern
    # Top streams
    for i, start_y in enumerate([100, 130]):
        points = []
        for x in range(30, WIDTH - 30, 5):
            # Curve around the first obstacle
            if 100 < x < 180:
                y_offset = -40 if x < 140 else -40 + ((x - 140) / 40) * 40
            else:
                y_offset = 0

            wave_y = start_y + 15 * math.sin(x / 40) + y_offset
            points.append((x, wave_y))

        for j in range(len(points) - 1):
            draw.line([points[j], points[j + 1]],
                     fill=PALETTE['flow'] if i == 0 else PALETTE['secondary'], width=3)

    # Middle streams
    for i, start_y in enumerate([210, 235]):
        points = []
        for x in range(30, WIDTH - 30, 5):
            # Curve around the second obstacle
            if 110 < x < 185:
                y_offset = 30 if x < 147 else 30 - ((x - 147) / 38) * 30
            else:
                y_offset = 0

            wave_y = start_y + 12 * math.sin(x / 35) + y_offset
            points.append((x, wave_y))

        for j in range(len(points) - 1):
            draw.line([points[j], points[j + 1]],
                     fill=PALETTE['pattern'] if i == 0 else PALETTE['flow'], width=3)

    # Bottom streams
    for i, start_y in enumerate([300, 330]):
        draw_river_wave(draw, 30, start_y, WIDTH - 30, 50, 20,
                       PALETTE['secondary'] if i == 0 else PALETTE['pattern'], width=3)


def draw_rivers_6_seven(img, draw):
    """
    Seven of Rivers: studying the pattern, rhythm analysis, examining cycles
    Content: Aerial view of multiple streams, rhythm patterns mapped out

    Visual: Top-down view of branching waterways, like a river delta
    """
    # Aerial/map view - showing the meta-perspective

    # Main trunk at bottom
    trunk_x = WIDTH // 2
    draw.line([(trunk_x, HEIGHT - 30), (trunk_x, HEIGHT - 100)],
             fill=PALETTE['flow'], width=12)

    # Seven branches spreading upward (delta pattern)
    branches = [
        (trunk_x, HEIGHT - 100, trunk_x - 70, HEIGHT - 200, 7),  # far left
        (trunk_x, HEIGHT - 100, trunk_x - 40, HEIGHT - 220, 6),  # mid-left
        (trunk_x, HEIGHT - 100, trunk_x - 15, HEIGHT - 250, 5),  # near-left
        (trunk_x, HEIGHT - 100, trunk_x, HEIGHT - 280, 8),        # center
        (trunk_x, HEIGHT - 100, trunk_x + 15, HEIGHT - 250, 5),  # near-right
        (trunk_x, HEIGHT - 100, trunk_x + 40, HEIGHT - 220, 6),  # mid-right
        (trunk_x, HEIGHT - 100, trunk_x + 70, HEIGHT - 200, 7),  # far right
    ]

    for x1, y1, x2, y2, width in branches:
        draw.line([(x1, y1), (x2, y2)], fill=PALETTE['secondary'], width=width)

        # Small circle at each endpoint
        draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=PALETTE['accent'])

    # Grid lines suggesting analysis/mapping
    for y in range(60, HEIGHT - 50, 40):
        draw.line([(20, y), (WIDTH - 20, y)], fill=PALETTE['pattern'], width=1)


def draw_rivers_7_eight(img, draw):
    """
    Eight of Rivers: rhythm applied, flow in purposeful motion, pattern deployed
    Content: Streams actively carving new channels, rhythm in transformative motion

    Visual: Flowing water cutting through landscape, creating new paths
    """
    # Landscape - showing ground being carved
    # Ground layers
    for i, y in enumerate([280, 310, 340, 370]):
        draw.rectangle([0, y, WIDTH, y + 25],
                      fill=PALETTE['shadow'] if i % 2 == 0 else PALETTE['secondary'])

    # Eight active streams cutting down through the layers
    for i, x in enumerate([40, 70, 100, 130, 160, 190, 220, 250]):
        # Vertical flowing streams cutting channels
        stream_points = []
        for y in range(80, 380, 5):
            x_offset = 8 * math.sin(y / 40) * (1 if i % 2 == 0 else -1)
            stream_points.append((x + x_offset, y))

        # Draw the carving stream
        for j in range(len(stream_points) - 1):
            draw.line([stream_points[j], stream_points[j + 1]],
                     fill=PALETTE['flow'], width=3)

        # Source at top
        draw.ellipse([x - 6, 70, x + 6, 82], fill=PALETTE['accent'])


def draw_rivers_8_nine(img, draw):
    """
    Nine of Rivers: complex pattern mastered, polyrhythmic abundance
    Content: Nine streams in elaborate interweaving, complex rhythm fully expressed

    Visual: Nine interwoven streams in beautiful complexity
    """
    # Nine streams in complex polyrhythmic pattern
    # Create three groups of three

    # Group 1 - top third (3 streams)
    for i, base_y in enumerate([90, 110, 130]):
        wavelength = 50 + i * 10
        amplitude = 15 + i * 3
        color = [PALETTE['flow'], PALETTE['secondary'], PALETTE['pattern']][i]
        draw_river_wave(draw, 30, base_y, WIDTH - 30, wavelength, amplitude, color, width=3)

    # Group 2 - middle third (3 streams)
    for i, base_y in enumerate([190, 210, 230]):
        wavelength = 55 + i * 8
        amplitude = 18 + i * 4
        color = [PALETTE['pattern'], PALETTE['flow'], PALETTE['secondary']][i]
        draw_river_wave(draw, 30, base_y, WIDTH - 30, wavelength, amplitude, color, width=3)

    # Group 3 - bottom third (3 streams)
    for i, base_y in enumerate([290, 310, 330]):
        wavelength = 48 + i * 12
        amplitude = 16 + i * 5
        color = [PALETTE['secondary'], PALETTE['pattern'], PALETTE['flow']][i]
        draw_river_wave(draw, 30, base_y, WIDTH - 30, wavelength, amplitude, color, width=3)

    # Nine small circles on the right edge marking each stream
    for i, y in enumerate([90, 110, 130, 190, 210, 230, 290, 310, 330]):
        draw.ellipse([WIDTH - 25, y - 4, WIDTH - 15, y + 4], fill=PALETTE['accent'])


def draw_rivers_9_ten(img, draw):
    """
    Ten of Rivers: pattern at overflow, rhythm exhausted, cycle at its limit
    Content: Ten streams overflowing boundaries, rhythm patterns filling all space

    Visual: Too many streams, chaotic overflow, pattern beyond containment
    """
    # Ten streams but they're overflowing, overlapping, chaotic

    # Start with organized streams that become increasingly chaotic
    for i in range(10):
        base_y = 60 + i * 30

        if i < 5:
            # Early streams: still organized
            draw_river_wave(draw, 20, base_y, WIDTH - 20, 50 + i * 5, 20,
                          PALETTE['flow'] if i % 2 == 0 else PALETTE['secondary'], width=3)
        else:
            # Later streams: breaking boundaries
            # Longer waves that spill beyond
            start_x = 20 - (i - 5) * 10
            end_x = WIDTH - 20 + (i - 5) * 10
            wavelength = 40 + i * 3
            amplitude = 25 + (i - 5) * 5

            # Clip to show overflow
            draw_river_wave(draw, max(0, start_x), base_y, min(WIDTH, end_x),
                          wavelength, amplitude, PALETTE['pattern'], width=4)

    # Chaos markers - showing the pattern is too much
    for i in range(6):
        x = 30 + i * 40
        for j in range(3):
            y = HEIGHT - 60 + j * 15
            draw.line([(x, y), (x + 25, y)], fill=PALETTE['shadow'], width=2)


def draw_rivers_10_observer(img, draw):
    """
    Observer of Rivers: watching patterns, documenting rhythms, studying flow from outside
    Content: A figure watching rivers flow, documenting rhythm patterns

    Visual: Figure with notebook by riverside, studying the flow analytically
    """
    # River in background
    river_y = 180
    for offset in [-25, 0, 25]:
        draw_river_wave(draw, 100, river_y + offset, WIDTH - 30, 60, 20,
                       PALETTE['flow'] if offset == 0 else PALETTE['secondary'], width=4)

    # Riverbank
    bank_points = [(100, 150), (100, HEIGHT), (0, HEIGHT), (0, 200)]
    draw.polygon(bank_points, fill=PALETTE['shadow'])

    # THE OBSERVER - figure sitting by river with notebook
    # Head
    draw.ellipse([55, 280, 80, 305], fill=PALETTE['accent'])

    # Body seated
    body_points = [(67, 305), (45, 320), (40, 380), (95, 380), (90, 320)]
    draw.polygon(body_points, fill=PALETTE['pattern'])

    # Notebook on lap
    draw.rectangle([50, 340, 75, 370], fill=PALETTE['primary'], outline=PALETTE['shadow'], width=2)
    # Lines on notebook
    for line_y in [348, 356, 364]:
        draw.line([(54, line_y), (71, line_y)], fill=PALETTE['shadow'], width=1)

    # Pencil in hand
    draw.line([(75, 355), (88, 350)], fill=PALETTE['shadow'], width=3)

    # Eyes looking at river
    draw.line([(62, 290), (64, 290)], fill=PALETTE['shadow'], width=2)
    draw.line([(72, 290), (74, 290)], fill=PALETTE['shadow'], width=2)


def draw_rivers_11_pretender(img, draw):
    """
    Pretender of Rivers: performing rhythm, theatrical flow, confident pattern
    Content: Figure making grand rhythmic gestures, dramatic costume

    Visual: Big theatrical gestures suggesting rhythm, costume with flowing elements
    """
    # Flowing decorative background - theatrical stage
    for i in range(8):
        y = 60 + i * 45
        draw_river_wave(draw, 150, y, WIDTH - 20, 40, 15, PALETTE['pattern'], width=2)

    # THE PRETENDER - figure with dramatic gesture
    # Small head (Byrne style)
    head_x, head_y = 100, 160
    draw.ellipse([head_x - 12, head_y, head_x + 12, head_y + 24], fill=PALETTE['accent'])

    # Large dramatic costume with flowing elements
    costume_points = [
        (head_x, head_y + 24),
        (head_x - 65, head_y + 60),   # Wide flowing shoulder
        (head_x - 70, head_y + 140),  # Flowing left side
        (head_x - 50, head_y + 260),
        (head_x - 20, head_y + 320),
        (head_x + 20, head_y + 320),
        (head_x + 50, head_y + 260),
        (head_x + 70, head_y + 140),  # Flowing right side
        (head_x + 65, head_y + 60),   # Wide flowing shoulder
    ]
    draw.polygon(costume_points, fill=PALETTE['secondary'])

    # Arm in grand sweeping gesture
    arm_points = [
        (head_x + 65, head_y + 80),
        (head_x + 120, head_y + 40),  # Sweeping up
        (head_x + 130, head_y + 45),
        (head_x + 70, head_y + 90)
    ]
    draw.polygon(arm_points, fill=PALETTE['shadow'])

    # Flowing ribbons/streamers
    for i, start_x in enumerate([head_x - 60, head_x - 40, head_x + 40]):
        start_y = head_y + 100
        draw_river_wave(draw, start_x, start_y, start_x + 50, 30, 20, PALETTE['flow'], width=4)


def draw_rivers_12_exile(img, draw):
    """
    Exile of Rivers: alone with broken rhythms, pattern dissolved, flow dried up
    Content: Solitary figure by dried riverbeds, silent rhythm

    Visual: Dry cracked riverbed, figure alone with the absence of flow
    """
    # Dried riverbed - cracked earth
    # Riverbed outline
    bed_points = [
        (30, 200), (60, 180), (100, 170), (140, 175), (180, 185), (220, 195), (250, 210),
        (250, 280), (220, 300), (180, 310), (140, 305), (100, 295), (60, 285), (30, 270)
    ]
    draw.polygon(bed_points, fill=PALETTE['shadow'])

    # Cracks in the dry bed - broken pattern
    cracks = [
        [(50, 200), (80, 240), (60, 270)],
        [(120, 180), (140, 220), (130, 260)],
        [(190, 190), (200, 230), (185, 280)],
        [(100, 210), (160, 215)],
        [(70, 250), (140, 245)],
    ]
    for crack in cracks:
        for i in range(len(crack) - 1):
            draw.line([crack[i], crack[i + 1]], fill=PALETTE['primary'], width=3)

    # A few stones/rocks where water used to be
    for x, y in [(90, 220), (170, 240), (130, 280)]:
        draw.ellipse([x - 8, y - 6, x + 8, y + 6], fill=PALETTE['pattern'])

    # THE EXILE - hunched figure at the edge
    head_x, head_y = 220, 340

    # Head bowed
    draw.ellipse([head_x - 12, head_y, head_x + 12, head_y + 24], fill=PALETTE['accent'])

    # Body hunched, sitting at the dry riverbed edge
    body_points = [
        (head_x, head_y + 24),
        (head_x - 25, head_y + 40),
        (head_x - 30, head_y + 70),
        (head_x + 30, head_y + 70),
        (head_x + 25, head_y + 40)
    ]
    draw.polygon(body_points, fill=PALETTE['flow'])

    # Hand touching the dry earth
    draw.line([(head_x - 25, head_y + 60), (head_x - 50, head_y + 50)],
             fill=PALETTE['flow'], width=6)
    draw.ellipse([head_x - 55, head_y + 47, head_x - 45, head_y + 57], fill=PALETTE['flow'])


def draw_rivers_13_giant(img, draw):
    """
    Giant of Rivers: authentic rhythm mastery, collaborative flow, conducting polyrhythm
    Content: Figure at full height conducting polyrhythm with others visible

    Visual: Tall figure conducting, multiple figures moving in sync, shared current
    """
    # Flowing rivers in background - the collaborative current
    for i in range(4):
        y = 120 + i * 60
        draw_river_wave(draw, 30, y, WIDTH - 30, 70, 25,
                       PALETTE['flow'] if i % 2 == 0 else PALETTE['secondary'], width=5)

    # THE GIANT - tall figure conducting
    head_x, head_y = 140, 140

    # Head proportional
    draw.ellipse([head_x - 14, head_y, head_x + 14, head_y + 28], fill=PALETTE['accent'])

    # Body upright, conducting
    body_points = [
        (head_x, head_y + 28),
        (head_x - 35, head_y + 55),
        (head_x - 38, head_y + 130),
        (head_x - 35, head_y + 200),
        (head_x - 15, head_y + 280),
        (head_x + 15, head_y + 280),
        (head_x + 35, head_y + 200),
        (head_x + 38, head_y + 130),
        (head_x + 35, head_y + 55),
    ]
    draw.polygon(body_points, fill=PALETTE['pattern'])

    # Arms conducting - graceful gestures
    # Left arm
    left_arm = [(head_x - 35, head_y + 75), (head_x - 70, head_y + 100),
                (head_x - 75, head_y + 110), (head_x - 38, head_y + 85)]
    draw.polygon(left_arm, fill=PALETTE['pattern'])

    # Right arm
    right_arm = [(head_x + 35, head_y + 75), (head_x + 70, head_y + 90),
                 (head_x + 75, head_y + 100), (head_x + 38, head_y + 85)]
    draw.polygon(right_arm, fill=PALETTE['pattern'])

    # Other figures moving in the flow - collaborative
    # Left figure
    draw.ellipse([50, 310, 65, 325], fill=PALETTE['accent'])
    draw.rectangle([52, 325, 63, 355], fill=PALETTE['secondary'])

    # Right figure
    draw.ellipse([215, 320, 230, 335], fill=PALETTE['accent'])
    draw.rectangle([217, 335, 228, 365], fill=PALETTE['secondary'])

    # Center figure
    draw.ellipse([130, 340, 145, 355], fill=PALETTE['accent'])
    draw.rectangle([132, 355, 143, 385], fill=PALETTE['secondary'])


# Main generation function
def generate_card(rank):
    """Generate a specific Rivers card by rank (0-13)"""
    img = bvt.create_canvas(PALETTE['primary'])
    draw = ImageDraw.Draw(img)

    # Draw the specific card
    card_functions = [
        draw_rivers_0_ace,
        draw_rivers_1_two,
        draw_rivers_2_three,
        draw_rivers_3_four,
        draw_rivers_4_five,
        draw_rivers_5_six,
        draw_rivers_6_seven,
        draw_rivers_7_eight,
        draw_rivers_8_nine,
        draw_rivers_9_ten,
        draw_rivers_10_observer,
        draw_rivers_11_pretender,
        draw_rivers_12_exile,
        draw_rivers_13_giant,
    ]

    if 0 <= rank <= 13:
        card_functions[rank](img, draw)

    return img


def main():
    """Generate all 14 Rivers cards with custom pixel art"""
    print("Generating custom Rivers suit cards...\n")

    output_dir = '/home/user/claude_skills/tarot/decks/byrne/cards'
    os.makedirs(output_dir, exist_ok=True)

    card_names = [
        "Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
        "Eight", "Nine", "Ten", "Observer", "Pretender", "Exile", "Giant"
    ]

    for rank in range(14):
        print(f"  [{rank + 1}/14] {card_names[rank]} of Rivers...")
        img = generate_card(rank)
        output_path = os.path.join(output_dir, f'rivers-{rank:02d}.png')
        img.save(output_path)

    print(f"\n✓ All 14 Rivers cards generated!")
    print(f"  Location: {output_dir}/rivers-*.png")


if __name__ == '__main__':
    main()
