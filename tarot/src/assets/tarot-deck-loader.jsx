import React, { useState, useEffect, useRef } from 'react';
import { Upload, XCircle, AlertCircle, Download, Edit2, Save, X, Eye } from 'lucide-react';

class ImageGenerationManager {
  constructor() {
    this.queue = []; // Array of { slug, prompt }
    this.inFlight = new Map(); // slug -> { startTime }
    this.maxConcurrent = 3;
    this.running = false;
    this.listeners = new Map();
    this.history = [];
    this.batchStartTime = null;
    this.batchEndTime = null;
    this.telemetry = {
      totalGenerations: 0,
      totalDuration: 0,
      totalPromptTokens: 0,
      totalCompletionTokens: 0,
      minDuration: null,
      maxDuration: null,
      avgDuration: 0,
      batchElapsedTime: 0
    };
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => callback(data));
    }
  }

  async generateFromPrompt(slug, prompt) {
    const startTime = Date.now();
    
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

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    const data = await response.json();
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    // Extract token usage if available
    const usage = data.usage || {};
    const promptTokens = usage.input_tokens || 0;
    const completionTokens = usage.output_tokens || 0;
    
    return {
      code: data.content[0].text,
      duration,
      promptTokens,
      completionTokens
    };
  }

  updateTelemetry(record) {
    this.telemetry.totalGenerations++;
    this.telemetry.totalDuration += record.duration;
    this.telemetry.totalPromptTokens += record.promptTokens;
    this.telemetry.totalCompletionTokens += record.completionTokens;
    
    if (this.telemetry.minDuration === null || record.duration < this.telemetry.minDuration) {
      this.telemetry.minDuration = record.duration;
    }
    
    if (this.telemetry.maxDuration === null || record.duration > this.telemetry.maxDuration) {
      this.telemetry.maxDuration = record.duration;
    }
    
    this.telemetry.avgDuration = this.telemetry.totalDuration / this.telemetry.totalGenerations;
    
    this.emit('telemetry-updated', this.telemetry);
  }

  getActiveGenerationTimes() {
    const now = Date.now();
    const times = {};
    for (const [slug, data] of this.inFlight.entries()) {
      times[slug] = {
        elapsed: now - data.startTime
      };
    }
    return times;
  }

  // Check how many in-flight, start more if < 3
  processQueue() {
    if (!this.running) return;
    
    // Start new requests up to maxConcurrent
    while (this.inFlight.size < this.maxConcurrent && this.queue.length > 0) {
      const item = this.queue.shift();
      const { slug, prompt } = item;
      
      const startTime = Date.now();
      this.inFlight.set(slug, { startTime });
      
      this.emit('generation-started', { slug });
      
      // Start the generation
      this.generateFromPrompt(slug, prompt)
        .then(result => {
          // Remove from in-flight
          this.inFlight.delete(slug);
          
          // Record telemetry
          const record = {
            cardSlug: slug,
            startTime,
            endTime: Date.now(),
            duration: result.duration,
            promptTokens: result.promptTokens,
            completionTokens: result.completionTokens,
            success: true
          };
          
          this.history.push(record);
          this.updateTelemetry(record);
          
          this.emit('generation-success', { 
            slug, 
            code: result.code,
            telemetry: record
          });
          
          // Process more from queue
          this.processQueue();
          
          // Check if done
          if (this.queue.length === 0 && this.inFlight.size === 0) {
            this.batchEndTime = Date.now();
            this.stop();
            this.emit('batch-completed', {});
          }
        })
        .catch(error => {
          // Remove from in-flight
          this.inFlight.delete(slug);
          
          console.error(`Failed to generate visual for ${slug}:`, error);
          
          // Record failed generation
          const record = {
            cardSlug: slug,
            startTime,
            endTime: Date.now(),
            duration: Date.now() - startTime,
            promptTokens: 0,
            completionTokens: 0,
            success: false,
            error: error.message
          };
          
          this.history.push(record);
          
          this.emit('generation-error', { 
            slug,
            error: error.message,
            telemetry: record
          });
          
          // Re-queue on error
          this.queue.push(item);
          
          // Process more from queue
          this.processQueue();
        });
    }
  }

  start(jobs) {
    // jobs is array of { slug, prompt }
    this.queue = [...jobs];
    this.running = true;
    this.batchStartTime = Date.now();
    this.batchEndTime = null;
    this.emit('batch-started', { total: jobs.length });
    this.processQueue();
  }

  stop() {
    this.running = false;
    this.queue = [];
    this.batchEndTime = Date.now();
    this.emit('batch-stopped', {});
  }

  getStatus() {
    return {
      running: this.running,
      queueLength: this.queue.length,
      inFlightCount: this.inFlight.size,
      inFlightSlugs: Array.from(this.inFlight.keys())
    };
  }

  getTelemetry() {
    const now = Date.now();
    const batchElapsedTime = this.batchStartTime 
      ? (this.batchEndTime || now) - this.batchStartTime
      : 0;
    
    return {
      ...this.telemetry,
      batchElapsedTime,
      activeGenerationTimes: this.getActiveGenerationTimes()
    };
  }

  getHistory() {
    return [...this.history];
  }

  clearHistory() {
    this.history = [];
    this.telemetry = {
      totalGenerations: 0,
      totalDuration: 0,
      totalPromptTokens: 0,
      totalCompletionTokens: 0,
      minDuration: null,
      maxDuration: null,
      avgDuration: 0
    };
    this.emit('telemetry-updated', this.telemetry);
  }
}

const P5Sketch = ({ code }) => {
  const containerRef = useRef(null);
  const p5InstanceRef = useRef(null);

  useEffect(() => {
    if (!code || !containerRef.current) return;

    // Clean up existing instance
    if (p5InstanceRef.current) {
      p5InstanceRef.current.remove();
      p5InstanceRef.current = null;
    }

    // Clear the container
    containerRef.current.innerHTML = '';

    try {
      // Execute the code to get the sketch function
      const sketchFunc = new Function('return ' + code)();
      
      // Load p5.js if not already loaded
      if (typeof window.p5 === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js';
        script.onload = () => {
          p5InstanceRef.current = new window.p5(sketchFunc, containerRef.current);
        };
        document.head.appendChild(script);
      } else {
        p5InstanceRef.current = new window.p5(sketchFunc, containerRef.current);
      }
    } catch (error) {
      console.error('Error creating p5 sketch:', error);
    }

    return () => {
      if (p5InstanceRef.current) {
        p5InstanceRef.current.remove();
        p5InstanceRef.current = null;
      }
    };
  }, [code]);

  return <div ref={containerRef} className="w-full h-full" />;
};

export default function TarotDeckLoader() {
  const [deck, setDeck] = useState(null);
  const [error, setError] = useState(null);
  const [validationDetails, setValidationDetails] = useState([]);
  const [currentView, setCurrentView] = useState('summary');
  const [selectedCard, setSelectedCard] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedCard, setEditedCard] = useState(null);
  const [imageGenCard, setImageGenCard] = useState(null);
  const [generatingVisual, setGeneratingVisual] = useState(false);
  const [hideDetails, setHideDetails] = useState(false);
  const [p5Instance, setP5Instance] = useState(null);
  const [batchMode, setBatchMode] = useState(false);
  const [batchRunning, setBatchRunning] = useState(false);
  const [batchProgress, setBatchProgress] = useState({ completed: 0, inProgress: [], remaining: 0 });
  const [generatingCards, setGeneratingCards] = useState(new Set());
  const [telemetry, setTelemetry] = useState({
    totalGenerations: 0,
    totalDuration: 0,
    totalPromptTokens: 0,
    totalCompletionTokens: 0,
    minDuration: null,
    maxDuration: null,
    avgDuration: 0,
    batchElapsedTime: 0,
    activeGenerationTimes: {}
  });
  
  // Spread definitions
  const spreadDefinitions = {
    single: {
      name: "Single Card",
      purpose: "Quick insight or daily guidance",
      instructions: "Focus on your question and draw a single card for direct guidance.",
      slots: [
        { name: "The Card", meaning: "Direct answer or guidance for your question" }
      ]
    },
    threeCard: {
      name: "Three Card Spread",
      purpose: "Understanding the flow of a situation through time",
      instructions: "This spread reveals the progression from past influences through present circumstances to future possibilities.",
      slots: [
        { name: "Past", meaning: "Past influences and foundations affecting the situation" },
        { name: "Present", meaning: "Current energies and circumstances at play" },
        { name: "Future", meaning: "Likely outcome or future direction based on current path" }
      ]
    },
    celticCross: {
      name: "Celtic Cross",
      purpose: "Comprehensive exploration of a complex situation",
      instructions: "This classic spread provides deep insight into all aspects of your question.",
      slots: [
        { name: "Present Position", meaning: "The current situation or central theme" },
        { name: "Challenge", meaning: "Immediate obstacle or crossing influence" },
        { name: "Foundation", meaning: "Root cause or basis of the situation" },
        { name: "Recent Past", meaning: "Events or influences now passing" },
        { name: "Possible Future", meaning: "Potential outcome if current path continues" },
        { name: "Near Future", meaning: "What is approaching in the immediate term" },
        { name: "Self", meaning: "Your attitude, role, or how you see yourself" },
        { name: "External Influences", meaning: "Environment, others, or external factors" },
        { name: "Hopes and Fears", meaning: "What you hope for or fear about this situation" },
        { name: "Outcome", meaning: "Final result or resolution of the matter" }
      ]
    }
  };
  
  // Reading state
  const [readingQuestion, setReadingQuestion] = useState('');
  const [selectedSpreadType, setSelectedSpreadType] = useState('single');
  const [currentSpread, setCurrentSpread] = useState(null);
  const [generatingReading, setGeneratingReading] = useState(false);
  const [readingResult, setReadingResult] = useState(null);
  const [showReadingSettings, setShowReadingSettings] = useState(false);
  const [confirmRemoveVisual, setConfirmRemoveVisual] = useState(null);
  const [readingPromptTemplate, setReadingPromptTemplate] = useState(`You are an experienced tarot reader providing a thoughtful, insightful reading. You have a sense of humor, and engage jovially with the querent.

Question: {{QUESTION}}

Spread: {{SPREAD_NAME}}
{{SPREAD_PURPOSE}}

Cards drawn:
{{CARDS_DESCRIPTION}}

Please provide a comprehensive reading that:
1. Addresses the question directly
2. Interprets each card in its position, considering whether it's upright or inverted
3. Weaves the cards together into a cohesive narrative
4. Offers practical guidance and insight

Your response should be conversational, providing a reading for each card as if the future cards have not yet been revealed. After each card, you "flip" the next one and continue the reading. Your response should be grouped into paragraphs, and end with a summary that answers the question as directly as possible based on the reading above.`);
  
  const managerRef = useRef(null);
  
  // Initialize manager
  useEffect(() => {
    if (!managerRef.current) {
      managerRef.current = new ImageGenerationManager();
      
      // Set up event listeners
      managerRef.current.on('generation-started', ({ slug }) => {
        setGeneratingCards(prev => new Set(prev).add(slug));
      });
      
      managerRef.current.on('generation-success', ({ slug }) => {
        setGeneratingCards(prev => {
          const newSet = new Set(prev);
          newSet.delete(slug);
          return newSet;
        });
      });
      
      managerRef.current.on('generation-success', ({ slug, code }) => {
        // Update deck state when generation completes
        setDeck(currentDeck => {
          if (!currentDeck || !currentDeck.cards || !currentDeck.cards[slug]) {
            console.error(`Cannot update card ${slug} - invalid deck state`, {
              hasDeck: !!currentDeck,
              hasCards: !!currentDeck?.cards,
              hasSlug: !!currentDeck?.cards?.[slug],
              slug
            });
            return currentDeck || null;
          }
          
          return {
            ...currentDeck,
            cards: {
              ...currentDeck.cards,
              [slug]: {
                ...currentDeck.cards[slug],
                visuals: {
                  ...(currentDeck.cards[slug].visuals || {}),
                  code: code
                }
              }
            }
          };
        });
        
        // If this is the selected card, update it too
        setSelectedCard(current => {
          if (current?.slug === slug) {
            return null; // Will be re-fetched from deck
          }
          return current;
        });
      });
      
      managerRef.current.on('generation-error', ({ slug }) => {
        setGeneratingCards(prev => {
          const newSet = new Set(prev);
          newSet.delete(slug);
          return newSet;
        });
      });
      
      managerRef.current.on('batch-completed', () => {
        setBatchRunning(false);
      });
      
      managerRef.current.on('batch-stopped', () => {
        setBatchRunning(false);
      });
      
      managerRef.current.on('telemetry-updated', (newTelemetry) => {
        setTelemetry(newTelemetry);
      });
    }
  }, []);
  
  // Update active generation times every second
  useEffect(() => {
    if (!batchRunning && generatingCards.size === 0) return;
    
    const interval = setInterval(() => {
      if (managerRef.current) {
        const fullTelemetry = managerRef.current.getTelemetry();
        setTelemetry(fullTelemetry);
      }
    }, 1000);
    
    return () => clearInterval(interval);
  }, [batchRunning, generatingCards]);
  const [promptTemplate, setPromptTemplate] = useState(`Create a p5.js sketch for a tarot card in a deck with these attributes:

## Deck Details
Deck Theme: {THEME_NAME}
Theme Description: {THEME_DESCRIPTION}

## Card Details
Card Name: {CARD_NAME} ({ARCANA} arcana)
Card Description: {CARD_DESCRIPTION}
Rank: {RANK_NAME} ({RANK_NUMBER})
Suit: {SUIT_NAME} // blank for major arcana
Upright Meaning: {UPRIGHT_MEANING}
Inverted Meaning: {INVERTED_MEANING}

Visual Instructions:
- Style Guidance: {STYLE_GUIDANCE}
- Content Guidance: {CONTENT_GUIDANCE}

Requested Card Visualization, given all of the above context: 
\`\`\`
{DETAILED_DESCRIPTION}
\`\`\`

Create an engaging, creative p5.js sketch that captures the essence of this card. The sketch should be:
- Animated or dynamic (use motion, transformation, particle systems, etc.)
- Subtly interactive (respond to mouse movement or clicks in a way that playfully engages with the themes depicted)
- Visually striking with good use of color and composition, paying close attention to the visual style specified
- 400x600 pixels (standard tarot card proportions)
- Complete and self-contained
- Focus on the artistic visual content ONLY (text content will be overload separately)

Return ONLY the p5.js code wrapped in a function called sketch(p) for instance mode. Do not include markdown code blocks or any other text. Start directly with:

function sketch(p) {
  p.setup = function() {
    p.createCanvas(400, 600);
    // your code
  };
  
  p.draw = function() {
    // your code
  };
}`);
  
  // Update batch progress whenever deck or generatingCards changes
  useEffect(() => {
    if (deck) {
      const allCards = Object.values(deck.cards);
      const completed = allCards.filter(card => card.visuals?.code).length;
      const inProgress = Array.from(generatingCards);
      const remaining = allCards.filter(card => !card.visuals?.code && !generatingCards.has(card.slug)).length;
      setBatchProgress({ completed, inProgress, remaining });
    }
  }, [deck, generatingCards]);

  const validateDeck = (data) => {
    const errors = [];
    const warnings = [];

    if (!data.name || typeof data.name !== 'string') {
      errors.push('Missing or invalid deck name');
    }
    if (!data.slug || typeof data.slug !== 'string') {
      errors.push('Missing or invalid deck slug');
    }
    if (!data.version || typeof data.version !== 'string') {
      errors.push('Missing or invalid version');
    }

    if (!data.theme) {
      errors.push('Missing theme object');
    } else {
      if (!data.theme.name) errors.push('Theme missing name');
      if (!data.theme.description) errors.push('Theme missing description');
      if (!data.theme.creator) warnings.push('Theme missing creator');
    }

    if (!data.suits || typeof data.suits !== 'object') {
      errors.push('Missing suits object');
    } else {
      const suitCount = Object.keys(data.suits).length;
      if (suitCount !== 4) {
        errors.push(`Expected 4 suits, found ${suitCount}`);
      }
    }

    if (!data.ranks || typeof data.ranks !== 'object') {
      errors.push('Missing ranks object');
    } else {
      const rankCount = Object.keys(data.ranks).length;
      if (rankCount !== 14) {
        errors.push(`Expected 14 ranks, found ${rankCount}`);
      }
    }

    if (!data.cards || typeof data.cards !== 'object') {
      errors.push('Missing cards object');
    } else {
      const cards = Object.values(data.cards);
      const minorCards = cards.filter(c => c.arcana === 'minor');
      
      if (minorCards.length !== 56) {
        errors.push(`Expected 56 minor arcana cards, found ${minorCards.length}`);
      }
      
      const majorCards = cards.filter(c => c.arcana === 'major');
      if (majorCards.length === 0) {
        warnings.push('No major arcana cards found');
      }
    }

    return { errors, warnings };
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const jsonData = JSON.parse(e.target.result);
        const { errors, warnings } = validateDeck(jsonData);
        
        setValidationDetails([...errors, ...warnings]);
        
        if (errors.length > 0) {
          setError(`Validation failed with ${errors.length} error(s)`);
          setDeck(null);
        } else {
          setDeck(jsonData);
          setError(null);
          setCurrentView('summary');
        }
      } catch (err) {
        setError(`Failed to parse JSON: ${err.message}`);
        setDeck(null);
        setValidationDetails([]);
      }
    };
    reader.readAsText(file);
  };

  const handleDownloadDeck = () => {
    if (!deck) return;
    
    const jsonStr = JSON.stringify(deck, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${deck.slug || 'tarot-deck'}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getRomanNumeral = (num) => {
    const romanNumerals = {
      0: '0', 1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
      6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X',
      11: 'XI', 12: 'XII', 13: 'XIII', 14: 'XIV', 15: 'XV',
      16: 'XVI', 17: 'XVII', 18: 'XVIII', 19: 'XIX', 20: 'XX',
      21: 'XXI', 22: 'XXII'
    };
    return romanNumerals[num] || num.toString();
  };

  const SuitSymbol = ({ suitSlug, color = 'currentColor', size = 16 }) => {
    if (!deck?.suits?.[suitSlug]) return null;
    const suit = deck.suits[suitSlug];
    
    try {
      // Parse the SVG and inject the color
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(suit.symbol.svg, 'image/svg+xml');
      const svgElement = svgDoc.querySelector('svg');
      
      if (svgElement) {
        // Find all elements with fill attributes and update them
        const elementsWithFill = svgElement.querySelectorAll('[fill]');
        elementsWithFill.forEach(el => {
          if (el.getAttribute('fill') !== 'none' && el.getAttribute('fill') !== 'white') {
            el.setAttribute('fill', color);
          }
        });
        
        // Ensure viewBox is set correctly
        if (!svgElement.getAttribute('viewBox')) {
          svgElement.setAttribute('viewBox', '0 0 100 100');
        }
        
        return (
          <span 
            className="inline-block align-baseline"
            style={{ 
              width: `${size}px`,
              height: `${size}px`
            }}
            dangerouslySetInnerHTML={{ __html: svgElement.outerHTML }}
          />
        );
      }
    } catch (error) {
      console.error('Error parsing SVG:', error);
    }
    
    // Fallback: just render the SVG as-is with a wrapper
    return (
      <span 
        className="inline-block align-baseline mx-0.5"
        style={{ 
          width: '1em',
          height: '1em',
          fontSize: 'inherit'
        }}
        dangerouslySetInnerHTML={{ __html: suit.symbol.svg }}
      />
    );
  };

  const getCardDisplayName = (card) => {
    if (card.arcana === 'major') {
      const rankNum = parseInt(card.rank_slug);
      return `${getRomanNumeral(rankNum)} - ${card.name}`;
    } else {
      const rank = deck.ranks[card.rank_slug];
      return `${rank?.symbol || ''} - ${card.name}`;
    }
  };

  const CardDisplayNameWithIcon = ({ card, symbolColor = 'currentColor' }) => {
    if (card.arcana === 'major') {
      const rankNum = parseInt(card.rank_slug);
      return <>{getRomanNumeral(rankNum)} - {card.name}</>;
    } else {
      const rank = deck.ranks[card.rank_slug];
      return (
        <>
          {rank?.symbol || ''} <SuitSymbol suitSlug={card.suit_slug} color={symbolColor} /> - {card.name}
        </>
      );
    }
  };

  const handleCardClick = (card) => {
    setSelectedCard(card);
    setEditedCard(JSON.parse(JSON.stringify(card)));
    setIsEditing(false);
  };

  const handleSaveEdit = () => {
    if (!editedCard) return;
    
    const updatedDeck = { ...deck };
    updatedDeck.cards[editedCard.slug] = editedCard;
    setDeck(updatedDeck);
    setSelectedCard(editedCard);
    setIsEditing(false);
  };

  const handleEditChange = (path, value) => {
    const newCard = { ...editedCard };
    const keys = path.split('.');
    let current = newCard;
    
    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) current[keys[i]] = {};
      current = current[keys[i]];
    }
    
    current[keys[keys.length - 1]] = value;
    setEditedCard(newCard);
  };

  const fillPromptTemplate = (card) => {
    if (!card || !deck) return '';
    
    const suit = card.suit_slug ? deck.suits[card.suit_slug] : null;
    const rank = card.rank_slug ? deck.ranks[card.rank_slug] : null;
    
    // For major arcana, use the card's own number field directly
    const rankName = card.arcana === 'major' ? card.name : (rank?.name || card.number || '');
    const rankNumber = card.number || '';
    
    return promptTemplate
      .replace('{THEME_NAME}', deck.theme?.name || '')
      .replace('{THEME_DESCRIPTION}', deck.theme?.description || '')
      .replace('{CARD_NAME}', card.name || '')
      .replace('{ARCANA}', card.arcana || '')
      .replace('{CARD_DESCRIPTION}', card.description || '')
      .replace('{RANK_NAME}', rankName)
      .replace('{RANK_NUMBER}', rankNumber)
      .replace('{SUIT_NAME}', suit?.name || '')
      .replace('{UPRIGHT_MEANING}', card.meaning?.upright || '')
      .replace('{INVERTED_MEANING}', card.meaning?.inverted || '')
      .replace('{STYLE_GUIDANCE}', card.visuals?.instructions?.style_guidance || '')
      .replace('{CONTENT_GUIDANCE}', card.visuals?.instructions?.content_guidance || '')
      .replace('{DETAILED_DESCRIPTION}', card.visuals?.instructions?.detailed_description || '');
  };

  const generateVisualForCard = async (card) => {
    if (!managerRef.current) return;
    
    setGeneratingCards(prev => new Set(prev).add(card.slug));
    
    try {
      const code = await managerRef.current.generateCard(card, promptTemplate, fillPromptTemplate);
      
      // Update the card in the deck with the generated code
      const updatedDeck = { ...deck };
      if (!updatedDeck.cards[card.slug].visuals) {
        updatedDeck.cards[card.slug].visuals = {};
      }
      updatedDeck.cards[card.slug].visuals.code = code;
      setDeck(updatedDeck);
      
      // If this is the currently selected card, update it too
      if (selectedCard?.slug === card.slug) {
        setSelectedCard(updatedDeck.cards[card.slug]);
      }
      
      return code;
    } catch (error) {
      console.error("Error generating visual:", error);
      throw error;
    } finally {
      setGeneratingCards(prev => {
        const newSet = new Set(prev);
        newSet.delete(card.slug);
        return newSet;
      });
    }
  };

  const startBatchGeneration = () => {
    if (!managerRef.current || !deck) return;
    
    const allCards = Object.values(deck.cards);
    const cardsWithoutVisuals = allCards.filter(card => !card.visuals?.code);
    
    if (cardsWithoutVisuals.length === 0) return;
    
    // Compile all prompts upfront
    const jobs = cardsWithoutVisuals.map(function compileJob(card) {
      return {
        slug: card.slug,
        prompt: fillPromptTemplate(card)
      };
    });
    
    setBatchRunning(true);
    managerRef.current.start(jobs);
  };

  const stopBatchGeneration = () => {
    if (managerRef.current) {
      managerRef.current.stop();
    }
    setBatchRunning(false);
  };
  
  // Reading functions
  const drawCards = () => {
    if (!deck || !readingQuestion.trim()) return;
    
    const spreadDef = spreadDefinitions[selectedSpreadType];
    if (!spreadDef) return;
    
    // Clone and shuffle deck
    const allCards = Object.values(deck.cards);
    const shuffled = [...allCards].sort(() => Math.random() - 0.5);
    
    // Deal cards with random inversion
    const dealtCards = shuffled.slice(0, spreadDef.slots.length).map(card => ({
      ...card,
      inverted: Math.random() < 0.5
    }));
    
    setCurrentSpread({
      ...spreadDef,
      dealt_cards: dealtCards
    });
    setReadingResult(null);
  };
  
  const generateReading = async () => {
    if (!currentSpread || !readingQuestion) return;
    
    setGeneratingReading(true);
    
    try {
      // Build the prompt
      const cardsDescription = currentSpread.dealt_cards.map((card, idx) => {
        const slot = currentSpread.slots[idx];
        const orientation = card.inverted ? 'inverted' : 'upright';
        return `${slot.name} (${slot.meaning}): ${card.name} - ${orientation}
Upright meaning: ${card.meaning.upright}
Inverted meaning: ${card.meaning.inverted}`;
      }).join('\n\n');
      
      const prompt = readingPromptTemplate
        .replace('{{QUESTION}}', readingQuestion)
        .replace('{{SPREAD_NAME}}', currentSpread.name)
        .replace('{{SPREAD_PURPOSE}}', currentSpread.purpose)
        .replace('{{CARDS_DESCRIPTION}}', cardsDescription);

      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 2000,
          messages: [
            { role: "user", content: prompt }
          ]
        })
      });
      
      const data = await response.json();
      const reading = data.content[0].text;
      
      setReadingResult(reading);
    } catch (error) {
      console.error("Error generating reading:", error);
      setError("Failed to generate reading. Please try again.");
    } finally {
      setGeneratingReading(false);
    }
  };
  
  const removeVisual = (card) => {
    const updatedDeck = { ...deck };
    delete updatedDeck.cards[card.slug].visuals;
    setDeck(updatedDeck);
    
    // Update selected card if it's the same one
    if (selectedCard?.slug === card.slug) {
      setSelectedCard(updatedDeck.cards[card.slug]);
      setHideDetails(false); // Reset to show details since there's no visual
    }
  };

  const stats = deck ? {
    total: Object.keys(deck.cards).length,
    major: Object.values(deck.cards).filter(c => c.arcana === 'major').length,
    minor: Object.values(deck.cards).filter(c => c.arcana === 'minor').length
  } : null;

  const cardList = deck ? Object.entries(deck.cards).map(function buildCardList([slug, card]) {
    return { slug, ...card };
  }) : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white/10 backdrop-blur-md rounded-lg shadow-2xl">
          {!deck ? (
            <div className="p-8">
              <h1 className="text-4xl font-bold text-white mb-2">Tarot Deck Loader</h1>
              <p className="text-purple-200 mb-8">Upload a tarot deck JSON file to begin</p>

              <label className="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed border-purple-300 rounded-lg cursor-pointer hover:border-purple-400 transition-colors bg-white/5">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload className="w-12 h-12 text-purple-300 mb-4" />
                  <p className="text-lg text-white mb-2">Click to upload or drag and drop</p>
                  <p className="text-sm text-purple-300">Tarot deck JSON file</p>
                </div>
                <input
                  type="file"
                  className="hidden"
                  accept=".json"
                  onChange={handleFileUpload}
                />
              </label>

              {error && (
                <div className="mt-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <XCircle className="w-5 h-5 text-red-400" />
                    <h3 className="text-red-400 font-semibold">Validation Error</h3>
                  </div>
                  <p className="text-red-300 mb-2">{error}</p>
                  {validationDetails.length > 0 && (
                    <ul className="text-sm text-red-300 space-y-1 ml-4">
                      {validationDetails.map(function renderValidationDetail(detail, idx) {
                        return <li key={idx}>• {detail}</li>;
                      })}
                    </ul>
                  )}
                </div>
              )}
            </div>
          ) : (
            <>
              <div className="p-6 border-b border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h1 className="text-3xl font-bold text-white mb-1">{deck.name}</h1>
                    <p className="text-purple-200 text-sm">Version {deck.version}</p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={handleDownloadDeck}
                      className="px-4 py-2 bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 rounded-lg text-green-300 transition-colors flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download JSON
                    </button>
                    <button
                      onClick={() => {
                        setDeck(null);
                        setError(null);
                        setValidationDetails([]);
                        setCurrentView('summary');
                      }}
                      className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
                    >
                      Load Different Deck
                    </button>
                  </div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => setCurrentView('summary')}
                    className={`px-4 py-2 rounded-lg transition-colors ${
                      currentView === 'summary'
                        ? 'bg-white/20 text-white'
                        : 'bg-white/5 text-purple-300 hover:bg-white/10'
                    }`}
                  >
                    Summary
                  </button>
                  <button
                    onClick={() => setCurrentView('browser')}
                    className={`px-4 py-2 rounded-lg transition-colors ${
                      currentView === 'browser'
                        ? 'bg-white/20 text-white'
                        : 'bg-white/5 text-purple-300 hover:bg-white/10'
                    }`}
                  >
                    Card Browser
                  </button>
                  <button
                    onClick={() => setCurrentView('readings')}
                    className={`px-4 py-2 rounded-lg transition-colors ${
                      currentView === 'readings'
                        ? 'bg-white/20 text-white'
                        : 'bg-white/5 text-purple-300 hover:bg-white/10'
                    }`}
                  >
                    Readings
                  </button>
                  <button
                    onClick={() => setCurrentView('imagegen')}
                    className={`px-4 py-2 rounded-lg transition-colors ${
                      currentView === 'imagegen'
                        ? 'bg-white/20 text-white'
                        : 'bg-white/5 text-purple-300 hover:bg-white/10'
                    }`}
                  >
                    Image Generation
                  </button>
                </div>
              </div>

              <div className="p-6">
                {currentView === 'summary' && (
                  <div className="space-y-6">
                    {validationDetails.length > 0 && (
                      <div className="p-4 bg-yellow-500/20 border border-yellow-500/50 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                          <AlertCircle className="w-5 h-5 text-yellow-400" />
                          <h3 className="text-yellow-400 font-semibold">Warnings</h3>
                        </div>
                        <ul className="text-sm text-yellow-300 space-y-1 ml-4">
                          {validationDetails.map(function renderWarningDetail(detail, idx) {
                            return <li key={idx}>• {detail}</li>;
                          })}
                        </ul>
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Theme - left column */}
                      <div className="bg-white/5 rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-white mb-3">Theme</h3>
                        <p className="text-lg text-purple-200 mb-2">{deck.theme.name}</p>
                        <p className="text-sm text-purple-300">{deck.theme.description}</p>
                        {deck.theme.creator && (
                          <p className="text-sm text-purple-400 mt-2">Created by {deck.theme.creator}</p>
                        )}
                      </div>

                      {/* Stats - right column */}
                      <div className="bg-white/5 rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-white mb-3">Deck Composition</h3>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-purple-300">Total Cards</span>
                            <span className="text-white font-semibold">{stats.total}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-purple-300">Major Arcana</span>
                            <span className="text-white font-semibold">{stats.major}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-purple-300">Minor Arcana</span>
                            <span className="text-white font-semibold">{stats.minor}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white/5 rounded-lg p-6">
                      <h3 className="text-xl font-semibold text-white mb-4">Suits</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {Object.values(deck.suits).map(function renderSuit(suit) {
                          return (
                            <div key={suit.slug} className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                            <div className="flex items-center gap-4">
                              <div className="flex-shrink-0">
                                <SuitSymbol suitSlug={suit.slug} color="white" size={96} />
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="font-semibold text-white text-lg mb-1">{suit.name}</p>
                                <p className="text-sm text-purple-300">{suit.description}</p>
                              </div>
                            </div>
                          </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                )}
                
                {currentView === 'browser' && (
                  <div>
                    <h2 className="text-2xl font-bold text-white mb-4">All Cards ({cardList.length})</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[600px] overflow-y-auto pr-2">
                      {cardList.map(function renderBrowserCard(card) {
                        return (
                          <button
                            key={card.slug}
                            onClick={() => handleCardClick(card)}
                            className={`bg-white/5 hover:bg-white/10 rounded-lg p-4 text-left transition-colors ${
                              card.visuals?.code ? 'border-2 border-purple-500' : ''
                            }`}
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex-1">
                                <p className="text-white font-medium">
                                  <CardDisplayNameWithIcon card={card} symbolColor="white" />
                                </p>
                                <p className="text-purple-300 text-sm mt-1 capitalize">{card.arcana} Arcana</p>
                              </div>
                              {card.visuals?.code && (
                                <span className="text-purple-400 text-xs ml-2">✓ Visual</span>
                              )}
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                )}
                
                {currentView === 'imagegen' && (
                  <div className="space-y-6">
                    <div className="bg-white/5 rounded-lg p-6">
                      <h2 className="text-2xl font-bold text-white mb-4">Image Generation Prompt</h2>
                      <p className="text-purple-300 text-sm mb-4">
                        Edit the prompt template below and select a card to generate a filled prompt for p5.js image generation.
                      </p>
                      
                      <div className="mb-6">
                        <label className="block text-purple-300 text-sm font-semibold mb-2">
                          Prompt Template
                        </label>
                        <textarea
                          value={promptTemplate}
                          onChange={(e) => setPromptTemplate(e.target.value)}
                          className="w-full h-64 bg-purple-900/90 backdrop-blur-sm text-white rounded-lg p-4 font-mono text-sm"
                          placeholder="Enter your prompt template with {PLACEHOLDERS}..."
                        />
                      </div>
                    </div>

                    <div className="bg-white/5 rounded-lg p-6">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-semibold text-white">Generation Mode</h3>
                        <div className="flex gap-2">
                          <button
                            onClick={() => setBatchMode(false)}
                            className={`px-4 py-2 rounded-lg transition-colors ${
                              !batchMode
                                ? 'bg-purple-600 text-white'
                                : 'bg-white/10 text-purple-300 hover:bg-white/20'
                            }`}
                          >
                            Single Card
                          </button>
                          <button
                            onClick={() => setBatchMode(true)}
                            className={`px-4 py-2 rounded-lg transition-colors ${
                              batchMode
                                ? 'bg-purple-600 text-white'
                                : 'bg-white/10 text-purple-300 hover:bg-white/20'
                            }`}
                          >
                            Batch
                          </button>
                        </div>
                      </div>

                      {!batchMode ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-96 overflow-y-auto pr-2">
                          {cardList.map(function renderImageGenCard(card) {
                            return (
                              <button
                                key={card.slug}
                                onClick={() => setImageGenCard(card)}
                                className={`rounded-lg p-4 text-left transition-colors ${
                                  imageGenCard?.slug === card.slug
                                    ? 'bg-purple-600 text-white'
                                    : 'bg-white/5 hover:bg-white/10 text-white'
                                }`}
                              >
                                <p className="font-medium">
                                  <CardDisplayNameWithIcon card={card} symbolColor="white" />
                                </p>
                                <p className="text-purple-300 text-sm mt-1 capitalize">{card.arcana} Arcana</p>
                              </button>
                            );
                          })}
                        </div>
                      ) : (
                        <div className="space-y-4">
                          <div className="grid grid-cols-3 gap-4">
                            <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4 backdrop-blur-sm text-center">
                              <div className="text-3xl font-bold text-green-400">{batchProgress.completed}</div>
                              <div className="text-sm text-purple-300">Completed</div>
                            </div>
                            <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4 backdrop-blur-sm text-center">
                              <div className="text-3xl font-bold text-yellow-400">{batchProgress.inProgress.length}</div>
                              <div className="text-sm text-purple-300">In Progress</div>
                            </div>
                            <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4 backdrop-blur-sm text-center">
                              <div className="text-3xl font-bold text-purple-400">{batchProgress.remaining}</div>
                              <div className="text-sm text-purple-300">Remaining</div>
                            </div>
                          </div>

                          {batchProgress.inProgress.length > 0 && (
                            <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4 backdrop-blur-sm">
                              <h4 className="text-white font-semibold mb-2">Currently Generating:</h4>
                              <ul className="text-sm text-purple-200 space-y-1">
                                {batchProgress.inProgress.map(function renderInProgressCard(slug) {
                                  const card = deck?.cards?.[slug];
                                  if (!card) {
                                    console.warn(`Card ${slug} not found in deck.cards`, { 
                                      slug, 
                                      deckExists: !!deck,
                                      cardsExists: !!deck?.cards,
                                      availableSlugs: deck?.cards ? Object.keys(deck.cards) : []
                                    });
                                    return null;
                                  }
                                  const activeTime = telemetry?.activeGenerationTimes?.[slug];
                                  const elapsed = activeTime ? Math.floor(activeTime.elapsed / 1000) : 0;
                                  return (
                                    <li key={slug} className="flex items-center justify-between">
                                      <span>• <CardDisplayNameWithIcon card={card} symbolColor="white" /></span>
                                      <span className="text-purple-400 text-xs">{elapsed}s</span>
                                    </li>
                                  );
                                })}
                              </ul>
                            </div>
                          )}

                          {telemetry.totalGenerations > 0 && (
                            <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                              <h4 className="text-white font-semibold mb-3">Generation Telemetry</h4>
                              <div className="grid grid-cols-2 gap-3 text-sm">
                                {telemetry.batchElapsedTime > 0 && (
                                  <div className="col-span-2">
                                    <p className="text-purple-300">Batch Elapsed Time:</p>
                                    <p className="text-white font-semibold text-lg">{(telemetry.batchElapsedTime / 1000).toFixed(1)}s</p>
                                  </div>
                                )}
                                <div>
                                  <p className="text-purple-300">Average Time:</p>
                                  <p className="text-white font-semibold">{(telemetry.avgDuration / 1000).toFixed(1)}s</p>
                                </div>
                                <div>
                                  <p className="text-purple-300">Total Generated:</p>
                                  <p className="text-white font-semibold">{telemetry.totalGenerations}</p>
                                </div>
                                <div>
                                  <p className="text-purple-300">Min Time:</p>
                                  <p className="text-white font-semibold">{telemetry.minDuration ? (telemetry.minDuration / 1000).toFixed(1) : '-'}s</p>
                                </div>
                                <div>
                                  <p className="text-purple-300">Max Time:</p>
                                  <p className="text-white font-semibold">{telemetry.maxDuration ? (telemetry.maxDuration / 1000).toFixed(1) : '-'}s</p>
                                </div>
                                {telemetry.totalPromptTokens > 0 && (
                                  <>
                                    <div>
                                      <p className="text-purple-300">Input Tokens:</p>
                                      <p className="text-white font-semibold">{telemetry.totalPromptTokens.toLocaleString()}</p>
                                    </div>
                                    <div>
                                      <p className="text-purple-300">Output Tokens:</p>
                                      <p className="text-white font-semibold">{telemetry.totalCompletionTokens.toLocaleString()}</p>
                                    </div>
                                  </>
                                )}
                              </div>
                            </div>
                          )}

                          <div className="flex gap-2">
                            {!batchRunning ? (
                              <button
                                onClick={startBatchGeneration}
                                disabled={batchProgress.remaining === 0 && batchProgress.inProgress.length === 0}
                                className="flex-1 px-6 py-3 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg text-purple-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                Start Batch Generation
                              </button>
                            ) : (
                              <button
                                onClick={stopBatchGeneration}
                                className="flex-1 px-6 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-lg text-red-300 transition-colors"
                              >
                                Stop Batch Generation
                              </button>
                            )}
                          </div>

                          <p className="text-sm text-purple-400">
                            {batchRunning 
                              ? `Batch generation in progress. Up to 3 cards will be generated concurrently.`
                              : `Start batch generation to create visuals for all cards without them. Up to 3 cards will be generated at once.`
                            }
                          </p>
                        </div>
                      )}
                    </div>

                    {!batchMode && imageGenCard && (
                      <div className="bg-white/5 rounded-lg p-6">
                        <div className="flex items-center justify-between mb-4">
                          <h3 className="text-xl font-semibold text-white">
                            Generated Prompt for <CardDisplayNameWithIcon card={imageGenCard} symbolColor="white" />
                          </h3>
                          <div className="flex gap-2">
                            <button
                              onClick={() => generateVisualForCard(imageGenCard)}
                              disabled={generatingCards.has(imageGenCard.slug)}
                              className="px-4 py-2 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg text-purple-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              {generatingCards.has(imageGenCard.slug) ? 'Generating...' : 'Generate Visual'}
                            </button>
                            <button
                              onClick={() => {
                                navigator.clipboard.writeText(fillPromptTemplate(imageGenCard));
                              }}
                              className="px-4 py-2 bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 rounded-lg text-green-300 transition-colors"
                            >
                              Copy to Clipboard
                            </button>
                          </div>
                        </div>
                        <pre className="bg-white/10 rounded-lg p-4 text-sm text-purple-200 overflow-x-auto whitespace-pre-wrap">
                          {fillPromptTemplate(imageGenCard)}
                        </pre>
                      </div>
                    )}
                  </div>
                )}
                
                {currentView === 'readings' && (
                  <div className="space-y-6">
                    <div className="bg-white/5 rounded-lg p-6">
                      <div className="flex items-center justify-between mb-4">
                        <h2 className="text-2xl font-bold text-white">Tarot Reading</h2>
                        <button
                          onClick={() => setShowReadingSettings(true)}
                          className="px-4 py-2 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg text-purple-300 transition-colors"
                        >
                          Settings
                        </button>
                      </div>
                      
                      {/* Question input */}
                      <div className="space-y-4 mb-6">
                        <div>
                          <label className="block text-purple-300 text-sm mb-2">Your Question</label>
                          <textarea
                            value={readingQuestion}
                            onChange={(e) => setReadingQuestion(e.target.value)}
                            placeholder="What question would you like guidance on?"
                            className="w-full bg-purple-900/50 text-white rounded-lg p-3 min-h-[100px] placeholder-purple-400"
                          />
                        </div>
                        
                        {/* Current spread info */}
                        <div className="bg-purple-900/30 rounded-lg p-3 text-sm">
                          <span className="text-purple-300">Selected spread: </span>
                          <span className="text-white font-semibold">{spreadDefinitions[selectedSpreadType].name}</span>
                          <span className="text-purple-400"> ({spreadDefinitions[selectedSpreadType].slots.length} cards)</span>
                        </div>
                        
                        {/* Draw button */}
                        <button
                          onClick={drawCards}
                          disabled={!readingQuestion.trim()}
                          className="w-full px-6 py-3 bg-purple-500 hover:bg-purple-600 rounded-lg text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Draw {spreadDefinitions[selectedSpreadType].slots.length} Card{spreadDefinitions[selectedSpreadType].slots.length > 1 ? 's' : ''}
                        </button>
                      </div>
                      
                      {/* Display spread */}
                      {currentSpread && (
                        <div className="space-y-6 border-t border-white/10 pt-6">
                          <div>
                            <h3 className="text-xl font-semibold text-white mb-2">{currentSpread.name}</h3>
                            <p className="text-sm text-purple-300 mb-4">{currentSpread.instructions}</p>
                          </div>
                          
                          {/* Cards display */}
                          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {currentSpread.dealt_cards.map((card, idx) => {
                              const slot = currentSpread.slots[idx];
                              return (
                                <div key={idx} className="bg-purple-900/50 rounded-lg p-4 max-w-[448px] mx-auto w-full">
                                  <div className="text-xs text-purple-400 mb-2">{slot.name}</div>
                                  
                                  {/* Card visual if available */}
                                  {card.visuals?.code && (
                                    <div 
                                      className="mb-3 bg-black/20 rounded-lg overflow-hidden mx-auto"
                                      style={{ 
                                        width: '400px',
                                        height: '600px',
                                        maxWidth: '100%',
                                        transform: card.inverted ? 'rotate(180deg)' : 'none'
                                      }}
                                    >
                                      <P5Sketch code={card.visuals.code} />
                                    </div>
                                  )}
                                  
                                  <div className="flex items-center gap-2 mb-2">
                                    <span className="text-white">
                                      <CardDisplayNameWithIcon card={card} symbolColor="white" />
                                    </span>
                                    {card.inverted && (
                                      <span className="text-xs text-yellow-400">(Inverted)</span>
                                    )}
                                  </div>
                                  <div className="text-xs text-purple-300 italic mb-2">{slot.meaning}</div>
                                  <div className="text-xs text-purple-200">
                                    {card.meaning ? (card.inverted ? card.meaning.inverted : card.meaning.upright) : 'No meaning available'}
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                          
                          {/* Generate reading button */}
                          {!readingResult && (
                            <button
                              onClick={generateReading}
                              disabled={generatingReading}
                              className="w-full px-6 py-3 bg-green-500 hover:bg-green-600 rounded-lg text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              {generatingReading ? 'Generating Reading...' : 'Generate Reading'}
                            </button>
                          )}
                          
                          {/* Reading result */}
                          {readingResult && (
                            <div className="bg-white/5 rounded-lg p-6">
                              <h3 className="text-xl font-semibold text-white mb-4">Your Reading</h3>
                              <div className="text-purple-200 whitespace-pre-wrap leading-relaxed">
                                {readingResult}
                              </div>
                              <button
                                onClick={() => {
                                  setCurrentSpread(null);
                                  setReadingResult(null);
                                }}
                                className="mt-6 px-6 py-2 bg-purple-500 hover:bg-purple-600 rounded-lg text-white transition-colors"
                              >
                                New Reading
                              </button>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
      
      {/* Reading Settings Modal */}
      {showReadingSettings && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setShowReadingSettings(false)}>
          <div className="bg-purple-900 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Reading Settings</h2>
              <button
                onClick={() => setShowReadingSettings(false)}
                className="p-2 hover:bg-white/10 rounded-lg transition-colors"
              >
                <X className="w-6 h-6 text-white" />
              </button>
            </div>
            
            <div className="space-y-6">
              {/* Spread selection */}
              <div>
                <label className="block text-purple-300 text-sm mb-3 font-semibold">Choose a Spread</label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {Object.entries(spreadDefinitions).map(([key, spread]) => (
                    <button
                      key={key}
                      onClick={() => setSelectedSpreadType(key)}
                      className={`p-4 rounded-lg text-left transition-colors ${
                        selectedSpreadType === key
                          ? 'bg-purple-600 border-2 border-purple-400'
                          : 'bg-white/5 hover:bg-white/10 border-2 border-transparent'
                      }`}
                    >
                      <div className="font-semibold text-white mb-1">{spread.name}</div>
                      <div className="text-sm text-purple-300">{spread.slots.length} card{spread.slots.length > 1 ? 's' : ''}</div>
                      <div className="text-xs text-purple-400 mt-2">{spread.purpose}</div>
                    </button>
                  ))}
                </div>
              </div>
              
              {/* Prompt template editor */}
              <div>
                <label className="block text-purple-300 text-sm mb-2 font-semibold">
                  Reading Prompt Template
                </label>
                <p className="text-xs text-purple-400 mb-2">
                  Available placeholders: QUESTION, SPREAD_NAME, SPREAD_PURPOSE, CARDS_DESCRIPTION
                </p>
                <textarea
                  value={readingPromptTemplate}
                  onChange={(e) => setReadingPromptTemplate(e.target.value)}
                  className="w-full bg-purple-900/50 text-white rounded-lg p-3 min-h-[300px] text-sm font-mono"
                />
              </div>
              
              <button
                onClick={() => setShowReadingSettings(false)}
                className="w-full px-6 py-3 bg-purple-500 hover:bg-purple-600 rounded-lg text-white font-semibold transition-colors"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
      
      {selectedCard && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => { setSelectedCard(null); setHideDetails(false); }}>
          <div className="relative rounded-lg max-w-4xl w-full flex flex-col bg-purple-900" style={{ height: '95vh' }} onClick={e => e.stopPropagation()}>
            {/* Header - always visible */}
            <div className="flex-shrink-0 bg-purple-900/95 backdrop-blur-sm p-6 border-b border-purple-700 flex items-center justify-between z-10 rounded-t-lg">
              <h2 className="text-2xl font-bold text-white">
                <CardDisplayNameWithIcon card={isEditing ? editedCard : selectedCard} symbolColor="white" />
              </h2>
              <div className="flex gap-2">
                {selectedCard.visuals?.code && (
                  <button
                    onClick={() => setHideDetails(!hideDetails)}
                    className={`p-2 rounded-lg text-white transition-colors ${
                      hideDetails 
                        ? 'bg-purple-600 hover:bg-purple-700' 
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                    title={hideDetails ? "Show details" : "Show visual only"}
                  >
                    <Eye className="w-5 h-5" />
                  </button>
                )}
                {!isEditing ? (
                  <button
                    onClick={() => setIsEditing(true)}
                    disabled={hideDetails}
                    className={`p-2 rounded-lg text-white transition-colors ${
                      hideDetails 
                        ? 'bg-white/5 text-white/30 cursor-not-allowed' 
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                    title="Edit card"
                  >
                    <Edit2 className="w-5 h-5" />
                  </button>
                ) : (
                  <>
                    <button
                      onClick={handleSaveEdit}
                      className="px-4 py-2 bg-green-500 hover:bg-green-600 rounded-lg text-white transition-colors flex items-center gap-2"
                    >
                      <Save className="w-4 h-4" />
                      Save
                    </button>
                    <button
                      onClick={() => {
                        setIsEditing(false);
                        setEditedCard(JSON.parse(JSON.stringify(selectedCard)));
                      }}
                      className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </>
                )}
                <button
                  onClick={() => { setSelectedCard(null); setHideDetails(false); }}
                  className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
            
            {/* Content area */}
            {hideDetails && selectedCard.visuals?.code ? (
              /* Visual-only view - large canvas */
              <div className="relative bg-black flex-col flex items-center justify-center overflow-hidden rounded-b-lg flex-1 min-h-0 p-6">
                {/* Discard button */}
                <div className="mb-4">
                  {!confirmRemoveVisual ? (
                    <button
                      onClick={() => setConfirmRemoveVisual(selectedCard.slug)}
                      className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-lg text-red-300 transition-colors"
                    >
                      Discard Visual
                    </button>
                  ) : confirmRemoveVisual === selectedCard.slug ? (
                    <div className="flex gap-2">
                      <button
                        onClick={() => {
                          removeVisual(selectedCard);
                          setConfirmRemoveVisual(null);
                        }}
                        className="px-4 py-2 bg-red-500 hover:bg-red-600 rounded-lg text-white font-semibold transition-colors"
                      >
                        Confirm Remove
                      </button>
                      <button
                        onClick={() => setConfirmRemoveVisual(null)}
                        className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : null}
                </div>
                
                <div style={{ 
                  width: '100%', 
                  maxWidth: '600px',
                  aspectRatio: '2/3',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <div style={{ 
                    transform: 'scale(1.5)',
                    transformOrigin: 'center'
                  }}>
                    <P5Sketch code={selectedCard.visuals.code} />
                  </div>
                </div>
              </div>
            ) : (
              /* Details view with visual in background */
              <div className="relative flex-1 overflow-hidden rounded-b-lg min-h-0">
                {/* P5 Sketch background */}
                {selectedCard.visuals?.code && (
                  <div className="absolute inset-0 flex items-center justify-center overflow-hidden pointer-events-none opacity-30 p-6">
                    <div style={{ 
                      width: '100%', 
                      maxWidth: '600px',
                      aspectRatio: '2/3',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <div style={{ 
                        transform: 'scale(1.5)',
                        transformOrigin: 'center'
                      }}>
                        <P5Sketch code={selectedCard.visuals.code} />
                      </div>
                    </div>
                  </div>
                )}
                
                {/* Details content */}
                <div className="relative bg-gradient-to-br from-purple-900/50 to-indigo-900/50 backdrop-blur-sm overflow-y-auto h-full">
                  <div className="p-6 space-y-6">
              {(() => {
                const card = isEditing ? editedCard : selectedCard;
                const suit = card.suit_slug ? deck.suits[card.suit_slug] : null;
                
                return (
                  <>
                    {card.arcana === 'major' ? (
                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                          <p className="text-purple-300 text-sm mb-1">Arcana</p>
                          <p className="text-white font-semibold capitalize">{card.arcana}</p>
                        </div>
                        <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                          <p className="text-purple-300 text-sm mb-1">Rank</p>
                          <p className="text-white font-semibold">{card.number}</p>
                        </div>
                      </div>
                    ) : (
                      <div className="grid grid-cols-3 gap-4">
                        <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                          <p className="text-purple-300 text-sm mb-1">Arcana</p>
                          <p className="text-white font-semibold capitalize">{card.arcana}</p>
                        </div>
                        <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                          <p className="text-purple-300 text-sm mb-1">Rank</p>
                          <p className="text-white font-semibold">{(() => {
                            const rank = deck.ranks[card.rank_slug];
                            return rank ? `${rank.numeric_value}${rank.name ? ' - ' + rank.name : ''}` : card.number;
                          })()}</p>
                        </div>
                        <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                          <p className="text-purple-300 text-sm mb-1">Suit</p>
                          <p className="text-white font-semibold text-xl">
                            <SuitSymbol suitSlug={card.suit_slug} color="white" /> {suit?.name}
                          </p>
                        </div>
                      </div>
                    )}

                    <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                      <p className="text-purple-300 text-sm mb-2">Description</p>
                      {isEditing ? (
                        <textarea
                          value={card.description}
                          onChange={(e) => handleEditChange('description', e.target.value)}
                          className="w-full bg-purple-900/90 backdrop-blur-sm text-white rounded p-2 min-h-[100px]"
                        />
                      ) : (
                        <p className="text-white">{card.description}</p>
                      )}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                        <p className="text-purple-300 text-sm mb-2">Upright Meaning</p>
                        {isEditing ? (
                          <textarea
                            value={card.meaning.upright}
                            onChange={(e) => handleEditChange('meaning.upright', e.target.value)}
                            className="w-full bg-purple-900/90 backdrop-blur-sm text-white rounded p-2 min-h-[100px]"
                          />
                        ) : (
                          <p className="text-white text-sm">{card.meaning.upright}</p>
                        )}
                      </div>
                      <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4">
                        <p className="text-purple-300 text-sm mb-2">Inverted Meaning</p>
                        {isEditing ? (
                          <textarea
                            value={card.meaning.inverted}
                            onChange={(e) => handleEditChange('meaning.inverted', e.target.value)}
                            className="w-full bg-purple-900/90 backdrop-blur-sm text-white rounded p-2 min-h-[100px]"
                          />
                        ) : (
                          <p className="text-white text-sm">{card.meaning.inverted}</p>
                        )}
                      </div>
                    </div>

                    {card.visuals?.instructions && (
                      <div className="bg-purple-900/90 backdrop-blur-sm rounded-lg p-4 space-y-4">
                        <p className="text-purple-300 text-sm font-semibold">Visual Instructions</p>
                        
                        <div>
                          <p className="text-purple-300 text-xs mb-1">Style Guidance</p>
                          {isEditing ? (
                            <textarea
                              value={card.visuals.instructions.style_guidance}
                              onChange={(e) => handleEditChange('visuals.instructions.style_guidance', e.target.value)}
                              className="w-full bg-purple-900/90 backdrop-blur-sm text-white rounded p-2 min-h-[60px] text-sm"
                            />
                          ) : (
                            <p className="text-white text-sm">{card.visuals.instructions.style_guidance}</p>
                          )}
                        </div>
                        
                        <div>
                          <p className="text-purple-300 text-xs mb-1">Content Guidance</p>
                          {isEditing ? (
                            <textarea
                              value={card.visuals.instructions.content_guidance}
                              onChange={(e) => handleEditChange('visuals.instructions.content_guidance', e.target.value)}
                              className="w-full bg-purple-900/90 backdrop-blur-sm text-white rounded p-2 min-h-[60px] text-sm"
                            />
                          ) : (
                            <p className="text-white text-sm">{card.visuals.instructions.content_guidance}</p>
                          )}
                        </div>
                        
                        <div>
                          <p className="text-purple-300 text-xs mb-1">Detailed Description</p>
                          {isEditing ? (
                            <textarea
                              value={card.visuals.instructions.detailed_description}
                              onChange={(e) => handleEditChange('visuals.instructions.detailed_description', e.target.value)}
                              className="w-full bg-purple-900/90 backdrop-blur-sm text-white rounded p-2 min-h-[100px] text-sm"
                            />
                          ) : (
                            <p className="text-white text-sm">{card.visuals.instructions.detailed_description}</p>
                          )}
                        </div>
                      </div>
                    )}
                  </>
                );
              })()}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}