import { useState, useEffect } from 'react'
import './App.css'
import Introduction from './components/Introduction'
import CardBrowser from './components/CardBrowser'

function App() {
  const [deckData, setDeckData] = useState(null)
  const [currentView, setCurrentView] = useState('intro')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/sound-of-music-tarot.json')
      .then(res => res.json())
      .then(data => {
        setDeckData(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load deck:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading the Sound of Music Tarot...</p>
      </div>
    )
  }

  if (!deckData) {
    return (
      <div className="error">
        <h1>Error loading deck data</h1>
        <p>Please make sure sound-of-music-tarot.json is in the public folder.</p>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏔️ The Sound of Music Tarot 🎵</h1>
        <nav>
          <button
            className={currentView === 'intro' ? 'active' : ''}
            onClick={() => setCurrentView('intro')}
          >
            Introduction
          </button>
          <button
            className={currentView === 'browse' ? 'active' : ''}
            onClick={() => setCurrentView('browse')}
          >
            Browse Cards
          </button>
        </nav>
      </header>

      <main className="app-main">
        {currentView === 'intro' ? (
          <Introduction deckData={deckData} onStartBrowsing={() => setCurrentView('browse')} />
        ) : (
          <CardBrowser deckData={deckData} />
        )}
      </main>

      <footer className="app-footer">
        <p>A tarot deck exploring authenticity vs instrumentality through The Sound of Music</p>
        <p className="credit">Created by Myk & Claude • {new Date().getFullYear()}</p>
      </footer>
    </div>
  )
}

export default App
