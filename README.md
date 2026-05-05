# 🧭 OXL Travel Agent — AI-Powered Multi-Agent Travel Assistant

An intelligent, multi-agent AI travel assistant that can plan, optimize, and manage entire travel journeys through natural conversation.

## Features (MVP)
- 💬 **Chat Interface** — Conversational AI travel assistant
- 📋 **Itinerary Generation** — Day-by-day trip plans with activities, meals, and transport
- ✈️ **Flight Search** — AI-generated realistic flight options
- 🏨 **Hotel Search** — Hotel recommendations with ratings and amenities
- 💰 **Budget Estimation** — Cost breakdowns with savings tips

## Tech Stack
- **Frontend**: Next.js 16 (App Router) + Vanilla CSS
- **Backend**: Python FastAPI
- **AI**: Google Gemini API (multi-agent system)
- **Styling**: Dark mode with glassmorphism design

## Quick Start

### 1. Set up the Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your Gemini API Key
Edit `backend/.env`:
```
GEMINI_API_KEY=your_actual_key_here
```
Get a free key at: https://aistudio.google.com/apikey

### 3. Start the Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 4. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

### 5. Open the App
Visit http://localhost:3000

## Project Structure
```
oxl-travel-agent/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py             # Environment config
│   ├── agents/               # Multi-agent system
│   │   ├── orchestrator.py   # Central supervisor agent
│   │   ├── destination_agent.py
│   │   ├── flight_agent.py
│   │   ├── hotel_agent.py
│   │   ├── budget_agent.py
│   │   ├── weather_agent.py
│   │   └── itinerary_agent.py
│   ├── models/schemas.py     # Pydantic models
│   └── routes/               # API endpoints
│       ├── chat.py
│       ├── search.py
│       └── itinerary.py
├── frontend/
│   └── src/
│       ├── app/              # Next.js pages
│       ├── components/       # React components
│       └── lib/api.js        # API client
└── prd.md                    # Product requirements
```

## License
MIT