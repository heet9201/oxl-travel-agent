from fastapi import APIRouter, HTTPException
from models.schemas import ItineraryRequest
from agents.itinerary_agent import ItineraryAgent

router = APIRouter(prefix="/api/itinerary", tags=["itinerary"])
itinerary_agent = ItineraryAgent()

# In-memory store for MVP
itinerary_store: dict = {}


@router.post("/generate")
async def generate_itinerary(request: ItineraryRequest):
    """Generate a full travel itinerary."""
    try:
        result = await itinerary_agent.generate_itinerary(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            budget=request.budget,
            travelers=request.travelers,
            preferences=request.preferences,
            travel_style=request.travel_style,
        )
        # Store the itinerary
        if "id" in result:
            itinerary_store[result["id"]] = result
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{itinerary_id}")
async def get_itinerary(itinerary_id: str):
    """Get a saved itinerary by ID."""
    if itinerary_id not in itinerary_store:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary_store[itinerary_id]
