from agents.base_agent import BaseAgent
from config import DEFAULT_CURRENCY_SYMBOL


class HotelAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Hotel Agent",
            system_prompt=f"""You are a hotel search specialist for an AI travel assistant.
Generate realistic hotel recommendations based on user queries.
Use real hotel names or realistic-sounding names for the destination.
Prices should be in {DEFAULT_CURRENCY_SYMBOL} per night and realistic.
Include a mix of budget, mid-range, and luxury options.
Consider location quality, amenities, and guest ratings."""
        )

    async def search_hotels(self, destination: str, check_in: str, check_out: str,
                            guests: int = 1, rooms: int = 1,
                            budget_max: float = None, rating_min: float = None) -> dict:
        prompt = f"""Generate realistic hotel search results for:
- Destination: {destination}
- Check-in: {check_in}
- Check-out: {check_out}
- Guests: {guests}, Rooms: {rooms}
{f'- Max budget: {DEFAULT_CURRENCY_SYMBOL}{budget_max}/night' if budget_max else ''}
{f'- Min rating: {rating_min}' if rating_min else ''}

Return JSON:
{{
    "hotels": [
        {{
            "name": "Hotel Name",
            "rating": 4.5,
            "price_per_night": 3500,
            "total_price": 17500,
            "location": "Near Beach / City Center",
            "amenities": ["WiFi", "Pool", "Breakfast", "AC"],
            "room_type": "Deluxe Double",
            "distance_to_center": "1.2 km",
            "review_highlight": "Amazing sea view and friendly staff"
        }}
    ],
    "best_value": 0,
    "highest_rated": 0,
    "search_summary": "Found X hotels in {destination}"
}}

Generate 4-6 realistic options. Include budget hostels to luxury resorts.
Sort by price ascending."""
        return await self.generate_json(prompt)
