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
    Draw a SIMPLE figure using circle head + polygon body (NO separate legs)
    The polygon shape itself conveys the posture and implies legs

    posture options: 'neutral', 'awkward', 'observing', 'moving'
    """
    draw = ImageDraw.Draw(canvas)

    s = scale  # Scale factor

    # Head - always a circle
    head_r = int(12 * s)
    draw.ellipse([x - head_r, y - int(90*s),
                  x + head_r, y - int(66*s)],
                 fill=palette.get('primary', (100, 100, 100)))

    # Body polygon - shape varies dramatically by posture
    # The body tapers down to imply legs without drawing them separately

    if posture == 'neutral':
        # Balanced, symmetrical, vertical
        body = [
            (x, y - int(65*s)),              # neck
            (x - int(14*s), y - int(45*s)),  # left shoulder
            (x - int(12*s), y - int(10*s)),  # left hip
            (x - int(6*s), y),               # left foot
            (x + int(6*s), y),               # right foot
            (x + int(12*s), y - int(10*s)),  # right hip
            (x + int(14*s), y - int(45*s)),  # right shoulder
        ]

    elif posture == 'awkward':
        # Hunched, angular, off-balance, head forward
        # Shoulders pulled in, uneven stance
        body = [
            (x + int(5*s), y - int(65*s)),   # neck (forward)
            (x - int(8*s), y - int(50*s)),   # left shoulder (hunched up)
            (x - int(10*s), y - int(12*s)),  # left hip
            (x - int(8*s), y),               # left foot (pigeon-toed)
            (x + int(4*s), y),               # right foot
            (x + int(8*s), y - int(15*s)),   # right hip (uneven)
            (x + int(10*s), y - int(48*s)),  # right shoulder (hunched)
        ]

    elif posture == 'observing':
        # Slight lean, attentive, weight shifted
        # One shoulder slightly raised
        body = [
            (x - int(2*s), y - int(65*s)),   # neck (slight lean)
            (x - int(16*s), y - int(48*s)),  # left shoulder (raised)
            (x - int(14*s), y - int(8*s)),   # left hip
            (x - int(8*s), y),               # left foot
            (x + int(4*s), y),               # right foot (weight shifted)
            (x + int(10*s), y - int(12*s)),  # right hip (lower)
            (x + int(12*s), y - int(42*s)),  # right shoulder (lower)
        ]

    elif posture == 'moving':
        # Dynamic, tilted, asymmetric, energy
        # Clear diagonal, one side extended
        body = [
            (x + int(8*s), y - int(65*s)),   # neck (tilted)
            (x - int(18*s), y - int(38*s)),  # left shoulder (extended back)
            (x - int(10*s), y - int(5*s)),   # left hip
            (x - int(3*s), y),               # left foot
            (x + int(12*s), y),              # right foot (forward)
            (x + int(18*s), y - int(15*s)),  # right hip (forward)
            (x + int(20*s), y - int(50*s)),  # right shoulder (forward)
        ]

    else:
        # Default to neutral
        body = [
            (x, y - int(65*s)),
            (x - int(14*s), y - int(45*s)),
            (x - int(12*s), y - int(10*s)),
            (x - int(6*s), y),
            (x + int(6*s), y),
            (x + int(12*s), y - int(10*s)),
            (x + int(14*s), y - int(45*s)),
        ]

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

    # Question mark: the hook is 3/4 of a circle, missing the upper-left quarter
    # In PIL, arcs go counter-clockwise from start to end angle
    # 0°=right, 90°=top, 180°=left, 270°=bottom
    # We want: left side → bottom → right side → top
    # That's 180° → 270° → 0° → 90° (counter-clockwise)
    # So: start=180, end=90
    draw.arc([38*s, 18*s, 62*s, 48*s], 180, 90, fill=color, width=int(9*s))

    # Vertical stem dropping from bottom-center of the hook
    draw.line([(50*s, 48*s), (50*s, 68*s)], fill=color, width=int(9*s))

    # Dot at bottom
    draw.ellipse([44*s, 76*s, 56*s, 88*s], fill=color)

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


# =============================================================================
# HUMAN FIGURE PRINCIPLES
# =============================================================================

"""
REPRESENTING HUMANS IN THE BYRNE JOURNEY TAROT

General Principles:
- Body language carries meaning: rigid/geometric → fluid/organic reflects the journey
- Figures are simplified but expressive
- Scale indicates relationship to environment (small = observed, large = present)
- Faces are minimal - the body tells the story

Specific Characters:

BYRNE (when depicted as himself):
- The Big Suit: Oversized boxy jacket - the key identifier
- Purpose of big suit: Makes the head smaller relative to the body
- This represents escaping cognitive prison - less head, more body
- Progression concept: Suit could get bigger / head could get smaller as ranks increase
- Posture evolution: Stiff/angular/upright (early) → loose/tilted/dancing (late)
- Often in performance stance, conducting, presenting, or mid-gesture
- Arms stay INSIDE jacket - the whole jacket shape shows movement

AUDIENCE/CROWD:
- Can be geometric (early: observed patterns) or organic (late: felt presence)
- Repetition with variation
- May be abstracted to dots, shapes, or simplified figures

GENERIC FIGURES:
- Match the era's aesthetic (geometric vs organic)
- Posture reflects card meaning
- Can be silhouettes or more detailed depending on focus

Visual Shortcuts:
- Big boxy jacket (head-to-body ratio) = Byrne
- Suit and tie = formal/structured self
- Loose clothing = relaxed/authentic self
- Multiple identical figures = pattern observation
- Varied figures together = genuine community

Standard Simple Figure Approach:
- Circle head + polygon body (NO separate legs)
- Legs implied by body polygon tapering to feet
- Posture conveyed through polygon shape and angle
- This keeps the style consistent and distinctive
"""


# =============================================================================
# COMMON VISUAL ELEMENTS
# =============================================================================

def example_urban_building(draw, x, y, width, height, palette, style='simple'):
    """
    Urban building - various styles
    style: 'simple', 'detailed', 'geometric'
    """
    if style == 'geometric':
        # Very clean, architectural
        draw.rectangle([x, y, x + width, y + height],
                       fill=palette.get('secondary', (120, 120, 120)),
                       outline=palette.get('grid', (100, 100, 100)), width=2)
        # Grid windows
        for wy in range(y + 20, y + height - 10, 30):
            for wx in range(x + 15, x + width - 10, 25):
                draw.rectangle([wx, wy, wx + 10, wy + 15],
                             fill=palette.get('accent', (80, 90, 100)))
    else:
        # Simple building
        draw.rectangle([x, y, x + width, y + height],
                       fill=palette.get('secondary', (120, 120, 120)))
        # Scattered windows
        window_color = palette.get('accent', (80, 90, 100))
        for wy in range(y + 15, y + height, 25):
            for wx in range(x + 10, x + width - 10, 20):
                draw.rectangle([wx, wy, wx + 8, wy + 12], fill=window_color)


def example_stage_elements(draw, x, y, width, palette):
    """
    Performance stage elements - lights, speakers, etc.
    """
    # Stage floor
    draw.rectangle([x, y, x + width, y + 40],
                   fill=palette.get('ground', (100, 100, 100)))

    # Speakers (boxes with grills)
    speaker_color = palette.get('shadow', (40, 40, 40))
    # Left speaker
    draw.rectangle([x + 10, y - 60, x + 40, y], fill=speaker_color)
    # Grill
    for i in range(5):
        draw.line([(x + 15, y - 50 + i*10), (x + 35, y - 50 + i*10)],
                  fill=palette.get('secondary', (80, 80, 80)), width=2)

    # Right speaker
    draw.rectangle([x + width - 40, y - 60, x + width - 10, y], fill=speaker_color)
    for i in range(5):
        draw.line([(x + width - 35, y - 50 + i*10), (x + width - 15, y - 50 + i*10)],
                  fill=palette.get('secondary', (80, 80, 80)), width=2)


def example_musical_elements(canvas, x, y, palette):
    """
    Musical notation elements - notes, staves, etc.
    These are symbols, not literal sheet music
    """
    draw = ImageDraw.Draw(canvas)

    # Musical note
    note_color = palette.get('primary', (50, 50, 50))

    # Note head (filled circle)
    draw.ellipse([x, y + 15, x + 12, y + 25], fill=note_color)

    # Stem
    draw.line([(x + 11, y + 20), (x + 11, y - 10)], fill=note_color, width=2)

    # Flag (eighth note)
    draw.arc([x + 11, y - 15, x + 25, y], 180, 360, fill=note_color, width=3)


def example_grid_structure(draw, bounds, palette, style='blueprint'):
    """
    Structural grids - useful for Structures suit
    style: 'blueprint', 'loose', 'perspective'
    """
    x1, y1, x2, y2 = bounds

    if style == 'blueprint':
        # Precise grid
        grid_color = palette.get('grid', (120, 140, 160))
        spacing = 30
        # Vertical
        for x in range(x1, x2, spacing):
            draw.line([(x, y1), (x, y2)], fill=grid_color, width=1)
        # Horizontal
        for y in range(y1, y2, spacing):
            draw.line([(x1, y), (x2, y)], fill=grid_color, width=1)

        # Thicker lines every 90px
        for x in range(x1, x2, 90):
            draw.line([(x, y1), (x, y2)], fill=grid_color, width=2)
        for y in range(y1, y2, 90):
            draw.line([(x1, y), (x2, y)], fill=grid_color, width=2)


def example_doorway_threshold(draw, x, y, width, height, palette):
    """
    Doorway/threshold - recurring motif for transitions
    """
    frame_color = palette.get('shadow', (40, 40, 40))
    light_color = palette.get('highlight', (220, 220, 200))

    # Light beyond doorway
    draw.rectangle([x + 15, y, x + width - 15, y + height],
                   fill=light_color)

    # Doorframe
    # Top
    draw.rectangle([x, y, x + width, y + 15], fill=frame_color)
    # Left
    draw.rectangle([x, y, x + 15, y + height], fill=frame_color)
    # Right
    draw.rectangle([x + width - 15, y, x + width, y + height], fill=frame_color)


# =============================================================================
# SETTING TYPES
# =============================================================================

"""
COMMON SETTINGS IN THE BYRNE JOURNEY TAROT

CITY STREET (urban observation):
- SUGGESTIVE container, not literal scene
- Buildings partially frame edges (leaving center open for life)
- Sky, ground plane, architectural hints
- The middle space is where figures and action go
- Used in: Early cards, Structures suit

PERFORMANCE STAGE:
- Raised platform
- Lighting elements
- Speakers/equipment
- Audience space
- Used in: Late cards, Dance suit

AERIAL VIEW (detached observation):
- Looking down from above
- Nature (greens, blues) intersecting with human structures
- The Big Country: grid-free nature + sparse human habitation
- Detached observation of natural and built systems
- Used in: Early-mid cards, "The Big Country"

INTERIOR DOMESTIC:
- Rooms with furniture/objects
- Windows looking out
- Organized/controlled space
- Used in: "Don't Worry About the Government", Structures

NATURAL LANDSCAPE:
- Rivers, patterns in nature
- Organic flows and curves
- Earth tones
- Used in: Rivers suit, transition cards

COLLABORATIVE SPACE:
- Open, inclusive composition
- Multiple figures with room to move
- Bright, welcoming
- Used in: Late cards, Curiosity suit, Dance suit
"""


def generate_setting_example(setting_type, palette):
    """
    Generate example of a setting type
    Returns an image showing that kind of space
    """
    canvas = create_canvas(palette.get('primary', (200, 200, 200)))
    draw = ImageDraw.Draw(canvas)

    if setting_type == 'city_street':
        # SUGGESTIVE, not literal - leave space for life
        # Hint of buildings framing the edges (partial, not dominant)
        building_color = palette.get('secondary', (120, 120, 120))

        # Left edge - partial building suggestion
        draw.rectangle([0, 100, 50, CARD_HEIGHT], fill=building_color)
        # A few windows to indicate it's a building
        for wy in range(140, 380, 60):
            draw.rectangle([15, wy, 23, wy+15], fill=palette.get('accent', (80, 90, 100)))
            draw.rectangle([27, wy, 35, wy+15], fill=palette.get('accent', (80, 90, 100)))

        # Right edge - partial building suggestion
        draw.rectangle([CARD_WIDTH - 50, 80, CARD_WIDTH, CARD_HEIGHT], fill=building_color)
        for wy in range(120, 380, 60):
            draw.rectangle([CARD_WIDTH - 35, wy, CARD_WIDTH - 27, wy+15],
                          fill=palette.get('accent', (80, 90, 100)))
            draw.rectangle([CARD_WIDTH - 23, wy, CARD_WIDTH - 15, wy+15],
                          fill=palette.get('accent', (80, 90, 100)))

        # Ground/pavement - subtle, at bottom
        draw.rectangle([0, CARD_HEIGHT - 40, CARD_WIDTH, CARD_HEIGHT],
                      fill=palette.get('ground', (150, 155, 160)))
        # Sidewalk edge line
        draw.line([(0, CARD_HEIGHT - 40), (CARD_WIDTH, CARD_HEIGHT - 40)],
                 fill=palette.get('shadow', (100, 100, 100)), width=2)

        # Sky at top (pale, receding)
        for y in range(0, 120):
            t = y / 120
            base_color = palette.get('primary', (240, 240, 240))
            sky_color = (200, 210, 220)
            r = int(sky_color[0] + (base_color[0] - sky_color[0]) * t)
            g = int(sky_color[1] + (base_color[1] - sky_color[1]) * t)
            b = int(sky_color[2] + (base_color[2] - sky_color[2]) * t)
            draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

        # The MIDDLE is open - this is where the life happens

    elif setting_type == 'stage':
        # Stage platform
        draw.polygon([
            (40, CARD_HEIGHT - 150),
            (CARD_WIDTH - 40, CARD_HEIGHT - 150),
            (CARD_WIDTH - 20, CARD_HEIGHT),
            (20, CARD_HEIGHT)
        ], fill=palette.get('secondary', (100, 80, 60)))
        # Equipment
        example_stage_elements(draw, 40, CARD_HEIGHT - 150, CARD_WIDTH - 80, palette)

    elif setting_type == 'aerial':
        # The Big Country - nature + human habitation from above
        # Natural greens and blues with geometric human structures

        # Sky/background - pale blue
        for y in range(CARD_HEIGHT):
            t = y / CARD_HEIGHT
            r = int(180 + (140 - 180) * t)
            g = int(200 + (170 - 200) * t)
            b = int(220 + (160 - 220) * t)
            draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

        # Natural landscape patches (greens)
        draw.ellipse([30, 80, 140, 180], fill=(120, 160, 100))
        draw.ellipse([160, 140, 260, 260], fill=(100, 145, 85))

        # River or water (blue)
        flow_points = []
        for x in range(0, CARD_WIDTH, 5):
            y_center = 200 + 30 * math.sin(x / 40)
            flow_points.append((x, y_center - 15))
        for x in range(CARD_WIDTH, 0, -5):
            y_center = 200 + 30 * math.sin(x / 40)
            flow_points.append((x, y_center + 15))
        draw.polygon(flow_points, fill=(90, 140, 180))

        # Human structures (geometric, sparse)
        draw.rectangle([60, 120, 85, 150], fill=palette.get('secondary', (120, 120, 120)))
        draw.rectangle([180, 200, 200, 225], fill=palette.get('secondary', (120, 120, 120)))
        # Road/grid (sparse, intersecting with nature)
        draw.line([(0, 100), (CARD_WIDTH, 100)], fill=(140, 140, 140), width=3)
        draw.line([(100, 0), (100, CARD_HEIGHT)], fill=(140, 140, 140), width=3)

    elif setting_type == 'interior':
        # Room frame
        draw.rectangle([30, 40, CARD_WIDTH - 30, CARD_HEIGHT - 40],
                       outline=palette.get('frame', (80, 80, 80)), width=3)
        # Window
        draw.rectangle([CARD_WIDTH - 100, 60, CARD_WIDTH - 50, 140],
                       fill=palette.get('highlight', (220, 230, 240)))
        # Simple furniture
        draw.rectangle([50, CARD_HEIGHT - 120, 110, CARD_HEIGHT - 60],
                       fill=palette.get('secondary', (100, 90, 80)))

    elif setting_type == 'natural':
        # Outdoor nature scene - sky, land, organic elements

        # Sky - gradient from pale to deeper
        for y in range(0, CARD_HEIGHT // 2):
            t = y / (CARD_HEIGHT // 2)
            r = int(180 + (140 - 180) * t)
            g = int(210 + (170 - 210) * t)
            b = int(230 + (190 - 230) * t)
            draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))

        # Distant hills/mountains (organic curves)
        hill_color = (100, 130, 110)
        # Far hills
        hill_points_far = []
        for x in range(0, CARD_WIDTH + 20, 15):
            y_var = 20 * math.sin(x / 60) + 15 * math.cos(x / 35)
            hill_points_far.append((x, CARD_HEIGHT // 3 + y_var))
        hill_points_far.append((CARD_WIDTH, CARD_HEIGHT))
        hill_points_far.append((0, CARD_HEIGHT))
        draw.polygon(hill_points_far, fill=hill_color)

        # Closer hills (darker, more variation)
        hill_color_close = (80, 110, 85)
        hill_points_close = []
        for x in range(0, CARD_WIDTH + 20, 12):
            y_var = 30 * math.sin(x / 50 + 2) + 20 * math.cos(x / 28)
            hill_points_close.append((x, CARD_HEIGHT // 2 + y_var))
        hill_points_close.append((CARD_WIDTH, CARD_HEIGHT))
        hill_points_close.append((0, CARD_HEIGHT))
        draw.polygon(hill_points_close, fill=hill_color_close)

        # Foreground - grass/vegetation hints
        grass_color = (95, 125, 90)
        draw.rectangle([0, CARD_HEIGHT * 2 // 3, CARD_WIDTH, CARD_HEIGHT],
                      fill=grass_color)

        # Some vegetation texture (organic irregular shapes)
        vegetation_dark = (75, 100, 70)
        import random
        random.seed(42)
        for i in range(15):
            x = random.randint(10, CARD_WIDTH - 30)
            y = random.randint(CARD_HEIGHT * 2 // 3, CARD_HEIGHT - 20)
            # Irregular organic blob shapes
            blob_points = []
            for angle in range(0, 360, 40):
                rad = math.radians(angle)
                r = random.randint(8, 18)
                blob_points.append((x + r * math.cos(rad), y + r * math.sin(rad)))
            draw.polygon(blob_points, fill=vegetation_dark)

    elif setting_type == 'collaborative':
        # Open bright space
        for y in range(CARD_HEIGHT):
            t = y / CARD_HEIGHT
            bright = palette.get('highlight', (240, 240, 220))
            base = palette.get('dialogue', (200, 210, 220))
            r = int(bright[0] + (base[0] - bright[0]) * t)
            g = int(bright[1] + (base[1] - bright[1]) * t)
            b = int(bright[2] + (base[2] - bright[2]) * t)
            draw.line([(0, y), (CARD_WIDTH, y)], fill=(r, g, b))
        # Simple circular gathering space
        draw.ellipse([CARD_WIDTH//2 - 80, CARD_HEIGHT//2 - 60,
                     CARD_WIDTH//2 + 80, CARD_HEIGHT//2 + 60],
                    outline=palette.get('accent', (180, 180, 180)), width=3)

    return canvas
