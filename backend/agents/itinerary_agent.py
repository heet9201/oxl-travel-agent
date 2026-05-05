from agents.base_agent import BaseAgent
from config import DEFAULT_CURRENCY_SYMBOL
import uuid


class ItineraryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Itinerary Agent",
            system_prompt=f"""You are an expert travel itinerary planner for an AI travel assistant.
Create detailed, realistic day-by-day travel itineraries.
All costs in {DEFAULT_CURRENCY_SYMBOL}.
Consider:
- Logical geographic routing (don't criss-cross the city)
- Realistic time for activities and travel between locations
- Meal breaks and rest time
- Mix of popular and hidden gem attractions
- Opening hours and best visit times
- Local transport options between activities"""
        )

    async def generate_itinerary(self, destination: str, start_date: str, end_date: str,
                                  budget: float = None, travelers: int = 1,
                                  preferences: list = None, travel_style: str = "balanced") -> dict:
        pref_str = ", ".join(preferences) if preferences else "general sightseeing"
        prompt = f"""Create a detailed day-by-day itinerary for:
- Destination: {destination}
- Dates: {start_date} to {end_date}
- Travelers: {travelers}
- Style: {travel_style}
- Interests: {pref_str}
{f'- Budget: {DEFAULT_CURRENCY_SYMBOL}{budget}' if budget else ''}

Return JSON:
{{
    "id": "{uuid.uuid4().hex[:8]}",
    "destination": "{destination}",
    "start_date": "{start_date}",
    "end_date": "{end_date}",
    "total_days": 0,
    "days": [
        {{
            "day": 1,
            "date": "{start_date}",
            "title": "Arrival & First Impressions",
            "activities": [
                {{
                    "time": "09:00",
                    "name": "Activity Name",
                    "description": "Brief description",
                    "duration": "2 hours",
                    "cost": 500,
                    "type": "sightseeing",
                    "location": "Specific location"
                }}
            ],
            "meals": [
                {{
                    "time": "13:00",
                    "type": "lunch",
                    "suggestion": "Restaurant Name - local cuisine",
                    "cost": 800
                }}
            ],
            "transport": [
                {{
                    "from": "Hotel",
                    "to": "Attraction",
                    "mode": "taxi",
                    "cost": 200,
                    "duration": "20 min"
                }}
            ],
            "estimated_cost": 3000
        }}
    ],
    "total_estimated_cost": 0,
    "budget_breakdown": {{
        "activities": 0,
        "food": 0,
        "transport": 0,
        "accommodation": 0,
        "miscellaneous": 0
    }},
    "tips": [
        "Pro tip 1",
        "Pro tip 2"
    ]
}}

Create a complete itinerary for each day. Be specific with activity names, locations, costs, and timings.
Include 3-5 activities per day with meals and transport."""
        return await self.generate_json(prompt)
