from fastapi import APIRouter, HTTPException
from models.schemas import FlightSearchRequest, HotelSearchRequest
from agents.flight_agent import FlightAgent
from agents.hotel_agent import HotelAgent

router = APIRouter(prefix="/api/search", tags=["search"])
flight_agent = FlightAgent()
hotel_agent = HotelAgent()


@router.post("/flights")
async def search_flights(request: FlightSearchRequest):
    """Search for flights."""
    try:
        result = await flight_agent.search_flights(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date,
            return_date=request.return_date,
            passengers=request.passengers,
            budget_max=request.budget_max,
            travel_class=request.travel_class,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hotels")
async def search_hotels(request: HotelSearchRequest):
    """Search for hotels."""
    try:
        result = await hotel_agent.search_hotels(
            destination=request.destination,
            check_in=request.check_in,
            check_out=request.check_out,
            guests=request.guests,
            rooms=request.rooms,
            budget_max=request.budget_max,
            rating_min=request.rating_min,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
