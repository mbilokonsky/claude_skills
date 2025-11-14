#!/usr/bin/env python3
"""
Assemble the complete Sound of Music Tarot deck from component JSON files.
"""

import json
from pathlib import Path

# Load all component files
def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Component files
suits_design = load_json('suits-design.json')
minor_ranks = load_json('minor-ranks-design.json')
major_arcana_design = load_json('major-arcana-design.json')
major_arcana_cards = load_json('major-arcana-cards.json')
songs_cards = load_json('songs-suit-cards.json')
mountains_cards = load_json('mountains-suit-cards.json')
puppets_cards = load_json('puppets-suit-cards.json')
whistles_cards = load_json('whistles-suit-cards.json')

# Build the complete deck
deck = {
    "name": "The Sound of Music Tarot",
    "slug": "sound-of-music-tarot",
    "version": "1.0.0",
    "theme": {
        "name": "The Sound of Music",
        "description": "A tarot deck exploring the dialectics of authenticity vs. instrumentality and creation vs. transmission through the story of The Sound of Music. The deck examines how fascism operates as instrumental creation masquerading as authentic transmission - an epistemic attack on meaning itself. Through Maria's authentic creativity, Georg's authentic transmission, and the looming shadow of fascism corrupting both puppetry and discipline, the deck asks: how do we preserve authentic joy and love when instrumental forces demand our submission?",
        "creator": "Myk & Claude"
    },
    "suits": {},
    "ranks": {},
    "major_arcana": major_arcana_design['major_arcana'],
    "cards": {}
}

# Add suits (convert from nested structure to flat keyed structure)
for suit_name in ['songs', 'mountains', 'puppets', 'whistles']:
    suit_data = suits_design['suits'][suit_name]
    deck['suits'][suit_name] = {
        "name": suit_data['name'],
        "slug": suit_name,
        "description": suit_data.get('description', ''),
        "symbol": suit_data['symbol'],
        "meaning": suit_data['meanings'],
        "visual_style": suit_data['visual_style']
    }

# Add minor ranks
for rank_data in minor_ranks['numbered_ranks']:
    rank_slug = rank_data['slug']
    deck['ranks'][rank_slug] = rank_data

for rank_data in minor_ranks['face_ranks']:
    rank_slug = rank_data['slug']
    deck['ranks'][rank_slug] = rank_data

# Add major arcana cards
for card in major_arcana_cards['major_arcana_cards']:
    card_slug = card['slug']
    deck['cards'][card_slug] = card

# Add minor arcana cards
for suit_cards, suit_slug in [
    (songs_cards['songs_suit_cards'], 'songs'),
    (mountains_cards['mountains_suit_cards'], 'mountains'),
    (puppets_cards['puppets_suit_cards'], 'puppets'),
    (whistles_cards['whistles_suit_cards'], 'whistles')
]:
    for card in suit_cards:
        card_slug = card['slug']
        deck['cards'][card_slug] = card

# Write the complete deck
with open('sound-of-music-tarot.json', 'w') as f:
    json.dump(deck, f, indent=2)

print(f"Complete deck assembled: {len(deck['cards'])} cards total")
print(f"  - {len([c for c in deck['cards'].values() if c.get('type') == 'major'])} Major Arcana")
print(f"  - {len([c for c in deck['cards'].values() if c.get('type') == 'minor'])} Minor Arcana")
print(f"Saved to: sound-of-music-tarot.json")
