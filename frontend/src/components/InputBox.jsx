import React, { useState } from 'react'

/**
 * InputBox Component
 * 
 * Fixed bottom input area with send button.
 * Features:
 * - Rounded, modern design
 * - Focus glow effect
 * - Disabled state during loading
 * - Send icon (SVG)
 * 
 * @param {Function} onSend - Callback when message is sent
 * @param {boolean} isLoading - Disable input while loading
 * @param {string[]} placeholderSuggestions - Optional placeholder texts to cycle through
 */
const InputBox = ({ onSend, isLoading = false, placeholderSuggestions = [] }) => {
  const [message, setMessage] = useState('')
  
  // Cycle through placeholder suggestions for inspiration
  const placeholder = placeholderSuggestions.length > 0
    ? placeholderSuggestions[Math.floor(Date.now() / 5000) % placeholderSuggestions.length]
    : "What's on your mind?"
  
  /**
   * Handle sending a message
   * - Trim whitespace
   * - Call parent callback
   * - Clear input
   */
  const handleSend = () => {
    const trimmedMessage = message.trim()
    if (trimmedMessage && !isLoading) {
      onSend(trimmedMessage)
      setMessage('')
    }
  }
  
  /**
   * Handle Enter key to send
   * - Shift+Enter for new line
   * - Enter alone to send
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }
  
  return (
    <div className="w-full p-4 bg-white/80 backdrop-blur-md border-t border-neutral-100">
      <div className="max-w-3xl mx-auto">
        {/* Input container with flex layout */}
        <div className="flex items-end gap-3">
          {/* Text input field */}
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={isLoading}
            className="chat-input flex-1 resize-none"
            rows={1}
            aria-label="Type your message"
          />
          
          {/* Send button with SVG icon */}
          <button
            onClick={handleSend}
            disabled={isLoading || !message.trim()}
            className="send-button flex-shrink-0"
            aria-label="Send message"
          >
            {/* Paper plane icon - universally recognized for "send" */}
            <svg 
              className="w-5 h-5" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" 
              />
            </svg>
          </button>
        </div>
        
        {/* Helper text - subtle hint about privacy/usage */}
        <p className="text-xs text-neutral-400 text-center mt-3">
          Your conversations are private and confidential
        </p>
      </div>
    </div>
  )
}

export default InputBox
