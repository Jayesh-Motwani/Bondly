import React from 'react'
import Header from './components/Header'
import ChatWindow from './components/ChatWindow'

/**
 * Main App Component
 * 
 * Root component that composes the layout:
 * - Header at top
 * - ChatWindow fills remaining space
 * 
 * The layout is designed to feel:
 * - Clean and uncluttered (reduces anxiety)
 * - Warm and inviting (encourages openness)
 * - Focused on the conversation (no distractions)
 */
const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-warm-50 via-primary-50 to-warm-100">
      {/* 
        Header - sticky at top with app branding 
        Provides context and reassurance about the app's purpose
      */}
      <Header 
        title="LoveGuru" 
        tagline="Talk it out. No judgment." 
      />
      
      {/* 
        Main chat interface
        Handles all conversation logic and UI
      */}
      <main>
        <ChatWindow />
      </main>
    </div>
  )
}

export default App
