from agents.base_agent import BaseAgent
from config import DEFAULT_CURRENCY_SYMBOL


class BudgetAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Budget Agent",
            system_prompt=f"""You are a budget planning specialist for an AI travel assistant.
You help travelers estimate costs and allocate budgets wisely.
All prices in {DEFAULT_CURRENCY_SYMBOL}.
Provide realistic cost estimates based on destination and travel style.
Always suggest ways to save money without compromising experience."""
        )

    async def estimate_budget(self, destination: str, days: int, travelers: int = 1,
                              style: str = "balanced", total_budget: float = None) -> dict:
        prompt = f"""Create a detailed budget breakdown for:
- Destination: {destination}
- Duration: {days} days
- Travelers: {travelers}
- Travel style: {style}
{f'- Total budget: {DEFAULT_CURRENCY_SYMBOL}{total_budget}' if total_budget else ''}

Return JSON:
{{
    "total_budget": {total_budget if total_budget else 0},
    "total_estimated": 0,
    "categories": {{
        "flights": 0,
        "accommodation": 0,
        "food": 0,
        "transport": 0,
        "activities": 0,
        "shopping": 0,
        "miscellaneous": 0
    }},
    "daily_breakdown": {{
        "accommodation": 0,
        "food": 0,
        "transport": 0,
        "activities": 0
    }},
    "savings_tips": [
        "Tip 1",
        "Tip 2"
    ],
    "within_budget": true,
    "budget_summary": "Brief summary of the budget allocation"
}}

Provide realistic estimates. If total_budget is given, try to fit within it."""
        return await self.generate_json(prompt)
