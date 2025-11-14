import { useEffect } from 'react'
import './CardModal.css'

function CardModal({ card, deckData, imagePath, onClose }) {
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleEsc)
    return () => window.removeEventListener('keydown', handleEsc)
  }, [onClose])

  const suitData = card.suit ? deckData.suits[card.suit] : null

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} aria-label="Close">
          ✕
        </button>

        <div className="modal-layout">
          <div className="modal-image">
            <img src={imagePath} alt={card.name} />
          </div>

          <div className="modal-details">
            <div className="card-header">
              <h2>{card.name}</h2>
              {card.type === 'major' && card.rank !== undefined && (
                <span className="rank-badge major">
                  {card.rank === 0 ? '0' : romanNumeral(card.rank)}
                </span>
              )}
              {card.suit && suitData && (
                <div className="suit-badge">
                  <span className="suit-name">{suitData.name}</span>
                  {card.rank !== undefined && (
                    <span className="rank-badge">{getRankName(card.rank, deckData)}</span>
                  )}
                </div>
              )}
            </div>

            {card.description && (
              <div className="card-description">
                <p>{card.description}</p>
              </div>
            )}

            {card.question && (
              <div className="card-question">
                <h3>The Question</h3>
                <p className="question-text">{card.question}</p>
              </div>
            )}

            {card.meanings && (
              <div className="card-meanings">
                <div className="meaning-section upright">
                  <h3>Upright</h3>
                  {Array.isArray(card.meanings.upright) ? (
                    <ul>
                      {card.meanings.upright.map((meaning, i) => (
                        <li key={i}>{meaning}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>{card.meanings.upright}</p>
                  )}
                </div>

                <div className="meaning-section inverted">
                  <h3>Inverted</h3>
                  {Array.isArray(card.meanings.inverted) ? (
                    <ul>
                      {card.meanings.inverted.map((meaning, i) => (
                        <li key={i}>{meaning}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>{card.meanings.inverted}</p>
                  )}
                </div>
              </div>
            )}

            {card.visual_description && (
              <div className="visual-description">
                <h3>Visual Elements</h3>
                <p>{card.visual_description}</p>
              </div>
            )}

            {suitData && (
              <div className="suit-info">
                <h3>About the {suitData.name} Suit</h3>
                <p className="suit-position">{getSuitPosition(card.suit)}</p>
                <p className="suit-description">{suitData.description}</p>
              </div>
            )}

            {card.type === 'major' && (
              <div className="major-arcana-info">
                <h3>Major Arcana</h3>
                <p>
                  This card is part of the Major Arcana, representing the narrative journey
                  through <em>The Sound of Music</em>'s 19 songs - from mountain solitude
                  to escape and freedom.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
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

function getRankName(rank, deckData) {
  // Find the rank in the deck data
  const rankData = Object.values(deckData.ranks).find(r => r.value === rank)
  return rankData?.name || `${rank}`
}

function getSuitPosition(slug) {
  const positions = {
    songs: 'Authentic / Creative',
    mountains: 'Authentic / Transmissive',
    puppets: 'Instrumental / Creative',
    whistles: 'Instrumental / Transmissive'
  }
  return positions[slug] || ''
}

export default CardModal
