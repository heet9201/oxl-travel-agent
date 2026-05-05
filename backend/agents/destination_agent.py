from agents.base_agent import BaseAgent
from config import DEFAULT_CURRENCY_SYMBOL


class DestinationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Destination Agent",
            system_prompt=f"""You are a destination recommendation expert for an AI travel assistant.
Your job is to suggest travel destinations based on user preferences, budget, and travel dates.
Always consider:
- Season and weather suitability
- Budget appropriateness (currency: {DEFAULT_CURRENCY_SYMBOL})
- Travel style (adventure, relaxation, culture, etc.)
- Safety and accessibility
- Unique experiences available

Provide detailed, enthusiastic recommendations with practical insights."""
        )

    async def suggest_destinations(self, preferences: dict) -> dict:
        prompt = f"""Based on these travel preferences, suggest 3-5 destinations:

Preferences: {preferences}
Budget: {preferences.get('budget', 'flexible')} {DEFAULT_CURRENCY_SYMBOL}
Travel dates: {preferences.get('dates', 'flexible')}
Travel style: {preferences.get('style', 'balanced')}
Travelers: {preferences.get('travelers', 1)}

Return JSON with this structure:
{{
    "destinations": [
        {{
            "name": "City, Country",
            "description": "Brief description why this is a great match",
            "best_for": ["relaxation", "culture"],
            "estimated_daily_cost": 5000,
            "weather_summary": "Sunny, 25-30°C",
            "top_attractions": ["Attraction 1", "Attraction 2", "Attraction 3"],
            "match_score": 95
        }}
    ],
    "reasoning": "Why these destinations were chosen"
}}"""
        return await self.generate_json(prompt)
