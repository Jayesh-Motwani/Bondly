# Bondly - AI Relationship Advice Assistant

A modern, full-stack AI-powered relationship advice chatbot that provides thoughtful, empathetic guidance for modern dating challenges, situationships, and relationship concerns.

![Status](https://img.shields.io/badge/status-ready-success)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![React](https://img.shields.io/badge/react-18-blue)

---

## Features

- **AI-Powered Advice**: Uses Google Gemini (free tier) for intelligent, context-aware relationship guidance
- **RAG Pipeline**: Retrieves relevant advice from curated relationship content across the web
- **Situationship Detection**: Automatically identifies situationship vs. relationship queries
- **Modern UI**: Clean, emotionally-safe React frontend with Tailwind CSS
- **100% Free Stack**: No paid APIs required - uses free tiers throughout

---

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Google API Key (free - get it [here](https://aistudio.google.com/app/apikey))

### 1. Clone the Repository

```bash
git clone https://github.com/Jayesh-Motwani/Bondly
cd Bondly
```

### 2. Set Up Backend

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Google Gemini API Key (FREE - get from https://aistudio.google.com/app/apikey)
GOOGLE_API_KEY=your_api_key_here

# User agent for web scraping
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

### 5. Run the Application

**Terminal 1 - Backend (FastAPI)**
```bash
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend (Vite + React)**
```bash
cd frontend
npm run dev
```

### 6. Open the App

Navigate to **http://localhost:3000** in your browser.

---

## Project Structure

```
Bondly/
├── app.py                      # FastAPI backend server
├── love_guru.py                # Main RAG pipeline and query logic
├── extraction_pipeline.py      # Web scraping and content extraction
├── prompt_templates.py         # LLM prompt templates
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── chroma_db/                  # Vector database (auto-generated)
│
└── frontend/                   # React frontend
    ├── src/
    │   ├── components/
    │   │   ├── Header.jsx         # App header with branding
    │   │   ├── MessageBubble.jsx  # Chat message component
    │   │   ├── InputBox.jsx       # Message input area
    │   │   └── ChatWindow.jsx     # Main chat interface
    │   ├── App.jsx             # Root component
    │   ├── main.jsx            # Entry point
    │   └── index.css           # Global styles + Tailwind
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── README.md
```

---

## Architecture

### Backend Pipeline

```
User Query → Intent Classification (Situationship or Relationship) → Vector Search → LLM Response
                                                                          ↓
                                                                    ChromaDB (Embeddings)
```

1. **Intent Classification**: Categorizes query as situationship or relationship advice
2. **Vector Search**: Retrieves relevant content from ChromaDB using semantic search
3. **LLM Generation**: Google Gemini generates empathetic, actionable advice

### Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| **LLM** | Google Gemini 3.0 Flash | Best free tier (15 RPM, 1M TPM) |
| **Embeddings** | Sentence Transformers | Local, free, multilingual |
| **Vector DB** | ChromaDB | Lightweight, persistent storage |
| **Backend** | FastAPI | Fast, async, easy to deploy |
| **Frontend** | React + Vite | Modern, fast DX |
| **Styling** | Tailwind CSS | Rapid UI development |
| **Web Scraping** | LangChain WebBaseLoader | Built-in content extraction |

---

## API Reference

### POST /query

Send a relationship question and get AI-powered advice.

**Request:**
```json
{
  "query": "I've been dating someone for 3 months but we haven't defined the relationship..."
}
```

**Response:**
```json
{
  "answer": "Understanding Your Situation...\n\nIt sounds like you're experiencing uncertainty...",
  "sources": [],
  "category": null
}
```

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "running"
}
```

---

## Configuration

### Changing the LLM

Edit `love_guru.py`:

```python
LLM_MODEL = "gemini-3.0-flash-exp"  # or other Gemini models
```

### Customizing Prompts

Edit `prompt_templates.py` to modify how the AI responds.

### Adding Data Sources

Edit `extraction_pipeline.py` to add more URLs:

```python
RELATIONSHIP_ADVICE_URLS = [
    "https://example.com/relationship-advice",
    # Add more sources
]
```

---

## Deployment

### Deploy Backend (Railway / Render / Fly.io)

1. Create a new Python project
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python -m uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `GOOGLE_API_KEY`

### Deploy Frontend (Vercel / Netlify)

1. Connect your GitHub repository
2. Set build command: `cd frontend && npm install && npm run build`
3. Set output directory: `frontend/dist`
4. Update API URL in `ChatWindow.jsx` to point to your deployed backend

### Environment Variables for Production

```env
GOOGLE_API_KEY=your_api_key_here
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

---

## Troubleshooting

### "API key not valid" Error

1. Get a new key from https://aistudio.google.com/app/apikey
2. Update `.env` file
3. Restart the backend

### Frontend Can't Connect to Backend

1. Ensure backend is running on port 8000
2. Check `vite.config.js` proxy configuration
3. Check browser console for CORS errors

---

## Free Tier Limits

| Service | Limit | Notes |
|---------|-------|-------|
| Google Gemini | 15 RPM / 1M TPM | Completely free |
| HuggingFace Embeddings | Rate limited | Free, no API key needed |
| ChromaDB | Local only | No limits |

---

## Roadmap

- [ ] Add conversation history
- [ ] User accounts and saved conversations
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Professional therapist directory integration
- [ ] Crisis helpline detection and resources

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
---

## Disclaimer

This AI chatbot provides general relationship advice and should not replace professional therapy or counseling. If you're experiencing serious mental health concerns, abuse, or crisis situations, please seek professional help.

**Crisis Resources:**
- National Domestic Violence Hotline: 1-800-799-7233
- Crisis Text Line: Text HOME to 741741
- National Suicide Prevention Lifeline: 988

---

Made with 💜 for anyone navigating modern relationships.

---

## Star History

If you found this project helpful, please consider giving it a star! ⭐
