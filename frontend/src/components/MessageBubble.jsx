import React from 'react'

/**
 * TypingIndicator Component
 * 
 * Shows three animated dots while AI is "thinking".
 * Provides visual feedback that a response is coming.
 */
const TypingIndicator = () => (
  <div className="flex items-center gap-1.5 px-5 py-4">
    <div className="w-2 h-2 rounded-full bg-neutral-400 typing-dot"></div>
    <div className="w-2 h-2 rounded-full bg-neutral-400 typing-dot"></div>
    <div className="w-2 h-2 rounded-full bg-neutral-400 typing-dot"></div>
  </div>
)

/**
 * MessageBubble Component
 * 
 * Renders individual chat messages with different styles
 * for user vs AI messages. Uses Tailwind classes for
 * emotionally-appropriate styling.
 * 
 * @param {Object} props
 * @param {'user' | 'assistant'} props.role - Message sender
 * @param {string} props.content - Message text
 * @param {boolean} props.isTyping - Show typing indicator instead
 */
const MessageBubble = ({ role, content, isTyping = false }) => {
  // User messages: right-aligned, purple accent
  // AI messages: left-aligned, neutral/white background
  const isUser = role === 'user'
  
  if (isTyping) {
    return (
      <div className="flex justify-start animate-slide-up">
        <div className="message-ai">
          <TypingIndicator />
        </div>
      </div>
    )
  }
  
  return (
    <div 
      className={`flex animate-slide-up ${
        isUser ? 'justify-end' : 'justify-start'
      }`}
    >
      <div className={isUser ? 'message-user' : 'message-ai'}>
        {/* 
          Message content with proper whitespace handling.
          AI responses can be long, so we use whitespace-pre-wrap
          to preserve paragraph breaks for readability.
        */}
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {content}
        </p>
        
        {/* Optional: Add timestamp later if needed */}
        {/* <span className="text-xs opacity-60 mt-2 block">
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span> */}
      </div>
    </div>
  )
}

export default MessageBubble
