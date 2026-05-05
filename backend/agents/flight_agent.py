from agents.base_agent import BaseAgent
from config import DEFAULT_CURRENCY_SYMBOL


class FlightAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Flight Agent",
            system_prompt=f"""You are a flight search specialist for an AI travel assistant.
Generate realistic flight search results based on user queries.
Use real airline names that actually operate the requested routes.
Prices should be in {DEFAULT_CURRENCY_SYMBOL} and realistic for the route.
Include a mix of budget, mid-range, and premium options.
Consider actual flight durations and common layover cities."""
        )

    async def search_flights(self, origin: str, destination: str, departure_date: str,
                             return_date: str = None, passengers: int = 1,
                             budget_max: float = None, travel_class: str = "economy") -> dict:
        prompt = f"""Generate realistic flight search results for:
- Route: {origin} → {destination}
- Departure: {departure_date}
{f'- Return: {return_date}' if return_date else '- One way'}
- Passengers: {passengers}
- Class: {travel_class}
{f'- Max budget: {DEFAULT_CURRENCY_SYMBOL}{budget_max}' if budget_max else ''}

Return JSON:
{{
    "flights": [
        {{
            "airline": "Air India",
            "flight_number": "AI-302",
            "departure_time": "06:30",
            "arrival_time": "09:15",
            "duration": "2h 45m",
            "stops": 0,
            "price": 5400,
            "travel_class": "economy",
            "origin": "{origin}",
            "destination": "{destination}",
            "origin_airport": "DEL",
            "destination_airport": "GOI",
            "baggage": "15kg included"
        }}
    ],
    "cheapest": 0,
    "fastest": 0,
    "best_value": 0,
    "search_summary": "Found X flights from {origin} to {destination}"
}}

Generate 4-6 realistic options with varying prices, airlines, and timings.
Sort by price ascending. Use airlines that actually fly this route."""
        return await self.generate_json(prompt)
