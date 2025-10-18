#!/usr/bin/env python3
"""
Merge a tarot deck JSON file with the TarotDeckViewer template.

Usage:
    python3 merge_deck.py <deck.json> [output_dir]

Arguments:
    deck.json    - Path to the deck JSON file
    output_dir   - Output directory (default: /mnt/user-data/outputs)

Example:
    python3 merge_deck.py my-deck.json
    python3 merge_deck.py my-deck.json /mnt/user-data/outputs
"""

import json
import sys
from pathlib import Path

TEMPLATE_PATH = Path("/mnt/skills/user/custom-tarot-designer/assets/TarotDeckViewer.jsx")
PLACEHOLDER = '"$$REPLACE_ME_WITH_JSON$$";'
DEFAULT_OUTPUT_DIR = Path("/mnt/user-data/outputs")


def load_deck(deck_path):
    """Load and validate deck JSON."""
    try:
        with open(deck_path, 'r') as f:
            deck = json.load(f)
        
        # Basic validation
        required_keys = ['theme', 'dialectics', 'major_arcana', 'minor_arcana']
        for key in required_keys:
            if key not in deck:
                raise ValueError(f"Deck JSON missing required key: {key}")
        
        return deck
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {deck_path}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading deck: {e}")
        sys.exit(1)


def load_template():
    """Load the TarotDeckViewer template."""
    try:
        with open(TEMPLATE_PATH, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)


def merge_deck_with_template(deck, template):
    """Replace placeholder in template with deck JSON."""
    # Convert deck to JSON string with proper formatting
    deck_json = json.dumps(deck, indent=2)
    
    # Replace placeholder with deck JSON
    if PLACEHOLDER not in template:
        print(f"Error: Placeholder {PLACEHOLDER} not found in template")
        sys.exit(1)
    
    merged = template.replace(PLACEHOLDER, deck_json + ';')
    return merged


def save_output(content, output_path):
    """Save merged content to output file."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"✓ Created: {output_path}")
        print(f"  Lines: {len(content.splitlines())}")
        print(f"  Size: {len(content)} bytes")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    deck_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR
    
    if not deck_path.exists():
        print(f"Error: Deck file not found: {deck_path}")
        sys.exit(1)
    
    # Load deck and template
    print(f"Loading deck: {deck_path}")
    deck = load_deck(deck_path)
    theme_name = deck['theme']['name']
    print(f"  Theme: {theme_name}")
    
    print(f"Loading template: {TEMPLATE_PATH}")
    template = load_template()
    
    # Merge
    print("Merging deck with template...")
    merged = merge_deck_with_template(deck, template)
    
    # Save to output
    output_filename = "DeckViewer.jsx"
    output_path = output_dir / output_filename
    save_output(merged, output_path)
    
    print(f"\n✓ Success! Your deck viewer is ready.")
    print(f"\nNext steps:")
    print(f"  1. Create a React artifact from: {output_path}")
    print(f"  2. The artifact will include all 5 integrated views")
    print(f"  3. Generate visuals for cards as needed")


if __name__ == '__main__':
    main()
