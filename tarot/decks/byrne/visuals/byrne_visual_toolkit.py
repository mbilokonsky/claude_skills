#!/usr/bin/env python3
"""
Byrne Journey Tarot - Visual Toolkit

This is a reference library and sketch toolkit, not a complete generative system.
It provides color palettes, helper functions, and example generators to maintain
visual coherence across the deck while allowing each card to be unique.

Think of this as a style guide that happens to be executable code.
"""

from PIL import Image, ImageDraw, ImageFont
import math

# Standard card dimensions (2:3 tarot ratio)
CARD_WIDTH = 280
CARD_HEIGHT = 420

# =============================================================================
# COLOR PALETTES
# =============================================================================

class MajorArcanaColors:
    """
    Color progression for Major Arcana: cool/static → warm/dynamic
    Early cards (0-7): Cool grays, blues, detached documentary aesthetic
    Middle cards (8-14): Transition, more color introduction
    Late cards (15-21): Warm, vibrant, embodied movement
    """

    # Early era (Talking Heads 77-80): Anxious observation
    EARLY = {
        'primary': (72, 82, 95),        # Cool gray-blue
        'secondary': (45, 52, 62),       # Dark blue-gray
        'accent': (165, 178, 195),       # Pale cool sky
        'highlight': (225, 228, 195),    # Pale yellow-tinged light
        'shadow': (28, 32, 38),          # Very dark
        'ground': (142, 148, 158),       # Cool concrete
    }

    # Transition era (Remain in Light-Speaking in Tongues): Discovery
    MIDDLE = {
        'primary': (105, 115, 125),      # Warmer gray
        'secondary': (85, 95, 105),      # Medium blue-gray
        'accent': (185, 145, 95),        # Warm earth tone
        'highlight': (215, 195, 145),    # Warm light
        'shadow': (42, 48, 55),          # Less stark shadow
        'ground': (125, 135, 125),       # Warmer ground
    }

    # Late era (American Utopia onwards): Joy and presence
    LATE = {
        'primary': (185, 95, 75),        # Warm red-orange
        'secondary': (145, 125, 95),     # Warm brown
        'accent': (225, 185, 95),        # Golden yellow
        'highlight': (245, 225, 185),    # Warm bright light
        'shadow': (65, 45, 38),          # Warm shadow
        'ground': (165, 145, 125),       # Warm earth
    }

    @staticmethod
    def for_card_number(n):
        """Returns palette for major arcana card number (0-21)"""
        if n <= 7:
            return MajorArcanaColors.EARLY
        elif n <= 14:
            return MajorArcanaColors.MIDDLE
        else:
            return MajorArcanaColors.LATE

    @staticmethod
    def interpolate_palette(n):
        """Smooth interpolation across all 22 major arcana cards"""
        # This is more nuanced - each card gets a unique blend
        t = n / 21.0  # 0.0 to 1.0

        if t < 0.33:  # Early era
            blend = t / 0.33
            return MajorArcanaColors._blend_palettes(
                MajorArcanaColors.EARLY,
                MajorArcanaColors.MIDDLE,
                blend * 0.5  # Slow transition
            )
        elif t < 0.66:  # Middle era
            blend = (t - 0.33) / 0.33
            return MajorArcanaColors._blend_palettes(
                MajorArcanaColors.MIDDLE,
                MajorArcanaColors.LATE,
                blend * 0.5
            )
        else:  # Late era
            blend = (t - 0.66) / 0.34
            return MajorArcanaColors._blend_palettes(
                MajorArcanaColors.LATE,
                MajorArcanaColors.LATE,  # Stay in late
                blend
            )

    @staticmethod
    def _blend_palettes(pal1, pal2, t):
        """Blend two palettes by factor t (0.0 to 1.0)"""
        result = {}
        for key in pal1:
            c1 = pal1[key]
            c2 = pal2[key]
            result[key] = (
                int(c1[0] + (c2[0] - c1[0]) * t),
                int(c1[1] + (c2[1] - c1[1]) * t),
                int(c1[2] + (c2[2] - c1[2]) * t)
            )
        return result


class SuitColors:
    """
    Each suit has its own complete visual language and color palette.
    These are distinct worlds, not variations on a theme.
    """

    STRUCTURES = {
        # observation, analysis, blueprints, containment
        # Clean geometric, architectural, white and cool grays
        'primary': (245, 248, 252),      # Almost white
        'secondary': (185, 195, 205),    # Cool light gray
        'accent': (95, 125, 155),        # Blueprint blue
        'grid': (155, 165, 175),         # Grid lines
        'shadow': (65, 72, 82),          # Dark but not black
        'frame': (125, 135, 145),        # Structure frames
    }

    RIVERS = {
        # cycles, patterns, rhythm, natural systems
        # Organic patterns, warm earth tones, rhythmic variations
        'primary': (145, 115, 85),       # Warm earth brown
        'secondary': (115, 135, 105),    # Organic green
        'accent': (185, 155, 115),       # Sandy warm
        'flow': (95, 145, 165),          # Water blue
        'shadow': (55, 45, 38),          # Rich dark earth
        'pattern': (165, 135, 95),       # Pattern accent
    }

    CURIOSITY = {
        # inquiry, civic engagement, dialogue, reasons to be cheerful
        # Bright optimistic, yellows and sky blues
        'primary': (245, 215, 95),       # Bright yellow
        'secondary': (145, 195, 235),    # Sky blue
        'accent': (255, 185, 85),        # Warm yellow-orange
        'dialogue': (195, 215, 225),     # Conversational pale blue
        'shadow': (85, 95, 105),         # Soft shadow
        'text': (65, 75, 85),            # Text color
    }

    DANCE = {
        # embodied joy, collective movement, groove, presence
        # Dynamic warm reds, oranges, golds with electric accents
        'primary': (215, 85, 65),        # Vibrant red
        'secondary': (235, 145, 55),     # Orange
        'accent': (245, 195, 75),        # Gold
        'electric': (195, 95, 215),      # Electric purple accent
        'shadow': (85, 35, 28),          # Warm dark
        'heat': (255, 125, 85),          # Heat glow
    }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_canvas(bg_color=None):
    """Create a standard tarot card canvas"""
    if bg_color is None:
        bg_color = (255, 255, 255)
    return Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), bg_color)


def radial_gradient(draw, center_x, center_y, radius, inner_color, outer_color):
    """
    Draw a radial gradient (example of a reusable effect)
    This is a helper, but each use might vary the parameters
    """
    for r in range(int(radius), 0, -5):
        t = 1.0 - (r / radius)
        color = (
            int(outer_color[0] + (inner_color[0] - outer_color[0]) * t),
            int(outer_color[1] + (inner_color[1] - outer_color[1]) * t),
            int(outer_color[2] + (inner_color[2] - outer_color[2]) * t),
        )
        draw.ellipse([
            center_x - r, center_y - r,
            center_x + r, center_y + r
        ], fill=color)


def draw_grid_pattern(draw, bounds, spacing, color, opacity=1.0):
    """
    Draw a grid pattern (useful for Structures suit)
    bounds: (x1, y1, x2, y2)
    """
    x1, y1, x2, y2 = bounds
    # Vertical lines
    for x in range(x1, x2, spacing):
        draw.line([(x, y1), (x, y2)], fill=color, width=1)
    # Horizontal lines
    for y in range(y1, y2, spacing):
        draw.line([(x1, y), (x2, y)], fill=color, width=1)


def draw_flow_pattern(draw, bounds, wavelength, amplitude, color):
    """
    Draw a flowing wave pattern (useful for Rivers suit)
    This is just ONE example of how flow might look
    """
    x1, y1, x2, y2 = bounds
    for y in range(y1, y2, 5):
        points = []
        for x in range(x1, x2, 2):
            offset = amplitude * math.sin((x / wavelength) * 2 * math.pi)
            points.append((x, y + offset))
        if len(points) > 1:
            draw.line(points, fill=color, width=2)


# =============================================================================
# EXAMPLE GENERATORS
# =============================================================================
# These show concepts/vibes, not deterministic outputs

def example_figure_simple(canvas, x, y, palette, posture='neutral', scale=1.0):
    """
    Draw a SIMPLE figure - this is a reference example
    Real cards might use this as a starting point but will vary significantly

    posture options: 'neutral', 'awkward', 'observing', 'moving'
    This doesn't implement all postures - it's showing the concept
    """
    draw = ImageDraw.Draw(canvas)

    # Scale factor
    s = scale

    # Head
    head_r = int(12 * s)
    draw.ellipse([x - head_r, y - int(90*s),
                  x + head_r, y - int(66*s)],
                 fill=palette.get('primary', (100, 100, 100)))

    # Body posture varies
    if posture == 'awkward':
        # Angular, stiff
        body = [(x, y - int(65*s)), (x - int(10*s), y - int(40*s)),
                (x - int(12*s), y), (x + int(12*s), y),
                (x + int(10*s), y - int(40*s))]
    elif posture == 'moving':
        # More fluid, tilted
        body = [(x + int(5*s), y - int(65*s)), (x - int(15*s), y - int(40*s)),
                (x - int(8*s), y), (x + int(16*s), y),
                (x + int(18*s), y - int(35*s))]
    else:  # neutral
        body = [(x, y - int(65*s)), (x - int(12*s), y - int(40*s)),
                (x - int(12*s), y), (x + int(12*s), y),
                (x + int(12*s), y - int(40*s))]

    draw.polygon(body, fill=palette.get('secondary', (80, 80, 80)))


def example_building(canvas, x, y, width, height, palette, windows=True):
    """
    Draw a simple building - example for urban scenes
    Each card might render buildings differently
    """
    draw = ImageDraw.Draw(canvas)

    # Building body
    draw.rectangle([x, y, x + width, y + height],
                   fill=palette.get('secondary', (120, 120, 120)))

    # Windows if requested
    if windows:
        window_color = palette.get('accent', (80, 90, 100))
        for wy in range(y + 15, y + height, 25):
            for wx in range(x + 10, x + width - 10, 20):
                draw.rectangle([wx, wy, wx + 8, wy + 12], fill=window_color)


# =============================================================================
# SUIT SYMBOL RENDERERS
# =============================================================================

def render_suit_symbol_structures(size=64):
    """Render the Structures symbol (house shape) as pixel art"""
    img = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    color = SuitColors.STRUCTURES['accent']
    s = size / 100  # Scale factor

    # House outline
    points = [
        (50*s, 15*s), (20*s, 40*s), (20*s, 85*s),
        (80*s, 85*s), (80*s, 40*s)
    ]
    draw.polygon(points, fill=color, outline=color)

    # Door
    draw.rectangle([40*s, 60*s, 60*s, 85*s], fill=(255, 255, 255))

    # Windows
    draw.rectangle([30*s, 45*s, 42*s, 57*s], fill=(255, 255, 255))
    draw.rectangle([58*s, 45*s, 70*s, 57*s], fill=(255, 255, 255))

    return img


def render_suit_symbol_rivers(size=64):
    """Render the Rivers symbol (flowing water) as pixel art"""
    img = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    color = SuitColors.RIVERS['flow']
    s = size / 100

    # Flowing water shape
    points = []
    for y in range(0, 100, 2):
        x_offset = 20 * math.sin(y / 20 * math.pi)
        points.append((30*s + x_offset*s, y*s))
    for y in range(100, 0, -2):
        x_offset = 20 * math.sin(y / 20 * math.pi)
        points.append((70*s + x_offset*s, y*s))

    draw.polygon(points, fill=color)

    return img


def render_suit_symbol_curiosity(size=64):
    """Render the Curiosity symbol (question mark) as pixel art"""
    img = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    color = SuitColors.CURIOSITY['primary']
    s = size / 100

    # Question mark curve
    draw.arc([30*s, 15*s, 70*s, 50*s], 0, 180, fill=color, width=int(8*s))
    draw.line([(50*s, 50*s), (50*s, 65*s)], fill=color, width=int(8*s))

    # Dot
    draw.ellipse([44*s, 75*s, 56*s, 87*s], fill=color)

    return img


def render_suit_symbol_dance(size=64):
    """Render the Dance symbol (dancing figure) as pixel art"""
    img = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    color = SuitColors.DANCE['primary']
    s = size / 100

    # Head
    draw.ellipse([42*s, 15*s, 58*s, 31*s], fill=color)

    # Body (dynamic pose)
    draw.line([(50*s, 31*s), (50*s, 55*s)], fill=color, width=int(8*s))

    # Arms (spread wide)
    draw.line([(45*s, 38*s), (20*s, 45*s)], fill=color, width=int(7*s))
    draw.line([(55*s, 38*s), (80*s, 30*s)], fill=color, width=int(7*s))

    # Legs (mid-motion)
    draw.line([(50*s, 55*s), (35*s, 85*s)], fill=color, width=int(8*s))
    draw.line([(50*s, 55*s), (65*s, 85*s)], fill=color, width=int(8*s))

    # Feet
    draw.ellipse([30*s, 83*s, 40*s, 90*s], fill=color)
    draw.ellipse([60*s, 83*s, 70*s, 90*s], fill=color)

    return img
