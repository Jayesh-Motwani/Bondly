import React from 'react'

/**
 * Header Component
 * 
 * Top navigation bar with app branding and tagline.
 * Designed to feel calm and welcoming, not corporate.
 * 
 * @param {string} title - App name (default: "LoveGuru")
 * @param {string} tagline - Subtitle text (default: "Talk it out. No judgment.")
 */
const Header = ({ title = "LoveGuru", tagline = "Talk it out. No judgment." }) => {
  return (
    <header className="w-full py-5 px-6 bg-white/80 backdrop-blur-md border-b border-neutral-100 sticky top-0 z-10">
      <div className="max-w-3xl mx-auto flex items-center gap-4">
        {/* Logo/Icon - Heart emoji for warmth and approachability */}
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-xl shadow-md">
          💜
        </div>
        
        {/* Title and tagline container */}
        <div className="flex-1">
          {/* App name - friendly, not intimidating */}
          <h1 className="text-xl font-semibold text-neutral-800 tracking-tight">
            {title}
          </h1>
          
          {/* Tagline - reinforces emotional safety */}
          <p className="text-xs text-neutral-500 font-medium">
            {tagline}
          </p>
        </div>
        
        {/* Optional: Could add settings/info button here later */}
        <div className="hidden sm:block">
          <span className="text-xs text-neutral-400 bg-neutral-100 px-3 py-1.5 rounded-full">
            AI Advisor
          </span>
        </div>
      </div>
    </header>
  )
}

export default Header
