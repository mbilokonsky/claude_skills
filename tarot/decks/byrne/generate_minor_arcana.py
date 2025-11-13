#!/usr/bin/env python3
"""
Generate all Minor Arcana cards for the Byrne Journey Tarot
56 cards total: 14 cards × 4 suits (Structures, Rivers, Curiosity, Dance)
"""

import json
import sys
import os
from PIL import Image, ImageDraw
import math
import random

# Add the visuals directory to path
sys.path.insert(0, '/home/user/claude_skills/tarot/decks/byrne/visuals')
import byrne_visual_toolkit as bvt

# Dimensions
WIDTH = 280
HEIGHT = 420

def load_deck_data():
    """Load the deck JSON"""
    with open('/home/user/claude_skills/tarot/decks/byrne/byrne-journey-tarot.json', 'r') as f:
        return json.load(f)

def generate_structures_card(card_data, rank):
    """
    Generate a Structures suit card
    Visual style: Clean geometric, architectural, cool grays, precise lines and grids
    """
    palette = bvt.SuitColors.STRUCTURES
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Grid background (subtle)
    bvt.draw_grid_pattern(draw, (20, 20, WIDTH - 20, HEIGHT - 20), 40, palette['grid'])

    # Rank-specific visual elements
    if rank == 0:  # Ace - seed of analysis
        # Single clean line on white space
        draw.line([(WIDTH//2, 80), (WIDTH//2, HEIGHT - 80)], fill=palette['frame'], width=4)
        draw.line([(60, HEIGHT//2), (WIDTH - 60, HEIGHT//2)], fill=palette['frame'], width=4)
        # Center point
        draw.ellipse([WIDTH//2 - 10, HEIGHT//2 - 10, WIDTH//2 + 10, HEIGHT//2 + 10], fill=palette['accent'])

    elif rank in [1, 2]:  # Two/Three - choosing frameworks, taxonomy emerging
        # Multiple architectural elements
        num_elements = rank + 1
        spacing = (WIDTH - 80) // num_elements
        for i in range(num_elements):
            x = 40 + i * spacing + spacing // 2
            y = HEIGHT // 2
            # Simple building frames
            bvt.example_building(img, x - 25, y - 60, 50, 100, palette)

    elif rank in [3, 4, 5]:  # Four/Five/Six - stable system, challenged, revised
        # Four-square structure
        size = 60
        margin = 30
        positions = [
            (margin + size//2, HEIGHT//2 - 40 - size//2),
            (WIDTH - margin - size//2, HEIGHT//2 - 40 - size//2),
            (margin + size//2, HEIGHT//2 + 40 + size//2),
            (WIDTH - margin - size//2, HEIGHT//2 + 40 + size//2)
        ]
        for i, (x, y) in enumerate(positions[:rank]):
            if rank == 4 and i == 3:  # Five - show crack
                draw.rectangle([x - size//2, y - size//2, x + size//2, y + size//2],
                             outline=palette['secondary'], width=3)
                draw.line([(x - size//2, y - size//2), (x + size//2, y + size//2)],
                         fill=palette['shadow'], width=2)
            else:
                draw.rectangle([x - size//2, y - size//2, x + size//2, y + size//2],
                             fill=palette['secondary'], outline=palette['frame'], width=2)

    elif rank in [6, 7, 8]:  # Seven/Eight/Nine - meta-analysis, perfected, completion
        # Blueprint/floor plan view
        bvt.example_grid_structure(draw, (40, 80, WIDTH - 40, HEIGHT - 80), palette, style='blueprint')
        # Add figure examining (for rank 6)
        if rank == 6:
            bvt.example_figure_simple(img, WIDTH//2, HEIGHT - 80, palette, posture='observing', scale=0.9)

    else:  # Ten+ - Court cards and higher numbers
        # Complex architectural composition
        bvt.example_urban_building(draw, 50, HEIGHT//2 - 80, 70, 160, palette, style='geometric')
        bvt.example_urban_building(draw, WIDTH - 120, HEIGHT//2 - 60, 70, 140, palette, style='simple')
        # Add figure(s) for court cards
        if rank >= 10:
            scale = 0.7 + (rank - 10) * 0.15
            bvt.example_figure_simple(img, WIDTH//2, HEIGHT - 70, palette, posture='neutral', scale=scale)

    # Suit symbol in corner
    symbol = bvt.render_suit_symbol_structures(48)
    img.paste(symbol, (WIDTH - 60, 15), symbol if symbol.mode == 'RGBA' else None)

    return img

def generate_rivers_card(card_data, rank):
    """
    Generate a Rivers suit card
    Visual style: Organic patterns, polyrhythmic layering, warm earth tones, flow
    """
    palette = bvt.SuitColors.RIVERS
    img = bvt.create_canvas(palette['primary'])
    draw = ImageDraw.Draw(img)

    # Rank determines complexity of flow patterns
    num_flows = min(rank + 1, 8)

    if rank == 0:  # Ace - seed of rhythm
        # Single pure flow
        bvt.draw_flow_pattern(draw, (40, HEIGHT//2 - 30, WIDTH - 40, HEIGHT//2 + 30),
                             60, 20, palette['flow'])

    elif rank <= 3:  # Early ranks - simple patterns
        for i in range(num_flows):
            y_offset = 60 + i * (HEIGHT - 120) // num_flows
            wavelength = 50 + i * 10
            amplitude = 15 + (i % 3) * 5
            bvt.draw_flow_pattern(draw, (20, y_offset, WIDTH - 20, y_offset + 30),
                                 wavelength, amplitude, palette['flow'])

    elif rank <= 6:  # Middle ranks - polyrhythmic layering
        # Multiple overlapping patterns
        for i in range(num_flows):
            y_offset = 50 + i * 45
            wavelength = 40 + i * 8
            amplitude = 12 + (i % 4) * 4
            alpha_color = palette['pattern'] if i % 2 == 0 else palette['flow']
            bvt.draw_flow_pattern(draw, (15, y_offset, WIDTH - 15, y_offset + 25),
                                 wavelength, amplitude, alpha_color)

    elif rank <= 9:  # Later ranks - complex systems
        # Natural landscape elements
        # Hills/waves
        for layer in range(4):
            y_base = HEIGHT - 100 + layer * 20
            hill_points = [(0, y_base)]
            for x in range(0, WIDTH + 20, 15):
                y_var = 15 * math.sin(x / (40 + layer * 10)) + 10 * math.cos(x / (25 + layer * 5))
                hill_points.append((x, y_base + y_var))
            hill_points.append((WIDTH, HEIGHT))
            hill_points.append((0, HEIGHT))
            draw.polygon(hill_points, fill=palette['pattern'] if layer % 2 else palette['secondary'])

    else:  # High ranks and court cards
        # Full natural system with figure(s)
        # Organic landscape
        for layer in range(3):
            y_base = HEIGHT // 2 + layer * 40
            hill_points = [(0, y_base)]
            for x in range(0, WIDTH + 20, 12):
                y_var = 20 * math.sin(x / (50 + layer * 15))
                hill_points.append((x, y_base + y_var))
            hill_points.append((WIDTH, HEIGHT))
            hill_points.append((0, HEIGHT))
            draw.polygon(hill_points, fill=palette['secondary'])

        # Add figure(s)
        if rank >= 10:
            scale = 0.6 + (rank - 10) * 0.12
            bvt.example_figure_simple(img, WIDTH//2, HEIGHT - 60, palette, posture='observing', scale=scale)

    # Suit symbol
    symbol = bvt.render_suit_symbol_rivers(48)
    img.paste(symbol, (WIDTH - 60, 15), symbol if symbol.mode == 'RGBA' else None)

    return img

def generate_curiosity_card(card_data, rank):
    """
    Generate a Curiosity suit card
    Visual style: Bright optimistic, conversational, open inviting spaces
    """
    palette = bvt.SuitColors.CURIOSITY
    img = bvt.create_canvas(palette['dialogue'])
    draw = ImageDraw.Draw(img)

    # Bright gradient background
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(palette['secondary'][0] + (palette['primary'][0] - palette['secondary'][0]) * t)
        g = int(palette['secondary'][1] + (palette['primary'][1] - palette['secondary'][1]) * t)
        b = int(palette['secondary'][2] + (palette['primary'][2] - palette['secondary'][2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    if rank == 0:  # Ace - seed of inquiry
        # Question mark centered
        symbol = bvt.render_suit_symbol_curiosity(96)
        img.paste(symbol, (WIDTH//2 - 48, HEIGHT//2 - 48), symbol if symbol.mode == 'RGBA' else None)

    elif rank <= 3:  # Early ranks - simple dialogue spaces
        num_spaces = rank + 1
        for i in range(num_spaces):
            x = 40 + (i * (WIDTH - 80) // num_spaces)
            y = 80 + (i % 2) * 120
            size = 50
            draw.rectangle([x, y, x + size, y + size], fill=palette['accent'])

    elif rank <= 6:  # Middle ranks - civic structures
        # Open civic space (town square feeling)
        # Ground
        draw.rectangle([0, HEIGHT - 100, WIDTH, HEIGHT], fill=palette['shadow'])

        # Buildings framing (not filling)
        draw.rectangle([20, HEIGHT // 2, 60, HEIGHT - 100], fill=palette['accent'])
        draw.rectangle([WIDTH - 60, HEIGHT // 2 + 20, WIDTH - 20, HEIGHT - 100], fill=palette['accent'])

    elif rank <= 9:  # Later ranks - collaborative spaces
        # Multiple figures in conversation
        num_figures = min(rank - 5, 4)
        spacing = WIDTH // (num_figures + 1)
        for i in range(num_figures):
            x = spacing * (i + 1)
            y = HEIGHT - 90
            posture = 'observing' if i % 2 == 0 else 'neutral'
            bvt.example_figure_simple(img, x, y, palette, posture=posture, scale=0.8)

        # Dialogue lines between figures
        for i in range(num_figures - 1):
            x1 = spacing * (i + 1)
            x2 = spacing * (i + 2)
            y = HEIGHT - 140
            draw.line([(x1, y), (x2, y)], fill=palette['text'], width=2)

    else:  # High ranks and court cards
        # Full community scene
        # Ground/platform
        draw.polygon([
            (30, HEIGHT - 120),
            (WIDTH - 30, HEIGHT - 120),
            (WIDTH - 20, HEIGHT - 40),
            (20, HEIGHT - 40)
        ], fill=palette['accent'])

        # Multiple figures
        num_figures = min(rank - 7, 5)
        for i in range(num_figures):
            x = 50 + i * 45
            y = HEIGHT - 90 - (i % 2) * 15
            scale = 0.7 + (i % 3) * 0.1
            bvt.example_figure_simple(img, x, y, palette, posture='moving', scale=scale)

    # Suit symbol
    symbol = bvt.render_suit_symbol_curiosity(48)
    img.paste(symbol, (WIDTH - 60, 15), symbol if symbol.mode == 'RGBA' else None)

    return img

def generate_dance_card(card_data, rank):
    """
    Generate a Dance suit card
    Visual style: Dynamic motion, vibrant warm colors, energy and heat visible
    """
    palette = bvt.SuitColors.DANCE
    img = bvt.create_canvas(palette['shadow'])
    draw = ImageDraw.Draw(img)

    # Energy center
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    if rank == 0:  # Ace - seed of movement
        # Single radial burst
        bvt.radial_gradient(draw, center_x, center_y, 100, palette['heat'], palette['shadow'])
        # Single dancing figure
        bvt.example_figure_simple(img, center_x, HEIGHT - 80, palette, posture='moving', scale=1.0)

    elif rank <= 3:  # Early ranks - beginning movement
        # Smaller radial energy
        bvt.radial_gradient(draw, center_x, center_y, 120, palette['heat'], palette['shadow'])

        # Multiple figures beginning to move
        num_figures = rank + 1
        for i in range(num_figures):
            angle = (i / num_figures) * math.pi * 2
            distance = 80
            x = center_x + int(distance * math.cos(angle))
            y = HEIGHT - 70 + int(20 * math.sin(angle))
            bvt.example_figure_simple(img, x, y, palette, posture='moving', scale=0.7)

    elif rank <= 6:  # Middle ranks - building energy
        # Larger radial gradient
        bvt.radial_gradient(draw, center_x, center_y + 30, 150, palette['heat'], palette['shadow'])

        # Energy lines
        for i in range(8):
            angle = i * math.pi / 4
            length = 60 + rank * 5
            end_x = center_x + int(length * math.cos(angle))
            end_y = center_y + int(length * math.sin(angle))
            draw.line([(center_x, center_y), (end_x, end_y)], fill=palette['electric'], width=3)

        # Figures in motion
        num_figures = min(rank, 4)
        for i in range(num_figures):
            x = 50 + i * 60
            y = HEIGHT - 70
            bvt.example_figure_simple(img, x, y, palette, posture='moving', scale=0.8)

    elif rank <= 9:  # Later ranks - full groove
        # Maximum radial energy
        bvt.radial_gradient(draw, center_x, center_y, 180, palette['heat'], palette['shadow'])

        # Heat waves
        for i in range(10):
            y = 40 + i * 35
            for x in range(0, WIDTH, 30):
                offset = 12 * math.sin((x + y) / 15)
                draw.line([(x + offset, y), (x + 25 + offset, y)], fill=palette['electric'], width=2)

        # Multiple figures dancing
        num_figures = min(rank - 3, 5)
        for i in range(num_figures):
            x = 40 + i * 50
            y = HEIGHT - 80 + (i % 2) * 20
            scale = 0.7 + (i % 3) * 0.15
            bvt.example_figure_simple(img, x, y, palette, posture='moving', scale=scale)

    else:  # High ranks and court cards
        # Full performance energy
        bvt.radial_gradient(draw, center_x, center_y + 20, 200, palette['heat'], palette['shadow'])

        # Stage elements
        bvt.example_stage_elements(draw, center_x, HEIGHT - 40, 200, palette)

        # Multiple figures in full dance
        positions = [
            (70, HEIGHT - 70), (140, HEIGHT - 85), (210, HEIGHT - 75)
        ]
        for i, (x, y) in enumerate(positions[:min(rank - 8, 3)]):
            scale = 0.9 + (i % 2) * 0.2
            bvt.example_figure_simple(img, x, y, palette, posture='moving', scale=scale)

        # Musical elements
        for i in range(3):
            bvt.example_musical_elements(img, 40 + i * 80, 60, palette)

    # Suit symbol
    symbol = bvt.render_suit_symbol_dance(48)
    img.paste(symbol, (WIDTH - 60, 15), symbol if symbol.mode == 'RGBA' else None)

    return img

def main():
    """Generate all 56 Minor Arcana cards"""
    print("Loading deck data...")
    deck_data = load_deck_data()

    # Create output directory
    output_dir = '/home/user/claude_skills/tarot/decks/byrne/cards'
    os.makedirs(output_dir, exist_ok=True)

    # Suits configuration
    suits = [
        ('structures', generate_structures_card),
        ('rivers', generate_rivers_card),
        ('curiosity', generate_curiosity_card),
        ('dance', generate_dance_card)
    ]

    total_cards = 0
    print(f"\nGenerating 56 Minor Arcana cards (14 per suit × 4 suits)...\n")

    for suit_name, generator_func in suits:
        print(f"Generating {suit_name.upper()} suit (14 cards):")

        for rank in range(14):  # 0-13
            card_key = f"{suit_name}-{rank}"
            card_data = deck_data['cards'].get(card_key, {})

            card_name = card_data.get('name', f'{suit_name}-{rank}')
            print(f"  [{rank+1}/14] {card_name}...")

            img = generator_func(card_data, rank)
            output_path = os.path.join(output_dir, f'{suit_name}-{rank:02d}.png')
            img.save(output_path)

            total_cards += 1

        print()

    print(f"✓ All {total_cards} Minor Arcana cards generated successfully!")
    print(f"  Location: {output_dir}/")
    print(f"  Files: structures-00.png through dance-13.png")

if __name__ == '__main__':
    main()
