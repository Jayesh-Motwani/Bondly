# LoveGuru Frontend 💜

A modern, emotionally-safe chat UI for AI relationship advice.

## Features

- 🎨 **Clean, warm design** - Soft colors and rounded corners for emotional safety
- 💬 **Real-time chat** - Smooth messaging experience with typing indicators
- 📱 **Responsive** - Works on desktop and mobile
- ⚡ **Fast** - Built with Vite for instant hot module replacement
- 🎯 **Accessible** - ARIA labels and keyboard navigation

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Fetch API** - Backend communication

## Getting Started

### Prerequisites

- Node.js 18+ 
- Python backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open at `http://localhost:3000`

### Building for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx        # Top navigation bar
│   │   ├── MessageBubble.jsx # Chat message component
│   │   ├── InputBox.jsx      # Message input area
│   │   └── ChatWindow.jsx    # Main chat interface
│   ├── App.jsx               # Root component
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

## API Integration

The frontend communicates with the Python backend via:

**Endpoint:** `POST /query`

**Request:**
```json
{
  "query": "I feel confused about my relationship..."
}
```

**Response:**
```json
{
  "answer": "I understand this is difficult...",
  "sources": [],
  "category": null
}
```

## Design Principles

1. **Emotional Safety** - Warm colors, non-judgmental language
2. **Clarity** - Easy to read typography, clear visual hierarchy
3. **Simplicity** - Minimal distractions, focus on conversation
4. **Trust** - Privacy notice, professional appearance

## Customization

### Colors

Edit `tailwind.config.js` to change the color palette:

```js
colors: {
  primary: { /* ... */ },  // Main accent color
  warm: { /* ... */ },     // Background tones
  neutral: { /* ... */ },  // Text colors
}
```

### Example Prompts

Edit the `examplePrompts` array in `ChatWindow.jsx`:

```js
const examplePrompts = [
  "Your prompt here...",
  // Add more prompts
]
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |

## License

MIT
