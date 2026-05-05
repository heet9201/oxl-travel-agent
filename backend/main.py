from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router
from routes.search import router as search_router
from routes.itinerary import router as itinerary_router

app = FastAPI(
    title="OXL Travel Agent API",
    description="AI-Powered Multi-Agent Travel Assistant Backend",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(chat_router)
app.include_router(search_router)
app.include_router(itinerary_router)


@app.get("/")
async def root():
    return {"message": "OXL Travel Agent API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
