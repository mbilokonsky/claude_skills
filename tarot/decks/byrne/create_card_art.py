#!/usr/bin/env python3
"""
Create pixel art for 'Uh-Oh, Love Comes to Town' card
Theme: Innocence, arrival, naïve entry
Style: Early Byrne - cooler palettes, static composition, documentary aesthetic
"""

from PIL import Image, ImageDraw
import math

# Tarot aspect ratio: roughly 2:3
WIDTH = 280
HEIGHT = 420

# Color palette - cool, early Talking Heads aesthetic
# Documentary grays and blues with hints of urban yellow light
PALETTE = {
    'dark_interior': (28, 32, 38),      # Very dark blue-gray (inside)
    'doorframe': (45, 52, 62),          # Dark frame
    'floor_dark': (52, 58, 68),         # Interior floor
    'figure_dark': (38, 42, 48),        # Figure silhouette
    'coat_gray': (72, 82, 95),          # Figure's coat
    'suitcase': (95, 68, 52),           # Brown suitcase
    'bright_threshold': (195, 205, 215), # Bright doorway light
    'sky_pale': (165, 178, 195),        # Pale cool sky
    'building_gray': (128, 138, 148),   # Distant buildings
    'light_glow': (225, 228, 195),      # Yellow-tinged light
    'highlight': (245, 248, 235),       # Brightest light
    'sidewalk': (142, 148, 158),        # Exterior ground
    'window_blue': (88, 105, 125),      # Building windows
}

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), PALETTE['dark_interior'])
draw = ImageDraw.Draw(img)

# LAYER 1: Background - bright exterior world
# Sky gradient at top of doorway
for y in range(0, HEIGHT // 2):
    blend = y / (HEIGHT // 2)
    r = int(PALETTE['light_glow'][0] + (PALETTE['sky_pale'][0] - PALETTE['light_glow'][0]) * blend)
    g = int(PALETTE['light_glow'][1] + (PALETTE['sky_pale'][1] - PALETTE['light_glow'][1]) * blend)
    b = int(PALETTE['light_glow'][2] + (PALETTE['sky_pale'][2] - PALETTE['light_glow'][2]) * blend)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Sidewalk/ground in lower exterior
draw.rectangle([0, HEIGHT // 2, WIDTH, HEIGHT], fill=PALETTE['sidewalk'])

# LAYER 2: City buildings in distance (geometric, simple)
# Left building
draw.rectangle([WIDTH//8, HEIGHT//4, WIDTH//3, HEIGHT//2], fill=PALETTE['building_gray'])
# Windows on left building
for wy in range(HEIGHT//4 + 15, HEIGHT//2, 25):
    for wx in range(WIDTH//8 + 10, WIDTH//3 - 10, 20):
        draw.rectangle([wx, wy, wx+8, wy+12], fill=PALETTE['window_blue'])

# Right building (taller)
draw.rectangle([WIDTH*2//3, HEIGHT//6, WIDTH*7//8, HEIGHT//2], fill=PALETTE['building_gray'])
# Windows on right building
for wy in range(HEIGHT//6 + 15, HEIGHT//2, 25):
    for wx in range(WIDTH*2//3 + 12, WIDTH*7//8 - 12, 20):
        draw.rectangle([wx, wy, wx+8, wy+12], fill=PALETTE['window_blue'])

# LAYER 3: Doorframe (defining the threshold)
# This creates the composition - dark interior frame around bright exterior
frame_width = 45
frame_top = 40

# Top of doorframe
draw.rectangle([frame_width, frame_top, WIDTH - frame_width, frame_top + 12],
               fill=PALETTE['doorframe'])

# Left side of doorframe
draw.rectangle([frame_width-12, frame_top, frame_width, HEIGHT],
               fill=PALETTE['doorframe'])

# Right side of doorframe
draw.rectangle([WIDTH - frame_width, frame_top, WIDTH - frame_width + 12, HEIGHT],
               fill=PALETTE['doorframe'])

# Interior floor
draw.rectangle([0, HEIGHT - 80, frame_width, HEIGHT], fill=PALETTE['floor_dark'])

# LAYER 4: Light spill and threshold glow
# Bright light flooding through doorway
light_center_x = WIDTH // 2
light_center_y = HEIGHT // 2

# Create radial glow effect at doorway
for r in range(80, 20, -10):
    alpha_factor = (80 - r) / 60.0
    glow_r = int(PALETTE['light_glow'][0] * alpha_factor + PALETTE['dark_interior'][0] * (1 - alpha_factor))
    glow_g = int(PALETTE['light_glow'][1] * alpha_factor + PALETTE['dark_interior'][1] * (1 - alpha_factor))
    glow_b = int(PALETTE['light_glow'][2] * alpha_factor + PALETTE['dark_interior'][2] * (1 - alpha_factor))
    draw.ellipse([light_center_x - r, light_center_y - r//2,
                  light_center_x + r, light_center_y + r//2],
                 fill=(glow_r, glow_g, glow_b))

# LAYER 5: The figure - at the threshold
# Figure positioned at doorway, slightly awkward
figure_x = frame_width + 20  # Just past the doorframe
figure_y_base = HEIGHT - 85   # Standing on interior floor

# Head (simplified, in profile/three-quarter)
head_x = figure_x + 15
head_y = figure_y_base - 110  # Adjusted to ensure proper spacing
draw.ellipse([head_x, head_y, head_x + 22, head_y + 26], fill=PALETTE['coat_gray'])

# Neck
draw.rectangle([head_x + 8, head_y + 24, head_x + 16, head_y + 32], fill=PALETTE['coat_gray'])

# Body/coat (angular, suggesting awkward posture)
# Torso
body_points = [
    (head_x + 12, head_y + 32),  # neck
    (head_x - 8, head_y + 50),   # left shoulder
    (head_x - 10, head_y + 95),  # left hip
    (head_x + 18, head_y + 98),  # right hip
    (head_x + 22, head_y + 48),  # right shoulder
]
draw.polygon(body_points, fill=PALETTE['coat_gray'])

# Arm holding suitcase (extended down)
arm_x = head_x + 20
draw.rectangle([arm_x, head_y + 50, arm_x + 8, head_y + 85], fill=PALETTE['coat_gray'])

# Legs (simple, standing)
leg1_x = head_x - 2
draw.rectangle([leg1_x, head_y + 95, leg1_x + 8, figure_y_base], fill=PALETTE['figure_dark'])
leg2_x = head_x + 10
draw.rectangle([leg2_x, head_y + 95, leg2_x + 8, figure_y_base], fill=PALETTE['figure_dark'])

# LAYER 6: Suitcase (recognizable object)
suitcase_x = arm_x + 8
suitcase_y = head_y + 82
draw.rectangle([suitcase_x, suitcase_y, suitcase_x + 28, suitcase_y + 20],
               fill=PALETTE['suitcase'])
# Handle
draw.rectangle([suitcase_x + 8, suitcase_y - 8, suitcase_x + 20, suitcase_y],
               fill=PALETTE['figure_dark'])
# Suitcase details (latches)
draw.rectangle([suitcase_x + 3, suitcase_y + 9, suitcase_x + 6, suitcase_y + 12],
               fill=PALETTE['figure_dark'])
draw.rectangle([suitcase_x + 22, suitcase_y + 9, suitcase_x + 25, suitcase_y + 12],
               fill=PALETTE['figure_dark'])

# LAYER 7: Final details - some edge highlights on figure to separate from darkness
# Rim light on head (from bright doorway)
draw.arc([head_x + 14, head_y, head_x + 24, head_y + 26],
         start=270, end=90, fill=PALETTE['bright_threshold'])

# Save the image
img.save('/home/user/claude_skills/tarot/decks/byrne/uh-oh-love-comes-to-town.png')
print("Card artwork created successfully!")
print(f"Size: {WIDTH}x{HEIGHT} pixels")
print(f"Location: /home/user/claude_skills/tarot/decks/byrne/uh-oh-love-comes-to-town.png")
