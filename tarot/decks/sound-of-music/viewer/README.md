# The Sound of Music Tarot - Interactive Viewer

A React-based interactive browser for exploring The Sound of Music Tarot deck.

## Features

- **Introduction Page**: Detailed explanation of the deck's dialectical framework, suits, and visual language
- **Card Browser**: Grid view of all 75 cards with filtering and sorting
- **Card Details**: Click any card to see detailed information including:
  - High-resolution card image
  - Card meanings (upright and inverted)
  - Suit information
  - Visual descriptions
  - Card-specific questions

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Deck Structure

The viewer displays all 75 cards from The Sound of Music Tarot:

- **19 Major Arcana**: The 19 songs from the film, charting the narrative journey
- **56 Minor Arcana**: Four suits of 14 cards each

### The Four Suits

1. **Songs** (Authentic/Creative): Alpine meadow watercolors - spontaneous joy
2. **Mountains** (Authentic/Transmissive): Weathered stone - ancient wisdom
3. **Puppets** (Instrumental/Creative): Theatrical staging - craft and spectacle
4. **Whistles** (Instrumental/Transmissive): Naval precision - order and discipline

## Technologies

- React 18
- Vite
- CSS3 with modern features

## Project Structure

```
viewer/
├── public/
│   ├── cards/              # All card images (75 total)
│   └── sound-of-music-tarot.json  # Complete deck data
├── src/
│   ├── components/
│   │   ├── Introduction.jsx
│   │   ├── CardBrowser.jsx
│   │   └── CardModal.jsx
│   ├── App.jsx
│   └── index.css
└── package.json
```

## Created By

Myk & Claude • 2025

Exploring dialectics through The Sound of Music - How do we preserve authentic joy and love when instrumental forces demand our submission?
