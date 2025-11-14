import { useState, useMemo } from 'react'
import './CardBrowser.css'
import CardModal from './CardModal'

function CardBrowser({ deckData }) {
  const [selectedCard, setSelectedCard] = useState(null)
  const [filter, setFilter] = useState('all')
  const [sortBy, setSortBy] = useState('position')

  const cards = useMemo(() => {
    const allCards = Object.entries(deckData.cards).map(([slug, card]) => ({
      slug,
      ...card
    }))

    let filtered = allCards
    if (filter !== 'all') {
      if (filter === 'major') {
        filtered = allCards.filter(card => card.type === 'major')
      } else {
        filtered = allCards.filter(card => card.suit === filter)
      }
    }

    if (sortBy === 'name') {
      filtered.sort((a, b) => a.name.localeCompare(b.name))
    } else if (sortBy === 'position') {
      filtered.sort((a, b) => {
        if (a.type === 'major' && b.type === 'major') {
          return (a.rank || 0) - (b.rank || 0)
        }
        if (a.type === 'major') return -1
        if (b.type === 'major') return 1

        const suitOrder = ['songs', 'mountains', 'puppets', 'whistles']
        const suitA = suitOrder.indexOf(a.suit)
        const suitB = suitOrder.indexOf(b.suit)

        if (suitA !== suitB) return suitA - suitB
        return (a.rank || 0) - (b.rank || 0)
      })
    }

    return filtered
  }, [deckData, filter, sortBy])

  const getCardImagePath = (slug) => {
    // Convert slugs like "major-0" to "major-00" to match filenames
    const paddedSlug = slug.replace(/-(\d)$/, '-0$1')
    return `/cards/${paddedSlug}.png`
  }

  return (
    <div className="card-browser">
      <div className="browser-controls">
        <div className="control-group">
          <label>Filter:</label>
          <select value={filter} onChange={(e) => setFilter(e.target.value)}>
            <option value="all">All Cards ({Object.keys(deckData.cards).length})</option>
            <option value="major">Major Arcana ({Object.values(deckData.cards).filter(c => c.type === 'major').length})</option>
            {Object.entries(deckData.suits).map(([slug, suit]) => (
              <option key={slug} value={slug}>
                {suit.name} ({Object.values(deckData.cards).filter(c => c.suit === slug).length})
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Sort:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="position">By Position</option>
            <option value="name">By Name</option>
          </select>
        </div>

        <div className="card-count">
          Showing {cards.length} cards
        </div>
      </div>

      <div className="cards-grid">
        {cards.map(card => (
          <div
            key={card.slug}
            className={`card-thumbnail ${card.type === 'major' ? 'major-arcana' : ''} suit-${card.suit || 'major'}`}
            onClick={() => setSelectedCard(card)}
          >
            <div className="card-image-wrapper">
              <img
                src={getCardImagePath(card.slug)}
                alt={card.name}
                loading="lazy"
              />
            </div>
            <div className="card-info">
              <h3>{card.name}</h3>
              {card.type === 'major' && card.rank !== undefined && (
                <span className="card-number">{romanNumeral(card.rank)}</span>
              )}
              {card.suit && (
                <span className="card-suit">{deckData.suits[card.suit]?.name}</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {selectedCard && (
        <CardModal
          card={selectedCard}
          deckData={deckData}
          imagePath={getCardImagePath(selectedCard.slug)}
          onClose={() => setSelectedCard(null)}
        />
      )}
    </div>
  )
}

function romanNumeral(num) {
  if (num === 0) return '0'
  const lookup = {
    M: 1000, CM: 900, D: 500, CD: 400, C: 100, XC: 90,
    L: 50, XL: 40, X: 10, IX: 9, V: 5, IV: 4, I: 1
  }
  let roman = ''
  let remaining = num
  for (let i in lookup) {
    while (remaining >= lookup[i]) {
      roman += i
      remaining -= lookup[i]
    }
  }
  return roman
}

export default CardBrowser
