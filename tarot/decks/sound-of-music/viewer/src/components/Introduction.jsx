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
        <h3>The Vision</h3>
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
        <p className="framework-intro">
          Two axes create four quadrants - four ways of relating to meaning and action:
        </p>
        <div className="dialectic-grid">
          <div className="axis">
            <h4>Authenticity ⟷ Instrumentality</h4>
            <p>Being genuine vs using for ends. Expression vs manipulation.</p>
          </div>
          <div className="axis">
            <h4>Creation ⟷ Transmission</h4>
            <p>Making new vs passing down. Innovation vs heritage.</p>
          </div>
        </div>
      </section>

      <section className="suits">
        <h3>The Four Suits</h3>
        <p className="suits-intro">Each suit occupies one quadrant of the dialectical space:</p>
        <div className="suits-grid">
          <div className="suit-card suit-songs">
            <div className="suit-header">
              <div className="suit-symbol" dangerouslySetInnerHTML={{ __html: deckData.suits.songs.symbol.svg }} />
              <div>
                <h4>Songs</h4>
                <p className="suit-position">Authentic / Creative</p>
              </div>
            </div>
            <p className="suit-description">
              Spontaneous expression, joy made audible. Alpine meadow watercolors -
              bright, airy, impressionistic overflow.
            </p>
          </div>

          <div className="suit-card suit-mountains">
            <div className="suit-header">
              <div className="suit-symbol" dangerouslySetInnerHTML={{ __html: deckData.suits.mountains.symbol.svg }} />
              <div>
                <h4>Mountains</h4>
                <p className="suit-position">Authentic / Transmissive</p>
              </div>
            </div>
            <p className="suit-description">
              Ancient wisdom passed down through generations. Weathered stone romanticism -
              monumental, permanent, sublime.
            </p>
          </div>

          <div className="suit-card suit-puppets">
            <div className="suit-header">
              <div className="suit-symbol" dangerouslySetInnerHTML={{ __html: deckData.suits.puppets.symbol.svg }} />
              <div>
                <h4>Puppets</h4>
                <p className="suit-position">Instrumental / Creative</p>
              </div>
            </div>
            <p className="suit-description">
              Craft and spectacle, performance for effect. Theatrical staging with Art Deco drama -
              spotlights, strings, and gilt.
            </p>
          </div>

          <div className="suit-card suit-whistles">
            <div className="suit-header">
              <div className="suit-symbol" dangerouslySetInnerHTML={{ __html: deckData.suits.whistles.symbol.svg }} />
              <div>
                <h4>Whistles</h4>
                <p className="suit-position">Instrumental / Transmissive</p>
              </div>
            </div>
            <p className="suit-description">
              Order and discipline, command structure. Naval precision with Bauhaus clarity -
              geometric grids and brass.
            </p>
          </div>
        </div>
      </section>

      <section className="major-arcana-intro">
        <h3>Major Arcana: The Journey (19 Cards)</h3>
        <p>
          The 19 Major Arcana correspond to the 19 songs in <em>The Sound of Music</em>,
          charting the narrative arc from Maria alone on the mountain to the family's escape
          over the Alps. Each song marks a pivotal transformation - from spontaneous
          joy to defiant resistance to ultimate freedom.
        </p>
        <p>
          This is the Technicolor journey: the Preludium's vast panorama, Maria's awakening,
          the children learning to sing, love blossoming, and finally the climb toward liberation.
          The Major Arcana asks: <em>How does authentic joy survive when fascism demands submission?</em>
        </p>
      </section>

      <section className="numbered-ranks">
        <h3>Numbered Ranks: Questions (Ace through Ten)</h3>
        <p>
          The numbered cards (Ace through Ten) pose <strong>questions</strong>, not answers.
          Each rank asks the same question across all four suits, but each suit interprets
          the question through its dialectical lens.
        </p>
        <div className="ranks-examples">
          <div className="rank-example">
            <strong>Ace:</strong> What enters your life? What gift, what seed, what beginning?
          </div>
          <div className="rank-example">
            <strong>Three:</strong> What are you learning? What wisdom is taking root?
          </div>
          <div className="rank-example">
            <strong>Seven:</strong> What choice confronts you? Which path will you take?
          </div>
          <div className="rank-example">
            <strong>Ten:</strong> What is complete? What cycle fulfilled, what journey ended?
          </div>
        </div>
        <p className="ranks-note">
          The same question reverberates differently in Songs (spontaneous joy), Mountains
          (ancient wisdom), Puppets (theatrical craft), and Whistles (ordered discipline).
        </p>
      </section>

      <section className="face-cards">
        <h3>Face Cards: Archetypes (Four Non-Hierarchical Roles)</h3>
        <p>
          Rather than traditional Page/Knight/Queen/King hierarchy, this deck uses four
          <strong>non-hierarchical archetypes</strong> in dialectical tension with each other.
          These aren't ranks to climb - they're different modes of being.
        </p>
        <div className="faces-grid">
          <div className="face-card">
            <h4>Singer</h4>
            <p>Voice as power, expression, authenticity. The one who sings.</p>
          </div>
          <div className="face-card">
            <h4>Goatherd</h4>
            <p>Playful authenticity, the Lonely Goatherd. Folk wisdom and delight.</p>
          </div>
          <div className="face-card">
            <h4>Puppeteer</h4>
            <p>Craft and control, strings visible or hidden. The maker who stages.</p>
          </div>
          <div className="face-card">
            <h4>Officer</h4>
            <p>Authority and discipline, command structure. Order embodied.</p>
          </div>
        </div>
        <p className="faces-note">
          Each archetype appears in all four suits, creating 16 different expressions of
          authority, creativity, and power. The Singer of Songs vs the Singer of Whistles -
          same role, profoundly different meanings.
        </p>
      </section>

      <div className="cta">
        <button onClick={onStartBrowsing} className="browse-button">
          Explore All 75 Cards →
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
