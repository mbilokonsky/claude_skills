import React, { useState, useRef, useEffect } from 'react';

// P5 Canvas Component (renders p5.js sketch code)
const P5Canvas = ({ code, cardKey }) => {
  const canvasRef = useRef(null);
  const p5InstanceRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !code) return;

    // Load p5.js if not already loaded
    if (typeof window.p5 === 'undefined') {
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js';
      script.onload = () => initP5();
      document.head.appendChild(script);
    } else {
      initP5();
    }

    function initP5() {
      try {
        // Clear any existing content
        if (canvasRef.current) {
          canvasRef.current.innerHTML = '';
        }
        
        // Create function from code string
        const sketchFunc = new Function('return ' + code)();
        
        // Create p5 instance - explicitly pass container
        p5InstanceRef.current = new window.p5(sketchFunc, canvasRef.current);
      } catch (e) {
        console.error('P5 init error:', e);
      }
    }

    return () => {
      if (p5InstanceRef.current) {
        p5InstanceRef.current.remove();
        p5InstanceRef.current = null;
      }
    };
  }, [code]);

  return <div ref={canvasRef} style={{ width: '100%', height: '100%', position: 'relative' }} />;
};

// Reusable suit symbol component with color customization
const SuitSymbol = ({ svgString, color = "#667eea", size = 24 }) => {
  if (!svgString) return null;
  
  // Replace color references in SVG
  const coloredSvg = svgString
    .replace(/#667eea/g, color)
    .replace(/stroke="#[^"]*"/g, `stroke="${color}"`)
    .replace(/fill="#667eea"/g, `fill="${color}"`);
  
  return (
    <div 
      style={{ width: size, height: size, display: 'inline-block' }}
      dangerouslySetInnerHTML={{ __html: coloredSvg }}
    />
  );
};

// Card banner component (overlays on top of P5 canvas)
const CardBanner = ({ cardName, suitSvg, cardType }) => {
  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      left: 0,
      width: '400px', // Fixed width to match canvas
      height: '20px',
      backgroundColor: '#ffd700',
      borderTop: '1px solid #daa520',
      borderBottom: '1px solid #daa520',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 10,
      pointerEvents: 'none',
      boxSizing: 'border-box'
    }}>
      {cardType === 'minor' && suitSvg && (
        <div style={{ position: 'absolute', left: '8px', top: '2px' }}>
          <SuitSymbol svgString={suitSvg} color="#000" size={16} />
        </div>
      )}
      <span style={{ 
        fontWeight: 'bold', 
        fontSize: '12px',
        color: '#000',
        textShadow: '0 0 2px rgba(255,255,255,0.5)'
      }}>
        {cardName}
      </span>
    </div>
  );
};

// Wrapper that combines P5 canvas with banner overlay
const CardVisualWithBanner = ({ code, cardKey, cardName, suitSvg, cardType, style }) => {
  return (
    <div style={{ 
      position: 'relative', 
      width: '400px', 
      height: '600px',
      overflow: 'hidden',
      ...style 
    }}>
      <P5Canvas code={code} cardKey={cardKey} />
      <CardBanner cardName={cardName} suitSvg={suitSvg} cardType={cardType} />
    </div>
  );
};

const deckData = 
"$$REPLACE_ME_WITH_JSON$$";


// Generate all 56 minor arcana cards
const generateMinorCards = () => {
  const cards = [];
  const suits = deckData.minor_arcana.suits;
  const numbered = deckData.minor_arcana.ranks.numbered;
  const face = deckData.minor_arcana.ranks.face;
  
  for (let suitIdx = 0; suitIdx < suits.length; suitIdx++) {
    const suit = suits[suitIdx];
    
    for (let rankIdx = 0; rankIdx < numbered.length; rankIdx++) {
      const rank = numbered[rankIdx];
      const rankNames = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"];
      
      cards.push({
        suit_index: suitIdx,
        rank_index: rankIdx,
        name: `${rankNames[rankIdx]} of ${suit.name}`,
        tags: [...rank.tags, ...suit.tags.slice(0, 2)],
        inverted_tags: [...rank.inverted_tags, ...suit.inverted_tags.slice(0, 2)],
        image_content: `${rank.image_content} within ${suit.name.toLowerCase()}: ${suit.visual_style}`
      });
    }
    
    for (let faceIdx = 0; faceIdx < face.length; faceIdx++) {
      const rank = face[faceIdx];
      
      cards.push({
        suit_index: suitIdx,
        rank_index: 10 + faceIdx,
        name: `${rank.name} of ${suit.name}`,
        tags: [...rank.tags, ...suit.tags.slice(0, 2)],
        inverted_tags: [...rank.inverted_tags, ...suit.inverted_tags.slice(0, 2)],
        image_content: `${rank.image_content} embodying ${suit.name.toLowerCase()}: ${suit.visual_style}`
      });
    }
  }
  
  return cards;
};

deckData.minor_arcana.cards = generateMinorCards();

const TarotDeckViewer = () => {
  const [activeView, setActiveView] = useState('summary');
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  const [artworkFilter, setArtworkFilter] = useState('all'); // 'all', 'with-artwork', 'without-artwork'
  const [selectedCardId, setSelectedCardId] = useState(null);
  
  // Visuals state
  const [generatedVisuals, setGeneratedVisuals] = useState({});
  const [generatingCard, setGeneratingCard] = useState(null);
  const [showRestoreBanner, setShowRestoreBanner] = useState(false);
  const [exportStatus, setExportStatus] = useState('');
  
  // Settings state
  const [showSettings, setShowSettings] = useState(false);
  const [customPrompt, setCustomPrompt] = useState('');
  const [customReaderPrompt, setCustomReaderPrompt] = useState('');
  const [spreadConfig, setSpreadConfig] = useState(null);
  
  // Reader state
  const questionRef = useRef(null);
  const [drawnCards, setDrawnCards] = useState(null);
  const [fixedQuestion, setFixedQuestion] = useState('');
  const [reading, setReading] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [readingRequested, setReadingRequested] = useState(false);
  const [dealingIndex, setDealingIndex] = useState(-1);
  const cardListRef = useRef(null);
  const scrollPositionRef = useRef(0);
  
  // Preserve scroll position when selecting cards
  useEffect(() => {
    const cardList = cardListRef.current;
    if (!cardList) return;
    
    // Save current scroll position
    const handleScroll = () => {
      scrollPositionRef.current = cardList.scrollTop;
    };
    
    cardList.addEventListener('scroll', handleScroll);
    return () => cardList.removeEventListener('scroll', handleScroll);
  }, []);
  
  // Restore scroll after selection changes
  useEffect(() => {
    const cardList = cardListRef.current;
    if (cardList && scrollPositionRef.current !== undefined) {
      // Use requestAnimationFrame to ensure DOM has updated
      requestAnimationFrame(() => {
        cardList.scrollTop = scrollPositionRef.current;
      });
    }
  }, [selectedCardId]);

  // Get storage key
  const getStorageKey = () => {
    const themeName = typeof deckData.theme === 'string' 
      ? deckData.theme 
      : deckData.theme.name;
    return `tarot-visuals-${themeName.replace(/\s+/g, '-').toLowerCase()}`;
  };

  // Load visuals from localStorage on mount
  useEffect(() => {
    const storageKey = getStorageKey();
    console.log('DeckViewer looking for visuals with key:', storageKey);
    const saved = localStorage.getItem(storageKey);
    console.log('Found in localStorage:', saved ? 'YES' : 'NO');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        console.log('Successfully parsed visuals, count:', Object.keys(parsed).length);
        setGeneratedVisuals(parsed);
      } catch (e) {
        console.error('Failed to load visuals:', e);
      }
    } else {
      setShowRestoreBanner(true);
    }
    
    // Load custom prompt if saved
    const savedPrompt = localStorage.getItem('tarot-custom-prompt');
    if (savedPrompt) {
      setCustomPrompt(savedPrompt);
    }
    
    // Load custom reader prompt if saved
    const savedReaderPrompt = localStorage.getItem('tarot-reader-prompt');
    if (savedReaderPrompt) {
      setCustomReaderPrompt(savedReaderPrompt);
    }
    
    // Load spread configuration if saved, otherwise use default
    const savedSpread = localStorage.getItem('tarot-spread-config');
    if (savedSpread) {
      setSpreadConfig(JSON.parse(savedSpread));
    } else {
      // Default three-card spread
      const defaultSpread = {
        name: 'Three-Card Spread',
        positions: [
          { label: 'Past', meaning: 'What has led to this moment' },
          { label: 'Present', meaning: 'The current situation or energy' },
          { label: 'Future', meaning: 'Where this path is leading' }
        ]
      };
      setSpreadConfig(defaultSpread);
    }
  }, []);

  // Save visuals to localStorage whenever they change
  useEffect(() => {
    if (Object.keys(generatedVisuals).length > 0) {
      localStorage.setItem(getStorageKey(), JSON.stringify(generatedVisuals));
      setShowRestoreBanner(false);
    }
  }, [generatedVisuals]);

  // Get card key for storage
  const getCardKey = (card) => {
    if (card.type === 'major') {
      return `major-${card.number}`;
    } else {
      const suit = deckData.minor_arcana.suits[card.suit_index];
      return `${suit.name.toLowerCase().replace(/\s+/g, '-')}-${card.rank_index + 1}`;
    }
  };

  // Generate p5.js visual for a card
  const generateVisual = async (card) => {
    const cardKey = getCardKey(card);
    setGeneratingCard(cardKey);

    // Default prompt template (v5.9 - no banner generation)
    const defaultPrompt = `Create a p5.js sketch for a tarot card with these attributes:

Card: {CARD_NAME}
Type: {CARD_TYPE}
Tags: {CARD_TAGS}
Visual Description: {VISUAL_DESCRIPTION}

Deck Theme: {DECK_THEME}
{VISUAL_STYLE}

Create an engaging, creative p5.js that captures the essence of this card. The sketch should be:
- Animated or dynamic (use motion, transformation, particle systems, etc.)
- Subtly interactive
- Visually striking with good use of color and composition, paying close attention to the visual style specified for the card
- 400x600 pixels (standard tarot card proportions)
- Complete and self-contained
- Focus on the artistic visual content ONLY (the card name banner will be added separately)

Return ONLY the p5.js code wrapped in a function called sketch(p) for instance mode. Do not include markdown code blocks or any other text. Start directly with:

function sketch(p) {
  p.setup = function() {
    p.createCanvas(400, 600);
    // your code
  };
  
  p.draw = function() {
    // your code
  };
}`;

    // Use custom prompt if available, otherwise use default
    const promptTemplate = customPrompt || defaultPrompt;
    
    // Replace template variables (no suit symbol needed - banner handles that)
    const prompt = promptTemplate
      .replace('{CARD_NAME}', card.name)
      .replace('{CARD_TYPE}', card.type === 'major' ? 'Major Arcana' : 'Minor Arcana')
      .replace('{CARD_TAGS}', card.tags.join(', '))
      .replace('{VISUAL_DESCRIPTION}', card.image_content)
      .replace('{DECK_THEME}', typeof deckData.theme === 'string' ? deckData.theme : deckData.theme.name)
      .replace('{VISUAL_STYLE}', card.type === 'major' 
        ? `Visual Style: ${deckData.major_arcana.visual_style}` 
        : card.suit_index !== undefined 
          ? `Suit: ${deckData.minor_arcana.suits[card.suit_index].name}
Visual Style: ${deckData.minor_arcana.suits[card.suit_index].visual_style}`
          : '');

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4000,
          messages: [{ role: "user", content: prompt }]
        })
      });

      const data = await response.json();
      let code = data.content[0].text;
      
      // Clean up code if wrapped in markdown
      code = code.replace(/```javascript\n?/g, "").replace(/```\n?/g, "").trim();
      
      // Store the generated code
      setGeneratedVisuals(prev => ({
        ...prev,
        [cardKey]: code
      }));
      
    } catch (error) {
      console.error('Failed to generate visual:', error);
      alert('Failed to generate visual. Please try again.');
    } finally {
      setGeneratingCard(null);
    }
  };

  // Export visuals to backup artifact via download
  const exportVisuals = () => {
    const visualCount = Object.keys(generatedVisuals).length;
    if (visualCount === 0) {
      alert('No visuals to export. Generate some visuals first!');
      return;
    }

    const themeName = typeof deckData.theme === 'string' 
      ? deckData.theme 
      : deckData.theme.name;

    // Create the DeckVisualsLoader JSX component
    const storageKey = `tarot-visuals-${themeName.replace(/\s+/g, '-').toLowerCase()}`;
    const jsxContent = `import React, { useState, useEffect } from 'react';

const DeckVisualsLoader = () => {
  const [status, setStatus] = useState('loading');
  
  const visualsData = ${JSON.stringify({
    deckTheme: themeName,
    timestamp: new Date().toISOString(),
    visualCount: visualCount,
    visuals: generatedVisuals
  }, null, 2)};

  const storageKey = 'tarot-visuals-${themeName.replace(/\s+/g, '-').toLowerCase()}';

  useEffect(() => {
    try {
      // Store all visuals as a single JSON object under the deck's storage key
      localStorage.setItem(storageKey, JSON.stringify(visualsData.visuals));
      console.log('Loaded visuals to localStorage with key:', storageKey);
      console.log('Visual count:', Object.keys(visualsData.visuals).length);
      setStatus('success');
      
      // Show success message
      setTimeout(() => {
        const message = \`Successfully loaded \${visualsData.visualCount} visual\${visualsData.visualCount !== 1 ? 's' : ''} into localStorage!\`;
        alert(message);
      }, 100);
    } catch (error) {
      console.error('Failed to load visuals:', error);
      setStatus('error');
    }
  }, []);

  return (
    <div style={{ 
      padding: '40px', 
      maxWidth: '800px', 
      margin: '0 auto',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <h1 style={{ marginBottom: '20px' }}>Deck Visuals Loader</h1>
      
      <div style={{ 
        padding: '20px', 
        borderRadius: '8px',
        backgroundColor: status === 'success' ? '#d4edda' : status === 'error' ? '#f8d7da' : '#fff3cd',
        border: \`1px solid \${status === 'success' ? '#c3e6cb' : status === 'error' ? '#f5c6cb' : '#ffeaa7'}\`,
        color: status === 'success' ? '#155724' : status === 'error' ? '#721c24' : '#856404'
      }}>
        {status === 'loading' && (
          <p>Loading visuals into localStorage...</p>
        )}
        {status === 'success' && (
          <div>
            <h2 style={{ marginTop: 0 }}>✓ Visuals Loaded Successfully</h2>
            <p><strong>Deck:</strong> {visualsData.deckTheme}</p>
            <p><strong>Count:</strong> {visualsData.visualCount} visual{visualsData.visualCount !== 1 ? 's' : ''}</p>
            <p><strong>Timestamp:</strong> {new Date(visualsData.timestamp).toLocaleString()}</p>
            <p><strong>Storage Key:</strong> <code style={{ background: '#f8f9fa', padding: '2px 6px', borderRadius: '3px' }}>{storageKey}</code></p>
            <p style={{ marginTop: '20px', fontSize: '0.9em' }}>
              Your generated visuals have been restored to localStorage. Return to your deck viewer to see them!
            </p>
          </div>
        )}
        {status === 'error' && (
          <div>
            <h2 style={{ marginTop: 0 }}>✗ Error Loading Visuals</h2>
            <p>Failed to load visuals into localStorage. Possible causes:</p>
            <ul>
              <li>localStorage is disabled</li>
              <li>Storage quota exceeded</li>
              <li>Browser security settings</li>
            </ul>
            <p style={{ marginTop: '20px', color: '#6c757d' }}>
              Check the browser console (F12) for more details.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default DeckVisualsLoader;
`;

    // Create downloadable JSX file
    const dataBlob = new Blob([jsxContent], { type: 'text/javascript' });
    const url = URL.createObjectURL(dataBlob);
    
    // Create temporary download link
    const link = document.createElement('a');
    link.href = url;
    const sanitizedTheme = themeName.replace(/[^a-zA-Z0-9]/g, '');
    link.download = `DeckVisualsLoader_${sanitizedTheme}_${Date.now()}.jsx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setExportStatus('downloaded');
  };

  // P5 Canvas Component
  // Get all cards
  const getAllCards = () => {
    const cards = [];
    
    deckData.major_arcana.cards.forEach(card => {
      cards.push({
        id: `major-${card.number}`,
        type: 'major',
        ...card
      });
    });
    
    deckData.minor_arcana.cards.forEach((card, idx) => {
      const suit = deckData.minor_arcana.suits[card.suit_index];
      cards.push({
        id: `minor-${idx}`,
        type: 'minor',
        suit: suit.name,
        ...card
      });
    });
    
    return cards;
  };

  const getFilteredCards = () => {
    const cards = getAllCards();
    return cards.filter(card => {
      const matchesFilter = filter === 'all' || card.type === filter;
      const matchesSearch = searchTerm === '' || 
        card.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        card.tags?.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
      
      // Artwork filter
      const cardKey = getCardKey(card);
      const hasVisual = !!generatedVisuals[cardKey];
      const matchesArtwork = artworkFilter === 'all' ||
        (artworkFilter === 'with-artwork' && hasVisual) ||
        (artworkFilter === 'without-artwork' && !hasVisual);
      
      return matchesFilter && matchesSearch && matchesArtwork;
    });
  };

  const CardListItem = ({ card }) => {
    const cardKey = getCardKey(card);
    const hasVisual = !!generatedVisuals[cardKey];
    
    // Get suit info for minor arcana
    const suitInfo = card.type === 'minor' && card.suit_index !== undefined
      ? deckData.minor_arcana.suits[card.suit_index]
      : null;
    
    // Get rank display (number or face card indicator)
    const getRankDisplay = () => {
      if (card.type === 'major') {
        return card.number !== undefined ? card.number : '?';
      }
      if (card.rank_index !== undefined) {
        if (card.rank_index < 10) {
          return card.rank_index + 1; // 1-10 for numbered cards
        } else {
          // Face cards: 11=Chosen, 12=Pilgrim, 13=Bearer, 14=Keeper
          return ['C', 'P', 'B', 'K'][card.rank_index - 10];
        }
      }
      return '?';
    };
    
    const handleClick = (e) => {
      e.preventDefault();
      setSelectedCardId(card.id);
    };
    
    return (
      <div 
        className={`card-list-item ${selectedCardId === card.id ? 'active' : ''}`}
        data-type={card.type}
        onClick={handleClick}
      >
        <div className={`list-item-badge badge-${card.type}`}>
          <div className="badge-rank">{getRankDisplay()}</div>
          {suitInfo && (
            <div className="badge-suit-icon">
              <SuitSymbol svgString={suitInfo.symbol_svg} color="white" size={14} />
            </div>
          )}
        </div>
        <div className="list-item-name">{card.name}</div>
        {hasVisual && (
          <div className="list-item-artwork-badge">
            🎨
          </div>
        )}
      </div>
    );
  };

  const CardDetail = ({ card }) => {
    if (!card) return (
      <div className="detail-empty">Select a card to view details</div>
    );

    const cardKey = getCardKey(card);
    const visualCode = generatedVisuals[cardKey];
    const isGenerating = generatingCard === cardKey;
    
    // State for collapsible sections
    const [suitExpanded, setSuitExpanded] = useState(false);
    const [rankExpanded, setRankExpanded] = useState(false);
    const [arcanaExpanded, setArcanaExpanded] = useState(false);
    
    // Get suit info for minor arcana
    const suitInfo = card.type === 'minor' && card.suit_index !== undefined
      ? deckData.minor_arcana.suits[card.suit_index]
      : null;
    
    // Get rank info for minor arcana (correctly handle numbered vs face cards)
    const rankInfo = card.type === 'minor' && card.rank_index !== undefined
      ? (card.rank_index < 10 
          ? deckData.minor_arcana.ranks.numbered[card.rank_index]
          : deckData.minor_arcana.ranks.face[card.rank_index - 10])
      : null;

    return (
      <div className="detail-content active">
        {/* Visual Section - Primary Content (no labels, visual speaks for itself) */}
        {visualCode ? (
          <div className="visual-container-primary">
            <CardVisualWithBanner 
              code={visualCode} 
              cardKey={cardKey}
              cardName={card.name}
              suitSvg={suitInfo?.symbol_svg}
              cardType={card.type}
            />
            <button 
              className="regenerate-button"
              onClick={() => generateVisual(card)}
              disabled={isGenerating}
            >
              {isGenerating ? 'Regenerating...' : 'Regenerate Visual'}
            </button>
          </div>
        ) : (
          <div className="visual-container-primary">
            <div className="no-visual-placeholder">
              <CardBanner 
                cardName={card.name}
                suitSvg={suitInfo?.symbol_svg}
                cardType={card.type}
              />
              <div className="no-visual-content">
                <p>No visual generated yet</p>
                <button 
                  className="generate-visual-button"
                  onClick={() => generateVisual(card)}
                  disabled={isGenerating}
                >
                  {isGenerating ? 'Generating...' : 'Generate Visual'}
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Visual Description */}
        <div className="detail-section">
          <div className="detail-section-title">Visual Description</div>
          <div className="detail-description-compact">{card.image_content}</div>
        </div>
        
        {/* Upright Tags - Compact */}
        <div className="detail-section">
          <div className="detail-section-title">Upright Meanings</div>
          <div className="detail-tags-compact">
            {card.tags?.map((tag, idx) => (
              <span key={idx} className="detail-tag-compact">{tag}</span>
            ))}
          </div>
        </div>
        
        {/* Inverted Tags - Compact */}
        <div className="detail-section">
          <div className="detail-section-title">Inverted Meanings</div>
          <div className="detail-tags-compact">
            {card.inverted_tags?.map((tag, idx) => (
              <span key={idx} className="detail-tag-compact inverted">{tag}</span>
            ))}
          </div>
        </div>
        
        {/* Collapsible Suit/Rank/Arcana Information */}
        {card.type === 'major' ? (
          <div className="detail-info-box">
            <div 
              className="detail-info-header"
              onClick={() => setArcanaExpanded(!arcanaExpanded)}
            >
              <div className="detail-info-title">
                Major Arcana #{card.number}
                {card.role && <span className="detail-info-subtitle"> — {card.role}</span>}
              </div>
              <div className="detail-info-toggle">{arcanaExpanded ? '−' : '+'}</div>
            </div>
            {arcanaExpanded && (
              <div className="detail-info-content">
                <div className="detail-info-field">
                  <strong>Visual Style:</strong>
                  <p>{deckData.major_arcana.visual_style}</p>
                </div>
              </div>
            )}
          </div>
        ) : (
          <>
            {suitInfo && (
              <div className="detail-info-box">
                <div 
                  className="detail-info-header"
                  onClick={() => setSuitExpanded(!suitExpanded)}
                >
                  <div className="detail-info-title">
                    Suit: {suitInfo.name}
                    <span className="detail-info-subtitle"> — {suitInfo.symbol}</span>
                  </div>
                  <div className="detail-info-toggle">{suitExpanded ? '−' : '+'}</div>
                </div>
                {suitExpanded && (
                  <div className="detail-info-content">
                    <div className="detail-info-field">
                      <strong>Visual Style:</strong>
                      <p>{suitInfo.visual_style}</p>
                    </div>
                    <div className="detail-info-field">
                      <strong>Upright Themes:</strong>
                      <div className="detail-tags-compact">
                        {suitInfo.tags?.map((tag, idx) => (
                          <span key={idx} className="detail-tag-compact">{tag}</span>
                        ))}
                      </div>
                    </div>
                    <div className="detail-info-field">
                      <strong>Inverted Themes:</strong>
                      <div className="detail-tags-compact">
                        {suitInfo.inverted_tags?.map((tag, idx) => (
                          <span key={idx} className="detail-tag-compact inverted">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {rankInfo && (
              <div className="detail-info-box">
                <div 
                  className="detail-info-header"
                  onClick={() => setRankExpanded(!rankExpanded)}
                >
                  <div className="detail-info-title">
                    Rank: {rankInfo.name || rankInfo.number}
                    {rankInfo.role && <span className="detail-info-subtitle"> — {rankInfo.role}</span>}
                  </div>
                  <div className="detail-info-toggle">{rankExpanded ? '−' : '+'}</div>
                </div>
                {rankExpanded && (
                  <div className="detail-info-content">
                    <div className="detail-info-field">
                      <strong>Visual Content:</strong>
                      <p>{rankInfo.image_content}</p>
                    </div>
                    <div className="detail-info-field">
                      <strong>Upright Associations:</strong>
                      <div className="detail-tags-compact">
                        {rankInfo.tags?.map((tag, idx) => (
                          <span key={idx} className="detail-tag-compact">{tag}</span>
                        ))}
                      </div>
                    </div>
                    <div className="detail-info-field">
                      <strong>Inverted Associations:</strong>
                      <div className="detail-tags-compact">
                        {rankInfo.inverted_tags?.map((tag, idx) => (
                          <span key={idx} className="detail-tag-compact inverted">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    );
  };

  // Reading Card Component (with visual support)
  const ReadingCard = ({ card, position, isVisible, dealDelay }) => {
    if (!card) return null;
    
    const cardKey = getCardKey(card);
    const visualCode = generatedVisuals[cardKey];
    const [hasRotated, setHasRotated] = useState(false);
    
    // Get suit SVG for minor arcana
    const suitSvg = card.type === 'minor' && card.suit_index !== undefined
      ? deckData.minor_arcana.suits[card.suit_index].symbol_svg
      : null;
    
    // Trigger rotation animation for inverted cards after they appear
    useEffect(() => {
      if (isVisible && position.inverted && !hasRotated) {
        setTimeout(() => {
          setHasRotated(true);
        }, 250); // Short delay after card appears
      }
    }, [isVisible, position.inverted, hasRotated]);

    const containerStyle = {
      opacity: isVisible ? 1 : 0,
      transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
      transition: `opacity 0.3s ease-out ${dealDelay}s, 
                   transform 0.3s ease-out ${dealDelay}s`
    };
    
    const visualStyle = {
      transform: (position.inverted && hasRotated) ? 'scale(0.35) rotate(180deg)' : 'scale(0.35)',
      transition: hasRotated ? 'transform 0.75s ease-out' : 'none'
    };

    return (
      <div className="reading-card-position" style={containerStyle}>
        <div className="position-label">{position.label}</div>
        <div className="reading-card">
          {visualCode && isVisible && (
            <div className="card-visual-wrapper">
              <div className="card-visual-canvas" style={visualStyle}>
                <CardVisualWithBanner 
                  code={visualCode} 
                  cardKey={cardKey}
                  cardName={card.name}
                  suitSvg={suitSvg}
                  cardType={card.type}
                />
              </div>
            </div>
          )}
          <div className="reading-card-content">
            <div className="reading-card-name">
              {card.name}
              {position.inverted && ' (Inverted)'}
            </div>
            <div className="reading-card-tags">
              {(position.inverted ? card.inverted_tags : card.tags)?.slice(0, 3).map((tag, idx) => (
                <span key={idx} className="detail-tag">{tag}</span>
              ))}
            </div>
          </div>
        </div>
        <div className="position-meaning">{position.meaning}</div>
      </div>
    );
  };

  const SummaryView = () => {
    const theme = typeof deckData.theme === 'string' 
      ? { name: deckData.theme, description: deckData.theme }
      : deckData.theme;

    return (
      <div className="view active">
        <div className="summary-grid">
          <div className="summary-card">
            <h3>Deck Structure</h3>
            <div className="stat">
              <span className="stat-label">Total Cards</span>
              <span className="stat-value">78</span>
            </div>
            <div className="stat">
              <span className="stat-label">Major Arcana</span>
              <span className="stat-value">22</span>
            </div>
            <div className="stat">
              <span className="stat-label">Minor Arcana</span>
              <span className="stat-value">56</span>
            </div>
            <div className="stat">
              <span className="stat-label">Generated Visuals</span>
              <span className="stat-value">{Object.keys(generatedVisuals).length}</span>
            </div>
            
            <div style={{ marginTop: '25px', paddingTop: '25px', borderTop: '2px solid #e9ecef' }}>
              <h4 style={{ fontSize: '1.1em', marginBottom: '15px', color: '#2c3e50' }}>Visual Backup</h4>
              <p style={{ marginBottom: '15px', fontSize: '0.9em', color: '#6c757d' }}>
                Download generated visuals as a JSX component for backup and restore.
              </p>
              <button 
                className="export-button"
                onClick={exportVisuals}
                disabled={Object.keys(generatedVisuals).length === 0}
              >
                Download Backup ({Object.keys(generatedVisuals).length} visual{Object.keys(generatedVisuals).length !== 1 ? 's' : ''})
              </button>
              {exportStatus === 'downloaded' && (
                <div className="export-ready-section" style={{ marginTop: '15px', padding: '15px', background: '#d4edda', borderRadius: '8px', border: '1px solid #c3e6cb' }}>
                  <h4 style={{ marginTop: 0, fontSize: '0.95em', color: '#155724' }}>✓ Backup Downloaded!</h4>
                  <p style={{ marginBottom: '10px', fontSize: '0.85em', color: '#155724' }}>
                    To restore: upload the .jsx file, ask Claude to convert to artifact, then open it.
                  </p>
                  <button 
                    onClick={() => setExportStatus('')}
                    style={{
                      marginTop: '10px',
                      padding: '6px 12px',
                      background: '#28a745',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '0.85em'
                    }}
                  >
                    Done
                  </button>
                </div>
              )}
              {exportStatus && exportStatus !== 'downloaded' && (
                <div className="export-status">{exportStatus}</div>
              )}
            </div>
          </div>

          <div className="summary-card theme-card">
            <h3>Theme</h3>
            <p style={{ fontSize: '1.05em', lineHeight: '1.7', marginBottom: '20px' }}>
              {theme.description}
            </p>
            {theme.salient_concepts && theme.salient_concepts.length > 0 && (
              <div>
                <h4 style={{ fontSize: '0.95em', color: '#667eea', marginBottom: '10px' }}>Key Concepts</h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {theme.salient_concepts.map((concept, idx) => (
                    <span key={idx} className="detail-tag" style={{ fontSize: '0.85em' }}>
                      {concept}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="summary-card">
            <h3>Dialectics</h3>
            <div style={{ marginBottom: '20px' }}>
              <div className="dialectic-display">
                <strong>{deckData.dialectics[0].thesis || deckData.dialectics[0].pole1}</strong>
                {' ⟷ '}
                <strong>{deckData.dialectics[0].antithesis || deckData.dialectics[0].pole2}</strong>
              </div>
              {deckData.dialectics[0].tensions && (
                <div style={{ marginTop: '10px', fontSize: '0.9em', color: '#6c757d', lineHeight: '1.6' }}>
                  {deckData.dialectics[0].tensions.map((tension, idx) => (
                    <div key={idx}>• {tension}</div>
                  ))}
                </div>
              )}
            </div>
            <div>
              <div className="dialectic-display">
                <strong>{deckData.dialectics[1].thesis || deckData.dialectics[1].pole1}</strong>
                {' ⟷ '}
                <strong>{deckData.dialectics[1].antithesis || deckData.dialectics[1].pole2}</strong>
              </div>
              {deckData.dialectics[1].tensions && (
                <div style={{ marginTop: '10px', fontSize: '0.9em', color: '#6c757d', lineHeight: '1.6' }}>
                  {deckData.dialectics[1].tensions.map((tension, idx) => (
                    <div key={idx}>• {tension}</div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const MajorArcanaView = () => (
    <div className="view active">
      <div className="story-section">
        <h2>The Story</h2>
        <p>{deckData.major_arcana.story}</p>
      </div>
      
      <div className="visual-style-section">
        <h3>Visual Style</h3>
        <p>{deckData.major_arcana.visual_style}</p>
      </div>
      
      <div className="cards-grid">
        {deckData.major_arcana.cards.map(card => {
          const fullCard = { ...card, type: 'major', id: `major-${card.number}` };
          const cardKey = getCardKey(fullCard);
          const hasVisual = !!generatedVisuals[cardKey];
          
          return (
            <div key={card.number} className="major-card">
              <div className="major-card-header">
                <span className="major-number">{card.number}</span>
                <h4>{card.name}</h4>
                {hasVisual && <span style={{ marginLeft: 'auto' }}>🎨</span>}
              </div>
              <p className="major-role">{card.role}</p>
              <p className="major-image">{card.image_content}</p>
              <div className="tag-section">
                <div className="tag-label">Upright</div>
                <div className="tag-container">
                  {card.tags.map((tag, idx) => (
                    <span key={idx} className="detail-tag">{tag}</span>
                  ))}
                </div>
              </div>
              <div className="tag-section">
                <div className="tag-label inverted">Inverted</div>
                <div className="tag-container">
                  {card.inverted_tags.map((tag, idx) => (
                    <span key={idx} className="detail-tag inverted">{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );

  const SuitsRanksView = () => (
    <div className="view active">
      <div className="minor-arcana-container">
        <div className="minor-arcana-sidebar">
          <h2>Suits</h2>
          {deckData.minor_arcana.suits.map((suit, idx) => (
            <div key={idx} className="suit-detail-card">
              <div className="suit-card-header">
                {suit.symbol_svg && (
                  <div 
                    className="suit-symbol-medium"
                    dangerouslySetInnerHTML={{ __html: suit.symbol_svg }}
                  />
                )}
                <div>
                  <h3>{suit.name}</h3>
                  <p className="suit-symbol-desc">{suit.symbol}</p>
                </div>
              </div>
              <p className="suit-visual-style">{suit.visual_style}</p>
              <div className="tag-section">
                <div className="tag-label">Upright</div>
                <div className="tag-container">
                  {suit.tags.map((tag, tagIdx) => (
                    <span key={tagIdx} className="detail-tag">{tag}</span>
                  ))}
                </div>
              </div>
              <div className="tag-section">
                <div className="tag-label inverted">Inverted</div>
                <div className="tag-container">
                  {suit.inverted_tags.map((tag, tagIdx) => (
                    <span key={tagIdx} className="detail-tag inverted">{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="minor-arcana-content">
          <h2>Numbered Ranks (1-10)</h2>
          <div className="ranks-list">
            {deckData.minor_arcana.ranks.numbered.map(rank => (
              <div key={rank.number} className="rank-detail-card">
                <div className="rank-card-header">
                  <span className="rank-number">{rank.number}</span>
                  <div>
                    <h4>Rank {rank.number}</h4>
                    <p className="rank-role">{rank.role}</p>
                  </div>
                </div>
                <p className="rank-image-content">{rank.image_content}</p>
                <div className="tag-section">
                  <div className="tag-label">Upright</div>
                  <div className="tag-container">
                    {rank.tags.map((tag, tagIdx) => (
                      <span key={tagIdx} className="detail-tag">{tag}</span>
                    ))}
                  </div>
                </div>
                <div className="tag-section">
                  <div className="tag-label inverted">Inverted</div>
                  <div className="tag-container">
                    {rank.inverted_tags.map((tag, tagIdx) => (
                      <span key={tagIdx} className="detail-tag inverted">{tag}</span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <h2 style={{ marginTop: '40px' }}>Face Ranks (11-14)</h2>
          <div className="ranks-list">
            {deckData.minor_arcana.ranks.face.map(rank => (
              <div key={rank.number} className="rank-detail-card">
                <div className="rank-card-header">
                  <span className="rank-number">{rank.number}</span>
                  <div>
                    <h4>{rank.name}</h4>
                    <p className="rank-role">{rank.role}</p>
                  </div>
                </div>
                <p className="rank-image-content">{rank.image_content}</p>
                <div className="tag-section">
                  <div className="tag-label">Upright</div>
                  <div className="tag-container">
                    {rank.tags.map((tag, tagIdx) => (
                      <span key={tagIdx} className="detail-tag">{tag}</span>
                    ))}
                  </div>
                </div>
                <div className="tag-section">
                  <div className="tag-label inverted">Inverted</div>
                  <div className="tag-container">
                    {rank.inverted_tags.map((tag, tagIdx) => (
                      <span key={tagIdx} className="detail-tag inverted">{tag}</span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const BrowserView = () => {
    const filteredCards = getFilteredCards();
    const selectedCard = selectedCardId 
      ? getAllCards().find(c => c.id === selectedCardId)
      : null;

    return (
      <div className="view active">
        <div className="browser-container">
          <div className="browser-sidebar">
            <div className="browser-controls">
              <input
                type="text"
                className="search-input"
                placeholder="Search cards..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <div className="filter-buttons">
                <button 
                  className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                  onClick={() => setFilter('all')}
                >
                  All ({getAllCards().length})
                </button>
                <button 
                  className={`filter-btn ${filter === 'major' ? 'active' : ''}`}
                  onClick={() => setFilter('major')}
                >
                  Major (22)
                </button>
                <button 
                  className={`filter-btn ${filter === 'minor' ? 'active' : ''}`}
                  onClick={() => setFilter('minor')}
                >
                  Minor (56)
                </button>
              </div>
              <div className="filter-buttons" style={{ marginTop: '10px' }}>
                <button 
                  className={`filter-btn ${artworkFilter === 'all' ? 'active' : ''}`}
                  onClick={() => setArtworkFilter('all')}
                >
                  All Cards
                </button>
                <button 
                  className={`filter-btn ${artworkFilter === 'with-artwork' ? 'active' : ''}`}
                  onClick={() => setArtworkFilter('with-artwork')}
                >
                  🎨 With Artwork
                </button>
                <button 
                  className={`filter-btn ${artworkFilter === 'without-artwork' ? 'active' : ''}`}
                  onClick={() => setArtworkFilter('without-artwork')}
                >
                  ⬜ Without Artwork
                </button>
              </div>
            </div>
            <div className="card-list" ref={cardListRef}>
              {filteredCards.map(card => (
                <CardListItem key={card.id} card={card} />
              ))}
            </div>
          </div>
          <div className="browser-detail">
            <CardDetail card={selectedCard} />
          </div>
        </div>
      </div>
    );
  };

  const ReadingsView = () => {
    // Use spread config or fallback to default
    const currentSpread = spreadConfig || {
      name: 'Three-Card Spread',
      positions: [
        { label: 'Past', meaning: 'What has led to this moment' },
        { label: 'Present', meaning: 'The current situation or energy' },
        { label: 'Future', meaning: 'Where this path is leading' }
      ]
    };

    const drawCards = () => {
      // Capture question before drawing
      const questionText = questionRef.current?.value || '';
      setFixedQuestion(questionText);
      
      const allCards = getAllCards();
      const shuffled = [...allCards].sort(() => Math.random() - 0.5);
      const numCards = currentSpread.positions.length;
      const drawn = shuffled.slice(0, numCards).map(card => ({
        ...card,
        inverted: Math.random() > 0.5
      }));
      
      setDrawnCards(drawn);
      setReading('');
      setReadingRequested(false);
      setDealingIndex(-1);
      
      // Animate card dealing
      drawn.forEach((_, idx) => {
        setTimeout(() => {
          setDealingIndex(idx);
        }, idx * 500);
      });
      
      // Complete dealing animation
      setTimeout(() => {
        setDealingIndex(drawn.length);
      }, drawn.length * 500);
    };

    const generateReading = async () => {
      if (!drawnCards) return;
      
      setIsGenerating(true);
      setReadingRequested(true);

      const questionText = fixedQuestion || 'General guidance';
      const cardsDescription = drawnCards.map((card, idx) => {
        const position = currentSpread.positions[idx].label;
        const orientation = card.inverted ? 'Inverted' : 'Upright';
        const tags = card.inverted ? card.inverted_tags : card.tags;
        return `${position}: ${card.name} (${orientation}) - ${tags.join(', ')}`;
      }).join('\n');

      // Default reader prompt
      const defaultReaderPrompt = `You are reading tarot cards for someone. Here is their question and the ${currentSpread.name.toLowerCase()}:

Question: "{QUESTION}"

Cards drawn:
{CARDS_DESCRIPTION}

Deck theme: {DECK_THEME}

Provide a thoughtful, meaningful interpretation of this spread in the context of their question. Consider:
- How each card's position relates to the question
- The significance of upright vs inverted orientations
- The narrative arc across all cards
- Practical guidance or insights

Write in a warm, insightful tone. Structure your response with clear paragraphs but no bullet points or headers.`;

      // Use custom prompt if available, otherwise use default
      const readerPromptTemplate = customReaderPrompt || defaultReaderPrompt;
      
      // Replace template variables
      const prompt = readerPromptTemplate
        .replace('{QUESTION}', questionText)
        .replace('{CARDS_DESCRIPTION}', cardsDescription)
        .replace('{DECK_THEME}', typeof deckData.theme === 'string' ? deckData.theme : deckData.theme.name);

      try {
        const response = await fetch("https://api.anthropic.com/v1/messages", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: "claude-sonnet-4-20250514",
            max_tokens: 2000,
            messages: [{ role: "user", content: prompt }]
          })
        });

        const data = await response.json();
        setReading(data.content[0].text);
      } catch (error) {
        console.error('Reading generation failed:', error);
        setReading('Failed to generate reading. Please try again.');
      } finally {
        setIsGenerating(false);
      }
    };

    const resetReading = () => {
      setDrawnCards(null);
      setReading('');
      setReadingRequested(false);
      setFixedQuestion('');
      setDealingIndex(-1);
      if (questionRef.current) questionRef.current.value = '';
    };

    return (
      <div className="view active">
        <div className="readings-container">
          <div className="readings-intro">
            <h2>{currentSpread.name}</h2>
            <p>Ask a question and draw cards for insight</p>
          </div>

          {!drawnCards ? (
            <div className="question-section">
              <label>Your Question (optional)</label>
              <textarea
                ref={questionRef}
                className="question-input"
                placeholder="What guidance do you seek?"
                rows="3"
              />
            </div>
          ) : (
            <div className="question-display">
              <label>Your Question</label>
              <div className="fixed-question">
                {fixedQuestion || 'General guidance'}
              </div>
            </div>
          )}

          <div className="reading-buttons">
            <button className="draw-button" onClick={drawCards}>
              {drawnCards ? 'Draw New Cards' : 'Draw Cards'}
            </button>
            {drawnCards && dealingIndex >= drawnCards.length && (
              <>
                <button 
                  className="generate-button"
                  onClick={generateReading}
                  disabled={isGenerating || readingRequested}
                >
                  {isGenerating ? 'Generating Reading...' : readingRequested ? 'Reading Generated' : 'Generate Reading'}
                </button>
                <button className="reset-button" onClick={resetReading}>
                  Reset
                </button>
              </>
            )}
          </div>

          {drawnCards && (
            <div className="spread-display">
              <div className={`spread-positions spread-${currentSpread.positions.length}`}>
                {drawnCards.map((card, idx) => (
                  <ReadingCard 
                    key={idx}
                    card={card}
                    position={{
                      ...currentSpread.positions[idx],
                      inverted: card.inverted
                    }}
                    isVisible={dealingIndex >= idx}
                    dealDelay={idx * 0.5}
                  />
                ))}
              </div>

              {reading && (
                <div className="reading-section">
                  <h3>Interpretation</h3>
                  <div className="reading-content">
                    {reading.split('\n\n').map((para, idx) => (
                      <p key={idx}>{para}</p>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  };

  const SettingsPanel = () => {
    const defaultPrompt = `Create a p5.js sketch for a tarot card with these attributes:

Card: {CARD_NAME}
Type: {CARD_TYPE}
Tags: {CARD_TAGS}
Visual Description: {VISUAL_DESCRIPTION}

Deck Theme: {DECK_THEME}
{VISUAL_STYLE}

Create an engaging, creative p5.js that captures the essence of this card. The sketch should be:
- Animated or dynamic (use motion, transformation, particle systems, etc.)
- Subtly interactive
- Visually striking with good use of color and composition, paying close attention to the visual style specified for the card
- 400x600 pixels (standard tarot card proportions)
- Complete and self-contained
- Focus on the artistic visual content ONLY (the card name banner will be added separately)

Return ONLY the p5.js code wrapped in a function called sketch(p) for instance mode. Do not include markdown code blocks or any other text. Start directly with:

function sketch(p) {
  p.setup = function() {
    p.createCanvas(400, 600);
    // your code
  };
  
  p.draw = function() {
    // your code
  };
}`;

    const defaultReaderPrompt = `You are reading tarot cards for someone. Here is their question and the three-card spread:

Question: "{QUESTION}"

Cards drawn:
{CARDS_DESCRIPTION}

Deck theme: {DECK_THEME}

Provide a thoughtful, meaningful interpretation of this three-card spread in the context of their question. Consider:
- How each card's position (past, present, future) relates to the question
- The significance of upright vs inverted orientations
- The narrative arc across all three cards
- Practical guidance or insights

Write in a warm, insightful tone. Structure your response with clear paragraphs but no bullet points or headers.`;

    const [tempPrompt, setTempPrompt] = useState(customPrompt || defaultPrompt);
    const [tempReaderPrompt, setTempReaderPrompt] = useState(customReaderPrompt || defaultReaderPrompt);
    
    const handleSave = () => {
      setCustomPrompt(tempPrompt);
      localStorage.setItem('tarot-custom-prompt', tempPrompt);
      alert('Visual generation prompt saved!');
    };
    
    const handleReset = () => {
      setTempPrompt(defaultPrompt);
      setCustomPrompt(defaultPrompt);
      localStorage.setItem('tarot-custom-prompt', defaultPrompt);
      alert('Visual generation prompt reset to default');
    };
    
    const handleReaderSave = () => {
      setCustomReaderPrompt(tempReaderPrompt);
      localStorage.setItem('tarot-reader-prompt', tempReaderPrompt);
      alert('Reader prompt saved!');
    };
    
    const handleReaderReset = () => {
      setTempReaderPrompt(defaultReaderPrompt);
      setCustomReaderPrompt(defaultReaderPrompt);
      localStorage.setItem('tarot-reader-prompt', defaultReaderPrompt);
      alert('Reader prompt reset to default');
    };
    
    if (!showSettings) return null;
    
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '20px'
      }}>
        <div style={{
          background: 'white',
          borderRadius: '15px',
          padding: '30px',
          maxWidth: '800px',
          width: '100%',
          maxHeight: '90vh',
          overflow: 'auto',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2 style={{ color: '#2c3e50', margin: 0 }}>Settings</h2>
            <button 
              onClick={() => setShowSettings(false)}
              style={{
                background: 'transparent',
                border: 'none',
                fontSize: '24px',
                cursor: 'pointer',
                color: '#6c757d'
              }}
            >
              ×
            </button>
          </div>
          
          {/* Visual Generation Prompt Section */}
          <div style={{ marginBottom: '30px', paddingBottom: '30px', borderBottom: '2px solid #e9ecef' }}>
            <h3 style={{ color: '#495057', marginBottom: '10px' }}>Visual Generation Prompt</h3>
            <p style={{ color: '#6c757d', fontSize: '14px', marginBottom: '15px' }}>
              Customize the prompt used to generate p5.js visuals. Use these template variables:
            </p>
            <div style={{ background: '#f8f9fa', padding: '15px', borderRadius: '8px', marginBottom: '15px', fontSize: '13px', fontFamily: 'monospace' }}>
              <div><strong>{'{CARD_NAME}'}</strong> - Name of the card</div>
              <div><strong>{'{CARD_TYPE}'}</strong> - Major or Minor Arcana</div>
              <div><strong>{'{CARD_TAGS}'}</strong> - Comma-separated tags</div>
              <div><strong>{'{CARD_SUIT_SYMBOL}'}</strong> - SVG code for suit symbol (Minor Arcana only)</div>
              <div><strong>{'{VISUAL_DESCRIPTION}'}</strong> - Card's visual description</div>
              <div><strong>{'{DECK_THEME}'}</strong> - Deck theme name</div>
              <div><strong>{'{VISUAL_STYLE}'}</strong> - Visual style (for major arcana)</div>
            </div>
            
            <textarea
              value={tempPrompt}
              onChange={(e) => setTempPrompt(e.target.value)}
              style={{
                width: '100%',
                height: '300px',
                padding: '15px',
                borderRadius: '8px',
                border: '2px solid #e9ecef',
                fontSize: '13px',
                fontFamily: 'monospace',
                resize: 'vertical'
              }}
            />
            
            <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
              <button 
                onClick={handleSave}
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '14px'
                }}
              >
                Save Visual Prompt
              </button>
              <button 
                onClick={handleReset}
                style={{
                  background: '#6c757d',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '14px'
                }}
              >
                Reset to Default
              </button>
            </div>
          </div>
          
          {/* Reader Prompt Section */}
          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ color: '#495057', marginBottom: '10px' }}>Reader Prompt</h3>
            <p style={{ color: '#6c757d', fontSize: '14px', marginBottom: '15px' }}>
              Customize the prompt used for tarot readings. Use these template variables:
            </p>
            <div style={{ background: '#f8f9fa', padding: '15px', borderRadius: '8px', marginBottom: '15px', fontSize: '13px', fontFamily: 'monospace' }}>
              <div><strong>{'{QUESTION}'}</strong> - The user's question or "General guidance"</div>
              <div><strong>{'{CARDS_DESCRIPTION}'}</strong> - Full card spread with positions and orientations</div>
              <div><strong>{'{DECK_THEME}'}</strong> - Deck theme name</div>
            </div>
            
            <textarea
              value={tempReaderPrompt}
              onChange={(e) => setTempReaderPrompt(e.target.value)}
              style={{
                width: '100%',
                height: '250px',
                padding: '15px',
                borderRadius: '8px',
                border: '2px solid #e9ecef',
                fontSize: '13px',
                fontFamily: 'monospace',
                resize: 'vertical'
              }}
            />
            
            <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
              <button 
                onClick={handleReaderSave}
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '14px'
                }}
              >
                Save Reader Prompt
              </button>
              <button 
                onClick={handleReaderReset}
                style={{
                  background: '#6c757d',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '14px'
                }}
              >
                Reset to Default
              </button>
            </div>
          </div>
          
          {/* Spread Configuration Section */}
          <div style={{ marginBottom: '30px', paddingTop: '30px', borderTop: '2px solid #e9ecef' }}>
            <h3 style={{ color: '#495057', marginBottom: '10px' }}>Spread Configuration</h3>
            <p style={{ color: '#6c757d', fontSize: '14px', marginBottom: '15px' }}>
              Customize the card spread layout. Supports 3-10 cards.
            </p>
            
            <SpreadConfigEditor 
              currentConfig={spreadConfig}
              onSave={(newConfig) => {
                setSpreadConfig(newConfig);
                localStorage.setItem('tarot-spread-config', JSON.stringify(newConfig));
                alert('Spread configuration saved!');
              }}
            />
          </div>
        </div>
      </div>
    );
  };
  
  const SpreadConfigEditor = ({ currentConfig, onSave }) => {
    const presets = {
      threeCard: {
        name: 'Three-Card Spread',
        positions: [
          { label: 'Past', meaning: 'What has led to this moment' },
          { label: 'Present', meaning: 'The current situation or energy' },
          { label: 'Future', meaning: 'Where this path is leading' }
        ]
      },
      celticCross: {
        name: 'Celtic Cross',
        positions: [
          { label: 'Present', meaning: 'Current situation' },
          { label: 'Challenge', meaning: 'What crosses you' },
          { label: 'Foundation', meaning: 'Basis of the situation' },
          { label: 'Past', meaning: 'Recent past' },
          { label: 'Crown', meaning: 'Possible future' },
          { label: 'Near Future', meaning: 'Immediate future' },
          { label: 'Self', meaning: 'Your attitude' },
          { label: 'Environment', meaning: 'External influences' },
          { label: 'Hopes/Fears', meaning: 'Inner emotions' },
          { label: 'Outcome', meaning: 'Final result' }
        ]
      }
    };
    
    const [editing, setEditing] = useState(false);
    const [tempConfig, setTempConfig] = useState(currentConfig || presets.threeCard);
    
    const handlePreset = (preset) => {
      setTempConfig(preset);
      onSave(preset);
      setEditing(false);
    };
    
    return (
      <div>
        <div style={{ marginBottom: '15px' }}>
          <strong style={{ display: 'block', marginBottom: '10px', fontSize: '14px' }}>Quick Presets:</strong>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={() => handlePreset(presets.threeCard)}
              style={{
                padding: '10px 20px',
                background: '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '13px'
              }}
            >
              Three-Card
            </button>
            <button
              onClick={() => handlePreset(presets.celticCross)}
              style={{
                padding: '10px 20px',
                background: '#764ba2',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '13px'
              }}
            >
              Celtic Cross (10 cards)
            </button>
          </div>
        </div>
        
        <div style={{ background: '#f8f9fa', padding: '15px', borderRadius: '8px', fontSize: '13px' }}>
          <strong>Current Spread:</strong> {tempConfig.name} ({tempConfig.positions.length} cards)
        </div>
      </div>
    );
  };

  return (
    <>
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: 'Georgia', serif;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
          padding: 20px;
        }

        .container {
          max-width: 1400px;
          margin: 0 auto;
          background: white;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
          overflow: hidden;
        }

        header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 40px;
          text-align: center;
        }

        h1 {
          font-size: 3em;
          margin-bottom: 10px;
          text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .theme-subtitle {
          font-size: 1.2em;
          opacity: 0.9;
          margin-bottom: 20px;
        }

        .suit-symbols-header {
          display: flex;
          gap: 20px;
          justify-content: center;
          margin: 20px 0;
          opacity: 0.7;
        }

        .header-suit-symbol {
          width: 40px;
          height: 40px;
          transition: all 0.3s ease;
        }

        .header-suit-symbol:hover {
          opacity: 1;
          transform: scale(1.15);
        }

        .header-suit-symbol svg {
          width: 100%;
          height: 100%;
          filter: drop-shadow(1px 1px 2px rgba(0, 0, 0, 0.3));
        }

        /* Restore Banner */
        .restore-banner {
          background: #fff3cd;
          border: 2px solid #ffc107;
          border-radius: 10px;
          padding: 20px;
          margin: 20px;
          color: #856404;
        }

        .restore-banner h3 {
          margin-bottom: 10px;
          color: #856404;
        }

        .restore-banner ol {
          margin-left: 20px;
          line-height: 1.8;
        }

        /* Navigation */
        .nav-tabs {
          display: flex;
          background: #f8f9fa;
          border-bottom: 3px solid #e9ecef;
          overflow-x: auto;
        }

        .nav-tab {
          flex: 1;
          padding: 20px;
          border: none;
          background: transparent;
          font-size: 1.1em;
          font-family: 'Georgia', serif;
          cursor: pointer;
          transition: all 0.3s ease;
          white-space: nowrap;
        }

        .nav-tab:hover {
          background: rgba(102, 126, 234, 0.1);
        }

        .nav-tab.active {
          background: white;
          color: #667eea;
          font-weight: bold;
          border-bottom: 3px solid #667eea;
        }

        .view {
          padding: 40px;
        }

        /* Summary View */
        .summary-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 25px;
          margin-bottom: 40px;
        }

        .summary-card {
          background: #f8f9fa;
          padding: 25px;
          border-radius: 15px;
          border-left: 5px solid #667eea;
        }

        .summary-card h3 {
          color: #2c3e50;
          margin-bottom: 20px;
          font-size: 1.5em;
        }

        .stat {
          display: flex;
          justify-content: space-between;
          padding: 12px 0;
          border-bottom: 1px solid #e9ecef;
        }

        .stat:last-child {
          border-bottom: none;
        }

        .stat-label {
          color: #6c757d;
          font-size: 1.05em;
        }

        .stat-value {
          color: #667eea;
          font-weight: bold;
          font-size: 1.2em;
        }

        .dialectic-display {
          padding: 12px 0;
          color: #495057;
          font-size: 1.05em;
        }

        /* Export Button */
        .export-button {
          width: 100%;
          padding: 15px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 10px;
          font-size: 1.05em;
          font-family: 'Georgia', serif;
          cursor: pointer;
          transition: all 0.3s ease;
          font-weight: bold;
        }

        .export-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .export-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .export-status {
          margin-top: 15px;
          padding: 12px;
          background: #d4edda;
          border: 1px solid #c3e6cb;
          border-radius: 8px;
          color: #155724;
          font-size: 0.95em;
        }

        /* Major Arcana */
        .story-section {
          background: #f8f9fa;
          padding: 30px;
          border-radius: 15px;
          margin-bottom: 30px;
          border-left: 5px solid #667eea;
        }

        .story-section h2 {
          color: #2c3e50;
          margin-bottom: 20px;
          font-size: 2em;
        }

        .story-section p {
          color: #495057;
          line-height: 1.8;
          font-size: 1.05em;
        }

        .visual-style-section {
          background: #e7f1ff;
          padding: 25px;
          border-radius: 15px;
          margin-bottom: 30px;
          border-left: 5px solid #667eea;
        }

        .visual-style-section h3 {
          color: #2c3e50;
          margin-bottom: 15px;
        }

        .visual-style-section p {
          color: #495057;
          line-height: 1.6;
        }

        .cards-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 25px;
        }

        .major-card {
          background: white;
          border: 2px solid #e9ecef;
          border-radius: 15px;
          padding: 25px;
          transition: all 0.3s ease;
        }

        .major-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
          border-color: #667eea;
        }

        .major-card-header {
          display: flex;
          align-items: center;
          gap: 15px;
          margin-bottom: 15px;
        }

        .major-number {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          flex-shrink: 0;
        }

        .major-card h4 {
          color: #2c3e50;
          font-size: 1.4em;
        }

        .major-role {
          color: #667eea;
          font-style: italic;
          margin-bottom: 15px;
        }

        .major-image {
          color: #6c757d;
          font-size: 0.95em;
          line-height: 1.6;
          margin-bottom: 20px;
          padding-bottom: 20px;
          border-bottom: 1px solid #e9ecef;
        }

        /* Minor Arcana Split View */
        .minor-arcana-container {
          display: grid;
          grid-template-columns: 450px 1fr;
          gap: 30px;
          height: calc(100vh - 300px);
          min-height: 600px;
        }

        .minor-arcana-sidebar {
          overflow-y: auto;
          overflow-x: hidden;
          padding-right: 10px;
        }

        .minor-arcana-sidebar h2 {
          color: #2c3e50;
          font-size: 2em;
          margin-bottom: 25px;
          position: sticky;
          top: 0;
          background: white;
          padding: 10px 0;
          z-index: 10;
        }

        .minor-arcana-content {
          overflow-y: auto;
          overflow-x: hidden;
          padding-right: 10px;
        }

        .minor-arcana-content h2 {
          color: #2c3e50;
          font-size: 2em;
          margin-bottom: 25px;
          position: sticky;
          top: 0;
          background: white;
          padding: 10px 0;
          z-index: 10;
        }

        /* Suit Cards */
        .suit-detail-card {
          background: white;
          border: 2px solid #e9ecef;
          border-radius: 15px;
          padding: 25px;
          margin-bottom: 20px;
          transition: all 0.3s ease;
        }

        .suit-detail-card:hover {
          border-color: #667eea;
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .suit-card-header {
          display: flex;
          align-items: center;
          gap: 20px;
          margin-bottom: 20px;
          padding-bottom: 20px;
          border-bottom: 2px solid #e9ecef;
        }

        .suit-symbol-medium {
          width: 70px;
          height: 70px;
          flex-shrink: 0;
        }

        .suit-symbol-medium svg {
          width: 100%;
          height: 100%;
        }

        .suit-detail-card h3 {
          color: #2c3e50;
          font-size: 1.6em;
          margin-bottom: 5px;
        }

        .suit-symbol-desc {
          color: #6c757d;
          font-style: italic;
          font-size: 0.9em;
        }

        .suit-visual-style {
          color: #495057;
          line-height: 1.7;
          margin-bottom: 20px;
          font-size: 0.95em;
        }

        /* Rank Cards */
        .ranks-list {
          display: flex;
          flex-direction: column;
          gap: 20px;
          margin-bottom: 40px;
        }

        .rank-detail-card {
          background: white;
          border: 2px solid #e9ecef;
          border-radius: 15px;
          padding: 25px;
          transition: all 0.3s ease;
        }

        .rank-detail-card:hover {
          border-color: #667eea;
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .rank-card-header {
          display: flex;
          align-items: center;
          gap: 20px;
          margin-bottom: 15px;
          padding-bottom: 15px;
          border-bottom: 2px solid #e9ecef;
        }

        .rank-number {
          width: 50px;
          height: 50px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          font-size: 1.3em;
          flex-shrink: 0;
        }

        .rank-detail-card h4 {
          color: #2c3e50;
          font-size: 1.4em;
          margin-bottom: 5px;
        }

        .rank-role {
          color: #667eea;
          font-style: italic;
          font-size: 0.95em;
        }

        .rank-image-content {
          color: #6c757d;
          line-height: 1.6;
          margin-bottom: 20px;
          font-size: 0.95em;
        }

        /* Consistent Tag Rendering */
        .tag-section {
          margin-bottom: 15px;
        }

        .tag-section:last-child {
          margin-bottom: 0;
        }

        .tag-label {
          font-weight: bold;
          color: #2c3e50;
          font-size: 0.9em;
          margin-bottom: 8px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .tag-label.inverted {
          color: #6c757d;
        }

        .tag-container {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        /* Browser View */
        .browser-container {
          display: grid;
          grid-template-columns: 400px 1fr;
          gap: 30px;
          height: calc(100vh - 300px);
          min-height: 600px;
        }

        .browser-sidebar {
          display: flex;
          flex-direction: column;
          gap: 20px;
          height: 100%;
          overflow: hidden;
        }

        .browser-controls {
          display: flex;
          flex-direction: column;
          gap: 15px;
          flex-shrink: 0;
        }

        .search-input {
          padding: 12px;
          border: 2px solid #e9ecef;
          border-radius: 10px;
          font-size: 1em;
          font-family: 'Georgia', serif;
        }

        .search-input:focus {
          outline: none;
          border-color: #667eea;
        }

        .filter-buttons {
          display: flex;
          gap: 10px;
        }

        .filter-btn {
          flex: 1;
          padding: 10px;
          border: 2px solid #e9ecef;
          background: white;
          border-radius: 8px;
          font-family: 'Georgia', serif;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .filter-btn:hover {
          border-color: #667eea;
          background: rgba(102, 126, 234, 0.1);
        }

        .filter-btn.active {
          background: #667eea;
          color: white;
          border-color: #667eea;
        }

        .card-list {
          flex: 1;
          min-height: 0;
          overflow-y: auto;
          overflow-x: hidden;
          display: flex;
          flex-direction: column;
          gap: 10px;
          padding-right: 10px;
        }

        .card-list-item {
          background: white;
          border: 2px solid #e9ecef;
          border-radius: 24px;
          padding: 0;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: stretch;
          gap: 0;
          position: relative;
          overflow: hidden;
          min-height: 48px;
        }

        .card-list-item:hover {
          border-color: #667eea;
          transform: translateX(3px);
          box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
        }

        .card-list-item.active {
          border-color: #667eea;
          background: rgba(102, 126, 234, 0.05);
          box-shadow: 0 2px 12px rgba(102, 126, 234, 0.15);
        }
        
        .list-item-badge {
          width: 50px;
          flex-shrink: 0;
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: center;
          gap: 4px;
          padding: 10px 8px;
        }
        
        .list-item-badge.badge-major {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .list-item-badge.badge-minor {
          background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        }
        
        .badge-rank {
          color: white;
          font-size: 1em;
          font-weight: 700;
          line-height: 1;
        }
        
        .badge-suit-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          opacity: 0.95;
        }
        
        .list-item-name {
          color: #2c3e50;
          font-size: 1em;
          font-weight: 600;
          line-height: 1.3;
          flex: 1;
          padding: 12px 16px;
        }
        
        .list-item-artwork-badge {
          width: 48px;
          flex-shrink: 0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1.1em;
          padding: 10px 8px;
        }

        .browser-detail {
          height: 100%;
          overflow-y: auto;
          overflow-x: hidden;
          padding-right: 10px;
        }

        .detail-empty {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100%;
          color: #6c757d;
          font-size: 1.2em;
          font-style: italic;
        }

        .detail-content {
          background: white;
          border: 2px solid #e9ecef;
          border-radius: 15px;
          padding: 30px;
        }

        .detail-header {
          margin-bottom: 30px;
          padding-bottom: 20px;
          border-bottom: 3px solid #e9ecef;
        }

        .detail-badge {
          display: inline-block;
          padding: 6px 16px;
          border-radius: 15px;
          font-size: 0.9em;
          margin-bottom: 15px;
          font-weight: bold;
        }

        .detail-number {
          display: inline-block;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          width: 50px;
          height: 50px;
          border-radius: 50%;
          text-align: center;
          line-height: 50px;
          font-size: 1.3em;
          font-weight: bold;
          margin-bottom: 15px;
        }

        .detail-name {
          color: #2c3e50;
          font-size: 2em;
          margin-bottom: 10px;
          font-weight: bold;
        }

        .detail-role {
          color: #667eea;
          font-size: 1.1em;
          font-style: italic;
          margin-bottom: 5px;
        }

        .detail-suit {
          color: #6c757d;
          font-size: 1.05em;
        }

        .detail-section {
          margin-bottom: 30px;
        }

        .detail-section-title {
          color: #2c3e50;
          font-size: 1.2em;
          margin-bottom: 12px;
          font-weight: 600;
        }
        
        .detail-subsection {
          color: #667eea;
          font-size: 0.95em;
          margin-bottom: 10px;
        }
        
        .detail-description-compact {
          color: #495057;
          line-height: 1.7;
          font-size: 0.95em;
          margin-bottom: 8px;
        }

        .detail-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
        }

        .detail-tag {
          background: #e7f1ff;
          color: #667eea;
          padding: 8px 16px;
          border-radius: 20px;
          font-size: 0.95em;
        }

        .detail-tag.inverted {
          background: #f8f9fa;
          color: #6c757d;
        }
        
        .detail-tags-compact {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
        }
        
        .detail-tag-compact {
          background: #e7f1ff;
          color: #667eea;
          padding: 4px 10px;
          border-radius: 12px;
          font-size: 0.8em;
        }
        
        .detail-tag-compact.inverted {
          background: #f8f9fa;
          color: #6c757d;
        }

        .detail-description {
          color: #495057;
          line-height: 1.8;
          font-size: 1.05em;
          white-space: normal;
          word-wrap: break-word;
          overflow-wrap: break-word;
        }
        
        /* Collapsible Info Boxes */
        .detail-info-box {
          margin-top: 20px;
          border: 2px solid #e9ecef;
          border-radius: 12px;
          overflow: hidden;
          background: #f8f9fa;
          transition: all 0.2s ease;
        }
        
        .detail-info-box:hover {
          border-color: #dee2e6;
        }
        
        .detail-info-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 15px 20px;
          cursor: pointer;
          user-select: none;
          background: white;
          transition: background 0.2s ease;
        }
        
        .detail-info-header:hover {
          background: #f8f9fa;
        }
        
        .detail-info-title {
          font-size: 1.1em;
          font-weight: 600;
          color: #2c3e50;
        }
        
        .detail-info-subtitle {
          font-weight: 400;
          color: #667eea;
          font-size: 0.9em;
        }
        
        .detail-info-toggle {
          font-size: 1.5em;
          color: #667eea;
          font-weight: 300;
          width: 24px;
          text-align: center;
        }
        
        .detail-info-content {
          padding: 20px;
          background: white;
          border-top: 1px solid #e9ecef;
          animation: slideDown 0.2s ease;
        }
        
        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .detail-info-field {
          margin-bottom: 18px;
        }
        
        .detail-info-field:last-child {
          margin-bottom: 0;
        }
        
        .detail-info-field strong {
          display: block;
          color: #2c3e50;
          margin-bottom: 8px;
          font-size: 0.95em;
        }
        
        .detail-info-field p {
          margin: 0;
          color: #495057;
          line-height: 1.6;
          font-size: 0.95em;
        }

        /* Visual Generation */
        .visual-container-primary {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 15px;
          margin-bottom: 30px;
        }
        
        .no-visual-placeholder {
          position: relative;
          width: 400px;
          height: 600px;
          background: #f8f9fa;
          border-radius: 12px;
          border: 2px dashed #dee2e6;
          overflow: hidden;
        }
        
        .no-visual-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          padding: 40px 20px;
          gap: 15px;
        }
        
        .no-visual-content p {
          color: #6c757d;
          margin: 0;
          font-size: 1.1em;
        }
        
        .visual-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 15px;
        }

        .no-visual {
          text-align: center;
          padding: 40px;
          background: #f8f9fa;
          border-radius: 10px;
          border: 2px dashed #e9ecef;
        }

        .no-visual p {
          color: #6c757d;
          margin-bottom: 20px;
          font-size: 1.05em;
        }

        .generate-visual-button, .regenerate-button {
          padding: 12px 30px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 25px;
          font-size: 1.05em;
          font-family: 'Georgia', serif;
          cursor: pointer;
          transition: all 0.3s ease;
          font-weight: bold;
        }

        .generate-visual-button:hover:not(:disabled),
        .regenerate-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .generate-visual-button:disabled,
        .regenerate-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .regenerate-button {
          background: #6c757d;
        }

        .regenerate-button:hover:not(:disabled) {
          background: #5a6268;
        }

        /* Readings */
        .readings-container {
          max-width: 1400px;
          margin: 0 auto;
        }

        .readings-intro {
          text-align: center;
          margin-bottom: 30px;
          padding-bottom: 20px;
          border-bottom: 3px solid #e9ecef;
        }

        .readings-intro h2 {
          color: #2c3e50;
          font-size: 2em;
          margin-bottom: 10px;
        }

        .question-section label,
        .question-display label {
          display: block;
          color: #2c3e50;
          font-size: 1.1em;
          margin-bottom: 10px;
          font-weight: bold;
        }
        
        .question-display {
          margin-bottom: 20px;
        }
        
        .fixed-question {
          width: 100%;
          padding: 15px;
          font-size: 1.05em;
          border: 2px solid #e9ecef;
          border-radius: 10px;
          font-family: 'Georgia', serif;
          background: #f8f9fa;
          color: #495057;
          font-style: italic;
          min-height: 60px;
        }

        .question-input {
          width: 100%;
          padding: 15px;
          font-size: 1.05em;
          border: 2px solid #e9ecef;
          border-radius: 10px;
          font-family: 'Georgia', serif;
          resize: vertical;
        }

        .question-input:focus {
          outline: none;
          border-color: #667eea;
        }

        .reading-buttons {
          display: flex;
          gap: 15px;
          margin-bottom: 30px;
          flex-wrap: wrap;
        }

        .draw-button, .generate-button, .reset-button {
          padding: 15px 30px;
          border: none;
          border-radius: 25px;
          font-size: 1.05em;
          font-family: 'Georgia', serif;
          cursor: pointer;
          transition: all 0.3s ease;
          font-weight: bold;
        }

        .draw-button {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          flex: 1;
        }

        .draw-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .generate-button {
          background: #28a745;
          color: white;
          flex: 1;
        }

        .generate-button:hover:not(:disabled) {
          background: #218838;
          transform: translateY(-2px);
        }

        .generate-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .reset-button {
          background: #6c757d;
          color: white;
        }

        .reset-button:hover {
          background: #5a6268;
          transform: translateY(-2px);
        }

        .spread-display {
          margin-top: 30px;
        }

        .spread-positions {
          display: grid;
          gap: 25px;
          margin-bottom: 30px;
          width: 100%;
        }
        
        /* Dynamic grid based on number of cards */
        .spread-3 {
          grid-template-columns: repeat(3, minmax(250px, 1fr));
          max-width: 1200px;
          margin: 0 auto;
        }
        
        .spread-4 {
          grid-template-columns: repeat(2, minmax(250px, 1fr));
          max-width: 800px;
          margin: 0 auto;
        }
        
        .spread-5 {
          grid-template-columns: repeat(3, minmax(200px, 1fr));
          max-width: 1000px;
          margin: 0 auto;
        }
        
        .spread-6 {
          grid-template-columns: repeat(3, minmax(200px, 1fr));
          max-width: 1000px;
          margin: 0 auto;
        }
        
        .spread-7, .spread-8, .spread-9, .spread-10 {
          grid-template-columns: repeat(5, minmax(180px, 1fr));
        }

        .reading-card-position {
          text-align: center;
          transition: opacity 0.3s ease-out, transform 0.3s ease-out;
          display: flex;
          flex-direction: column;
        }
        
        .card-visual-wrapper {
          position: relative;
          width: 100%;
          height: 210px;
          margin-bottom: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          isolation: isolate;
        }
        
        .card-visual-canvas {
          width: 400px;
          height: 600px;
          transform-origin: center center;
          transition: transform 0.75s ease-out;
          position: relative;
        }
        
        .card-visual-canvas canvas {
          display: block !important;
          position: relative !important;
        }
        
        .reading-card-content {
          padding: 0 10px;
        }
        }

        .position-label {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 10px;
          border-radius: 10px 10px 0 0;
          font-weight: bold;
          font-size: 1.1em;
        }

        .reading-card {
          background: white;
          border: 2px solid #e9ecef;
          border-top: none;
          padding: 15px;
          min-height: 120px;
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          gap: 10px;
        }

        .reading-card-name {
          color: #2c3e50;
          font-size: 1.1em;
          font-weight: bold;
        }

        .reading-card-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
          justify-content: center;
        }

        .position-meaning {
          background: #f8f9fa;
          padding: 10px;
          border-radius: 0 0 10px 10px;
          color: #6c757d;
          font-style: italic;
          font-size: 0.95em;
        }

        .reading-section {
          background: #f8f9fa;
          padding: 30px;
          border-radius: 15px;
          border-left: 5px solid #667eea;
        }

        .reading-section h3 {
          color: #2c3e50;
          font-size: 1.8em;
          margin-bottom: 20px;
        }

        .reading-content {
          color: #495057;
          line-height: 1.8;
          font-size: 1.05em;
        }

        .reading-content p {
          margin-bottom: 15px;
        }

        @media (max-width: 1200px) {
          .browser-container {
            grid-template-columns: 1fr;
            height: auto;
          }

          .browser-sidebar {
            max-height: 400px;
          }
          
          .spread-7, .spread-8, .spread-9, .spread-10 {
            grid-template-columns: repeat(3, minmax(180px, 1fr));
          }
        }
        
        @media (max-width: 900px) {
          .spread-5, .spread-6,
          .spread-7, .spread-8, .spread-9, .spread-10 {
            grid-template-columns: repeat(2, minmax(200px, 1fr));
          }
        }

        @media (max-width: 768px) {
          .spread-positions,
          .spread-3, .spread-4, .spread-5, .spread-6,
          .spread-7, .spread-8, .spread-9, .spread-10 {
            grid-template-columns: 1fr;
            max-width: 400px;
            margin: 0 auto;
          }

          .reading-buttons {
            flex-direction: column;
          }

          .draw-button, .generate-button, .reset-button {
            width: 100%;
          }
        }
      `}</style>
      
      <div className="container">
        <header>
          <div style={{ position: 'relative' }}>
            <button 
              onClick={() => setShowSettings(!showSettings)}
              style={{
                position: 'absolute',
                right: '20px',
                top: '20px',
                background: 'rgba(255, 255, 255, 0.2)',
                border: '2px solid white',
                color: 'white',
                padding: '10px 20px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '14px',
                fontWeight: 'bold',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => e.target.style.background = 'rgba(255, 255, 255, 0.3)'}
              onMouseOut={(e) => e.target.style.background = 'rgba(255, 255, 255, 0.2)'}
            >
              ⚙️ Settings
            </button>
          </div>
          <h1>{typeof deckData.theme === 'string' ? deckData.theme : deckData.theme.name}</h1>
          <p className="theme-subtitle">Custom Tarot Deck v5.5.1</p>
          <div className="suit-symbols-header">
            {deckData.minor_arcana.suits.map((suit, idx) => {
              // Replace the SVG color with white for better contrast
              const whiteSvg = suit.symbol_svg?.replace(/#667eea/g, '#ffffff').replace(/stroke="#[^"]*"/g, 'stroke="#ffffff"').replace(/fill="#667eea"/g, 'fill="#ffffff"');
              return whiteSvg && (
                <div 
                  key={idx}
                  className="header-suit-symbol"
                  dangerouslySetInnerHTML={{ __html: whiteSvg }}
                  title={suit.name}
                />
              );
            })}
          </div>
        </header>

        {showRestoreBanner && (
          <div className="restore-banner">
            <h3>No saved visuals found</h3>
            <p style={{ fontSize: '13px', color: '#666', marginBottom: '12px' }}>
              Looking for localStorage key: <code style={{ background: '#f0f0f0', padding: '2px 6px', borderRadius: '3px' }}>{getStorageKey()}</code>
            </p>
            <p>To restore from a backup:</p>
            <ol>
              <li><strong>If you have a DeckVisualsLoader artifact</strong> in this conversation:
                <ul style={{ marginTop: '8px', marginBottom: '8px' }}>
                  <li>Scroll up and open it</li>
                  <li>It will auto-restore your visuals</li>
                  <li>Close that tab and refresh this page</li>
                </ul>
              </li>
              <li><strong>If you have a backup JSON file</strong>:
                <ul style={{ marginTop: '8px' }}>
                  <li>Upload the file to this conversation</li>
                  <li>Ask Claude to create a loader from it</li>
                  <li>Follow the steps above</li>
                </ul>
              </li>
            </ol>
          </div>
        )}
        
        <div className="nav-tabs">
          <button 
            className={`nav-tab ${activeView === 'summary' ? 'active' : ''}`}
            onClick={() => setActiveView('summary')}
          >
            Deck Summary
          </button>
          <button 
            className={`nav-tab ${activeView === 'major' ? 'active' : ''}`}
            onClick={() => setActiveView('major')}
          >
            Major Arcana
          </button>
          <button 
            className={`nav-tab ${activeView === 'suits' ? 'active' : ''}`}
            onClick={() => setActiveView('suits')}
          >
            Minor Arcana
          </button>
          <button 
            className={`nav-tab ${activeView === 'browser' ? 'active' : ''}`}
            onClick={() => setActiveView('browser')}
          >
            Card Browser
          </button>
          <button 
            className={`nav-tab ${activeView === 'readings' ? 'active' : ''}`}
            onClick={() => setActiveView('readings')}
          >
            Readings
          </button>
        </div>
        
        {activeView === 'summary' && <SummaryView />}
        {activeView === 'major' && <MajorArcanaView />}
        {activeView === 'suits' && <SuitsRanksView />}
        {activeView === 'browser' && <BrowserView />}
        {activeView === 'readings' && <ReadingsView />}
      </div>
      
      <SettingsPanel />
    </>
  );
};

export default TarotDeckViewer;
