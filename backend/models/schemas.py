from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str
    message_type: str = Field(default="text", description="text, flights, hotels, itinerary, budget")
    data: Optional[dict] = None


class ChatRequest(BaseModel):
    message: str
    conversation_history: list[ChatMessage] = []
    trip_context: Optional[dict] = None


class ChatResponse(BaseModel):
    reply: str
    message_type: str = "text"
    data: Optional[dict] = None
    trip_context: Optional[dict] = None


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    passengers: int = 1
    budget_max: Optional[float] = None
    travel_class: str = "economy"


class HotelSearchRequest(BaseModel):
    destination: str
    check_in: str
    check_out: str
    guests: int = 1
    rooms: int = 1
    budget_max: Optional[float] = None
    rating_min: Optional[float] = None


class ItineraryRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: Optional[float] = None
    travelers: int = 1
    preferences: list[str] = []
    travel_style: str = "balanced"


class FlightOption(BaseModel):
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    duration: str
    stops: int
    price: float
    travel_class: str = "economy"
    origin: str
    destination: str


class HotelOption(BaseModel):
    name: str
    rating: float
    price_per_night: float
    total_price: float
    location: str
    amenities: list[str]
    room_type: str
    image_placeholder: str = ""


class DayPlan(BaseModel):
    day: int
    date: str
    title: str
    activities: list[dict]
    meals: list[dict] = []
    transport: list[dict] = []
    estimated_cost: float = 0


class Itinerary(BaseModel):
    id: str
    destination: str
    start_date: str
    end_date: str
    total_days: int
    days: list[DayPlan]
    total_estimated_cost: float
    budget_breakdown: dict
    tips: list[str] = []


class BudgetBreakdown(BaseModel):
    total_budget: float
    total_estimated: float
    categories: dict[str, float]
    savings_tips: list[str] = []
    within_budget: bool = True
