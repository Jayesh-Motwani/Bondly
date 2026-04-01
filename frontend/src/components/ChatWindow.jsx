import React, { useState, useRef, useEffect } from 'react'
import MessageBubble from './MessageBubble'
import InputBox from './InputBox'

/**
 * ChatWindow Component
 * 
 * Main chat interface that manages:
 * - Message state and history
 * - API communication with backend
 * - Loading states
 * - Auto-scrolling to latest message
 * - Empty state with example prompts
 * 
 * API: POST /query
 * Request: { query: string }
 * Response: { answer: string, sources: array, category: string|null }
 */
const ChatWindow = () => {
  // Message history: array of { role: 'user' | 'assistant', content: string }
  const [messages, setMessages] = useState([])
  
  // Loading state - disables input and shows typing indicator
  const [isLoading, setIsLoading] = useState(false)
  
  // Ref for auto-scrolling to bottom of chat
  const messagesEndRef = useRef(null)
  
  // Example prompts for empty state - helps users get started
  const examplePrompts = [
    "I feel confused about my relationship...",
    "She stopped texting me, what should I do?",
    "How do I know if they're the one?",
    "We've been dating for months but haven't defined things...",
    "My partner and I keep fighting about the same thing...",
  ]
  
  /**
   * Scroll to bottom of message list
   * Called whenever messages change
   */
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  
  useEffect(() => {
    scrollToBottom()
  }, [messages])
  
  /**
   * Send message to backend API
   * - Adds user message to state
   * - Shows loading indicator
   * - Calls POST /query
   * - Adds AI response to state
   * 
   * @param {string} query - User's message
   */
  const handleSendMessage = async (query) => {
    // Add user message to history
    setMessages(prev => [...prev, { role: 'user', content: query }])
    setIsLoading(true)
    
    try {
      // Call backend API
      const response = await fetch('/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Add AI response to history
      // The backend returns { answer, sources, category }
      // We display the 'answer' field
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer || "I'm here to help. Could you tell me more about what's on your mind?" 
      }])
      
    } catch (error) {
      console.error('Error fetching response:', error)
      
      // Show error message to user
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "I'm having trouble connecting right now. Please check your connection and try again." 
      }])
    } finally {
      setIsLoading(false)
    }
  }
  
  /**
   * Handle clicking an example prompt
   * Sends it as a message
   */
  const handleExampleClick = (prompt) => {
    handleSendMessage(prompt)
  }
  
  return (
    <div className="chat-container h-screen pb-24">
      {/* Header spacing */}
      <div className="h-20 flex-shrink-0"></div>
      
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto scrollbar-thin px-4 py-6">
        <div className="space-y-6">
          {/* Empty state - shown before first message */}
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 animate-fade-in">
              {/* Friendly welcome icon */}
              <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-4xl mb-6 shadow-lg">
                💜
              </div>
              
              {/* Welcome text */}
              <h2 className="text-2xl font-semibold text-neutral-800 mb-2">
                What's on your mind?
              </h2>
              <p className="text-neutral-500 text-center max-w-md mb-8">
                I'm here to listen and help you navigate your relationships. 
                No judgment, just support.
              </p>
              
              {/* Example prompts - clickable chips */}
              <div className="flex flex-wrap justify-center gap-3 max-w-2xl">
                {examplePrompts.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => handleExampleClick(prompt)}
                    className="prompt-chip"
                    disabled={isLoading}
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          {/* Message list */}
          {messages.map((message, index) => (
            <MessageBubble
              key={index}
              role={message.role}
              content={message.content}
            />
          ))}
          
          {/* Typing indicator - shown while waiting for API response */}
          {isLoading && messages.length > 0 && (
            <MessageBubble role="assistant" isTyping={true} />
          )}
          
          {/* Invisible element for auto-scroll target */}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input area - fixed at bottom */}
      <div className="fixed bottom-0 left-0 right-0">
        <InputBox 
          onSend={handleSendMessage} 
          isLoading={isLoading}
          placeholderSuggestions={examplePrompts}
        />
      </div>
    </div>
  )
}

export default ChatWindow
