#!/usr/bin/env python3
"""
Sound of Music Tarot - Visual Toolkit

This is a style guide and reference library for generating card imagery.
It provides color palettes, helper functions, and visual language for each suit
and the Major Arcana.

The deck's visual thesis: Technicolor meets dialectical tension.
Each suit has a distinct aesthetic reflecting its position in the dialectical space.
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Standard card dimensions (2:3 tarot ratio)
CARD_WIDTH = 280
CARD_HEIGHT = 420

# =============================================================================
# COLOR PALETTES
# =============================================================================

class SongsColors:
    """
    Songs suit (Authentic/Creative): Alpine meadow watercolors
    Bright, airy, impressionistic - the aesthetic of spontaneous joy
    """
    PRIMARY = (135, 206, 250)      # Sky blue
    SECONDARY = (144, 238, 144)    # Light green (grass)
    ACCENT_1 = (255, 218, 185)     # Peach (wildflowers)
    ACCENT_2 = (255, 192, 203)     # Pink (wildflowers)
    ACCENT_3 = (255, 255, 102)     # Yellow (wildflowers)
    HIGHLIGHT = (255, 250, 205)    # Lemon chiffon (sunlight)
    SHADOW = (100, 149, 237)       # Cornflower blue (sky depth)
    GROUND = (34, 139, 34)         # Forest green (meadow base)

class MountainsColors:
    """
    Mountains suit (Authentic/Transmissive): Weathered stone romanticism
    Monumental, permanent, Caspar David Friedrich sublime
    """
    PRIMARY = (112, 128, 144)      # Slate gray (stone)
    SECONDARY = (139, 69, 19)      # Saddle brown (earth)
    ACCENT = (255, 250, 250)       # Snow white
    HIGHLIGHT = (176, 196, 222)    # Light steel blue (distant sky)
    SHADOW = (47, 79, 79)          # Dark slate gray
    GROUND = (160, 82, 45)         # Sienna (earth)
    PEAK = (245, 245, 245)         # White smoke (snow)

class PuppetsColors:
    """
    Puppets suit (Instrumental/Creative): Theatrical staging
    Art Deco meets German Expressionist theater - dramatic, purposeful
    """
    PRIMARY = (139, 0, 0)          # Dark red (curtains)
    SECONDARY = (218, 165, 32)     # Goldenrod (gilt, brass)
    ACCENT_1 = (75, 0, 130)        # Indigo (deep purple)
    ACCENT_2 = (220, 20, 60)       # Crimson
    HIGHLIGHT = (255, 215, 0)      # Gold (spotlight)
    SHADOW = (0, 0, 0)             # Black (stage darkness)
    STAGE = (139, 0, 0)            # Dark red (stage)
    STRING = (192, 192, 192)       # Silver (puppet strings)

class WhistlesColors:
    """
    Whistles suit (Instrumental/Transmissive): Naval precision
    Bauhaus clarity, institutional order - can be protective or oppressive
    """
    PRIMARY = (25, 25, 112)        # Midnight blue (naval)
    SECONDARY = (255, 255, 255)    # White (crisp uniform)
    ACCENT = (184, 134, 11)        # Dark goldenrod (brass)
    HIGHLIGHT = (240, 248, 255)    # Alice blue (light)
    SHADOW = (47, 79, 79)          # Dark slate (iron)
    GROUND = (105, 105, 105)       # Dim gray (order)
    METAL = (169, 169, 169)        # Dark gray (steel)

class MajorArcanaColors:
    """
    Major Arcana: Cinematic Technicolor journey
    Colors shift through the narrative arc from natural to golden to dramatic
    """
    # Early cards (0-6): Natural, outdoor, beginning
    EARLY = {
        'sky': (135, 206, 250),
        'meadow': (144, 238, 144),
        'earth': (160, 82, 45),
        'light': (255, 250, 205),
        'shadow': (100, 149, 237)
    }

    # Middle cards (7-13): Indoor, warm, golden
    MIDDLE = {
        'wall': (222, 184, 135),      # Burlywood
        'wood': (139, 69, 19),         # Saddle brown
        'gold': (218, 165, 32),        # Goldenrod
        'light': (255, 228, 181),      # Moccasin
        'shadow': (101, 67, 33)        # Dark brown
    }

    # Late cards (14-18): Dramatic, twilight, crisis/resolution
    LATE = {
        'twilight': (72, 61, 139),     # Dark slate blue
        'stone': (112, 128, 144),      # Slate gray
        'gold': (255, 215, 0),         # Gold
        'light': (255, 250, 240),      # Floral white
        'shadow': (25, 25, 112),       # Midnight blue
        'urgent': (178, 34, 34)        # Firebrick (danger)
    }

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_card_base(bg_color=(255, 255, 255)):
    """Create a blank card with background color"""
    return Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), bg_color)

def draw_gradient_sky(draw, y_start, y_end, color_top, color_bottom):
    """Draw a vertical gradient (for skies)"""
    for y in range(y_start, y_end):
        t = (y - y_start) / (y_end - y_start)
        r = int(color_top[0] * (1-t) + color_bottom[0] * t)
        g = int(color_top[1] * (1-t) + color_bottom[1] * t)
        b = int(color_top[2] * (1-t) + color_bottom[2] * t)
        draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

def draw_mountain_peak(draw, x_base, y_base, width, height, color, snow=True):
    """Draw a simple mountain peak"""
    points = [
        (x_base - width//2, y_base),
        (x_base, y_base - height),
        (x_base + width//2, y_base)
    ]
    draw.polygon(points, fill=color)

    if snow:
        # Snow cap
        snow_height = height // 3
        snow_points = [
            (x_base - width//6, y_base - height + snow_height),
            (x_base, y_base - height),
            (x_base + width//6, y_base - height + snow_height)
        ]
        draw.polygon(snow_points, fill=(255, 255, 255))

def draw_wildflowers(draw, x, y, num_flowers, palette):
    """Draw scattered wildflowers for Songs suit"""
    import random
    random.seed(x + y)  # Consistent randomness

    flower_colors = [palette.ACCENT_1, palette.ACCENT_2, palette.ACCENT_3]

    for i in range(num_flowers):
        fx = x + random.randint(-20, 20)
        fy = y + random.randint(-15, 15)
        color = random.choice(flower_colors)

        # Simple flower: small circle with petals
        draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=color)

def draw_puppet_strings(draw, x_control, y_control, x_puppet, y_puppet, color):
    """Draw marionette control strings"""
    # Draw 4 strings from control bar to puppet
    draw.line([(x_control-10, y_control), (x_puppet-5, y_puppet)], fill=color, width=1)
    draw.line([(x_control-3, y_control), (x_puppet-2, y_puppet)], fill=color, width=1)
    draw.line([(x_control+3, y_control), (x_puppet+2, y_puppet)], fill=color, width=1)
    draw.line([(x_control+10, y_control), (x_puppet+5, y_puppet)], fill=color, width=1)

def draw_whistle(draw, x, y, size, color):
    """Draw a simple naval boatswain's whistle"""
    # Main body (ellipse)
    draw.ellipse([x-size, y-size//2, x+size, y+size//2], fill=color)
    # Mouthpiece (rectangle)
    draw.rectangle([x-size*1.5, y-size//4, x-size, y+size//4], fill=color)
    # Sound hole
    draw.ellipse([x+size//2, y-size//4, x+size//2+4, y-size//4+4], fill=(0, 0, 0))

def draw_musical_note(draw, x, y, size, color):
    """Draw a simple musical note"""
    # Note head (filled circle)
    draw.ellipse([x-size//2, y, x+size//2, y+size], fill=color)
    # Stem
    draw.rectangle([x+size//2-2, y-size*2, x+size//2+2, y], fill=color)
    # Flag
    draw.polygon([
        (x+size//2+2, y-size*2),
        (x+size//2+2+size, y-size*1.5),
        (x+size//2+2, y-size)
    ], fill=color)

def draw_edelweiss(draw, x, y, size, color=(255, 255, 255)):
    """Draw a simple edelweiss flower (for Mountains suit)"""
    # Center
    draw.ellipse([x-size//4, y-size//4, x+size//4, y+size//4], fill=(255, 255, 200))

    # Petals (8 petals in star pattern)
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(angle)
        px = x + int(size * math.cos(rad))
        py = y + int(size * math.sin(rad))
        draw.ellipse([px-size//3, py-size//3, px+size//3, py+size//3], fill=color)

# =============================================================================
# SUIT-SPECIFIC STYLE HELPERS
# =============================================================================

def get_songs_background(draw):
    """Create typical Songs suit background: sky and meadow"""
    # Sky gradient
    draw_gradient_sky(draw, 0, CARD_HEIGHT//2,
                     SongsColors.HIGHLIGHT, SongsColors.PRIMARY)
    # Meadow
    draw.rectangle([0, CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT],
                  fill=SongsColors.GROUND)

def get_mountains_background(draw, with_peaks=True):
    """Create typical Mountains suit background: distant peaks and stone"""
    # Sky
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT//3], fill=MountainsColors.HIGHLIGHT)

    if with_peaks:
        # Distant peaks
        draw_mountain_peak(draw, CARD_WIDTH//4, CARD_HEIGHT//3, 80, 60,
                          MountainsColors.SHADOW, snow=True)
        draw_mountain_peak(draw, CARD_WIDTH//2, CARD_HEIGHT//3, 100, 80,
                          MountainsColors.PRIMARY, snow=True)
        draw_mountain_peak(draw, 3*CARD_WIDTH//4, CARD_HEIGHT//3, 70, 50,
                          MountainsColors.SHADOW, snow=True)

    # Stone ground
    draw.rectangle([0, CARD_HEIGHT//3, CARD_WIDTH, CARD_HEIGHT],
                  fill=MountainsColors.GROUND)

def get_puppets_background(draw):
    """Create typical Puppets suit background: stage curtains"""
    # Black background
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT], fill=PuppetsColors.SHADOW)

    # Red curtains on sides
    draw.rectangle([0, 0, 40, CARD_HEIGHT], fill=PuppetsColors.PRIMARY)
    draw.rectangle([CARD_WIDTH-40, 0, CARD_WIDTH, CARD_HEIGHT],
                  fill=PuppetsColors.PRIMARY)

    # Spotlight effect (lighter in center)
    for y in range(0, CARD_HEIGHT):
        for x in range(40, CARD_WIDTH-40):
            dist_from_center = abs(x - CARD_WIDTH//2) / (CARD_WIDTH//2)
            brightness = int(30 * (1 - dist_from_center * 0.5))
            draw.point((x, y), fill=(brightness, brightness, brightness))

def get_whistles_background(draw):
    """Create typical Whistles suit background: geometric precision"""
    # Navy background
    draw.rectangle([0, 0, CARD_WIDTH, CARD_HEIGHT], fill=WhistlesColors.PRIMARY)

    # Geometric grid (subtle)
    grid_color = (35, 35, 122)
    for x in range(0, CARD_WIDTH, 40):
        draw.line([(x, 0), (x, CARD_HEIGHT)], fill=grid_color, width=1)
    for y in range(0, CARD_HEIGHT, 40):
        draw.line([(0, y), (CARD_WIDTH, y)], fill=grid_color, width=1)

# =============================================================================
# TESTING / EXAMPLES
# =============================================================================

def generate_suit_palette_demo():
    """Generate a demo showing all four suit color palettes"""
    demo_width = CARD_WIDTH * 4
    demo_height = CARD_HEIGHT

    img = Image.new('RGB', (demo_width, demo_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Songs
    img_songs = create_card_base()
    draw_songs = ImageDraw.Draw(img_songs)
    get_songs_background(draw_songs)
    draw_wildflowers(draw_songs, CARD_WIDTH//2, CARD_HEIGHT*3//4, 20, SongsColors)
    img.paste(img_songs, (0, 0))

    # Mountains
    img_mountains = create_card_base()
    draw_mountains = ImageDraw.Draw(img_mountains)
    get_mountains_background(draw_mountains, with_peaks=True)
    draw_edelweiss(draw_mountains, CARD_WIDTH//2, CARD_HEIGHT*2//3, 15)
    img.paste(img_mountains, (CARD_WIDTH, 0))

    # Puppets
    img_puppets = create_card_base()
    draw_puppets = ImageDraw.Draw(img_puppets)
    get_puppets_background(draw_puppets)
    draw_puppet_strings(draw_puppets, CARD_WIDTH//2, 100, CARD_WIDTH//2, 200,
                       PuppetsColors.STRING)
    img.paste(img_puppets, (CARD_WIDTH*2, 0))

    # Whistles
    img_whistles = create_card_base()
    draw_whistles = ImageDraw.Draw(img_whistles)
    get_whistles_background(draw_whistles)
    draw_whistle(draw_whistles, CARD_WIDTH//2, CARD_HEIGHT//2, 20,
                WhistlesColors.ACCENT)
    img.paste(img_whistles, (CARD_WIDTH*3, 0))

    return img

if __name__ == '__main__':
    # Generate palette demo
    demo = generate_suit_palette_demo()
    demo.save('sound_of_music_palette_demo.png')
    print("Generated palette demo: sound_of_music_palette_demo.png")
    print(f"Card dimensions: {CARD_WIDTH}x{CARD_HEIGHT}")
    print("\nSuit palettes defined:")
    print("  - Songs: Alpine meadow watercolors")
    print("  - Mountains: Weathered stone romanticism")
    print("  - Puppets: Theatrical staging")
    print("  - Whistles: Naval precision")
