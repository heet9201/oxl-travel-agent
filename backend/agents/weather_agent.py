from agents.base_agent import BaseAgent


class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Weather Agent",
            system_prompt="""You are a weather information specialist for an AI travel assistant.
Provide weather forecasts and travel impact assessments based on destination and dates.
Use your knowledge of typical weather patterns for destinations.
Always mention how weather might affect planned activities."""
        )

    async def get_weather(self, destination: str, dates: str) -> dict:
        prompt = f"""Provide weather information for:
- Destination: {destination}
- Travel dates: {dates}

Return JSON:
{{
    "destination": "{destination}",
    "dates": "{dates}",
    "forecast": {{
        "temperature_range": "25-32°C",
        "conditions": "Partly cloudy with occasional showers",
        "humidity": "70-80%",
        "rainfall_chance": "30%"
    }},
    "travel_impact": {{
        "outdoor_activities": "Good - carry umbrella",
        "beach_weather": "Excellent",
        "sightseeing": "Good - prefer mornings"
    }},
    "packing_suggestions": ["Light clothes", "Sunscreen", "Umbrella"],
    "best_time_of_day": "Mornings and evenings are most pleasant",
    "warnings": []
}}"""
        return await self.generate_json(prompt)
