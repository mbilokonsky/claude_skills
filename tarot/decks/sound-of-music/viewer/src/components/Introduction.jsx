import './Introduction.css'

function Introduction({ deckData, onStartBrowsing }) {
  return (
    <div className="introduction">
      <section className="hero">
        <h2>The Sound of Music Tarot</h2>
        <p className="tagline">
          A dialectical journey through authenticity and instrumentality,
          creation and transmission
        </p>
      </section>

      <section className="concept">
        <h3>The Deck's Philosophy</h3>
        <p>
          This deck explores the dialectics at the heart of <em>The Sound of Music</em>,
          examining how fascism operates as <strong>instrumental creation masquerading as
          authentic transmission</strong> - an epistemic attack on meaning itself.
        </p>
        <p>
          Through Maria's authentic creativity, Georg's authentic transmission, and the
          looming shadow of fascism corrupting both puppetry and discipline, the deck asks:
          <em>How do we preserve authentic joy and love when instrumental forces demand our
          submission?</em>
        </p>
      </section>

      <section className="dialectics">
        <h3>The Dialectical Framework</h3>
        <div className="dialectic-grid">
          <div className="axis">
            <h4>Vertical Axis</h4>
            <p><strong>Authenticity ⟷ Instrumentality</strong></p>
            <p>Being vs using, genuine expression vs manipulation</p>
          </div>
          <div className="axis">
            <h4>Horizontal Axis</h4>
            <p><strong>Creation ⟷ Transmission</strong></p>
            <p>Making new vs passing down, innovation vs heritage</p>
          </div>
        </div>
      </section>

      <section className="suits">
        <h3>The Four Suits</h3>
        <div className="suits-grid">
          {Object.entries(deckData.suits).map(([slug, suit]) => (
            <div key={slug} className={`suit-card suit-${slug}`}>
              <div className="suit-symbol" dangerouslySetInnerHTML={{ __html: suit.symbol.svg }} />
              <h4>{suit.name}</h4>
              <p className="suit-position">{getSuitPosition(slug)}</p>
              <p className="suit-description">{suit.description}</p>
              <div className="suit-meanings">
                <div className="upright">
                  <strong>Upright:</strong>
                  <ul>
                    {suit.meaning.upright.slice(0, 3).map((meaning, i) => (
                      <li key={i}>{meaning}</li>
                    ))}
                  </ul>
                </div>
                <div className="inverted">
                  <strong>Inverted:</strong>
                  <ul>
                    {suit.meaning.inverted.slice(0, 3).map((meaning, i) => (
                      <li key={i}>{meaning}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="major-arcana-intro">
        <h3>Major Arcana: The Journey</h3>
        <p>
          The 19 Major Arcana cards correspond to the 19 songs in <em>The Sound of Music</em>,
          tracing the narrative arc from Maria alone on the mountain to the family's escape
          over the Alps. Each song marks a pivotal moment in the story, from spontaneous
          joy to defiant resistance to ultimate freedom.
        </p>
        <p>
          From the Preludium's vast mountain panorama through Maria's transformation,
          the children's awakening, Georg and Maria's love, to the final climb toward freedom -
          the Major Arcana charts a Technicolor journey from innocence through crisis to liberation.
        </p>
      </section>

      <section className="visual-style">
        <h3>Visual Language</h3>
        <div className="visual-grid">
          <div className="visual-note">
            <h4>🎵 Songs</h4>
            <p>Alpine meadow watercolors - bright, airy, impressionistic.
            The aesthetic of spontaneous joy and creative overflow.</p>
          </div>
          <div className="visual-note">
            <h4>⛰️ Mountains</h4>
            <p>Weathered stone romanticism - monumental, permanent, sublime.
            Caspar David Friedrich meets ancient wisdom.</p>
          </div>
          <div className="visual-note">
            <h4>🎭 Puppets</h4>
            <p>Theatrical staging with Art Deco drama - spotlights, strings,
            and gilt. Craft that can delight or manipulate.</p>
          </div>
          <div className="visual-note">
            <h4>📯 Whistles</h4>
            <p>Naval precision with Bauhaus clarity - geometric grids and brass.
            Order that can protect or oppress.</p>
          </div>
        </div>
      </section>

      <div className="cta">
        <button onClick={onStartBrowsing} className="browse-button">
          Explore the Deck →
        </button>
      </div>
    </div>
  )
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

export default Introduction
