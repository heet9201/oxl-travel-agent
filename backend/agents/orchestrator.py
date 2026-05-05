from agents.base_agent import BaseAgent
from agents.destination_agent import DestinationAgent
from agents.flight_agent import FlightAgent
from agents.hotel_agent import HotelAgent
from agents.budget_agent import BudgetAgent
from agents.weather_agent import WeatherAgent
from agents.itinerary_agent import ItineraryAgent
from config import DEFAULT_CURRENCY_SYMBOL
import json


class OrchestratorAgent(BaseAgent):
    """Supervisor agent that routes queries to specialized agents."""

    def __init__(self):
        super().__init__(
            name="Orchestrator",
            system_prompt=f"""You are the central orchestrator of an AI travel assistant called OXL Travel.
Your role is to understand user travel queries and provide helpful, conversational responses.
You coordinate between specialized agents for flights, hotels, destinations, budgets, weather, and itineraries.

Currency: {DEFAULT_CURRENCY_SYMBOL} (INR)

You should:
1. Be warm, enthusiastic, and knowledgeable about travel
2. Ask clarifying questions when needed
3. Provide structured, actionable responses
4. When you have enough info, suggest generating a full plan

When analyzing user intent, classify it as one of:
- "chat" — General conversation or clarifying questions
- "destination" — Asking for destination suggestions
- "flights" — Looking for flight options
- "hotels" — Looking for accommodation
- "itinerary" — Wants a full trip plan
- "budget" — Budget estimation or breakdown
- "weather" — Weather queries

Always be proactive in offering to help with the next step of planning."""
        )
        self.destination_agent = DestinationAgent()
        self.flight_agent = FlightAgent()
        self.hotel_agent = HotelAgent()
        self.budget_agent = BudgetAgent()
        self.weather_agent = WeatherAgent()
        self.itinerary_agent = ItineraryAgent()

    async def classify_intent(self, message: str, context: dict = None) -> dict:
        """Classify the user's intent to route to the right agent."""
        prompt = f"""Analyze this travel query and classify the intent.

User message: "{message}"
{f'Trip context: {json.dumps(context)}' if context else ''}

Return JSON:
{{
    "intent": "chat|destination|flights|hotels|itinerary|budget|weather",
    "entities": {{
        "destination": null,
        "origin": null,
        "start_date": null,
        "end_date": null,
        "budget": null,
        "travelers": null,
        "preferences": [],
        "travel_style": null
    }},
    "needs_clarification": false,
    "clarification_questions": []
}}

Extract all travel entities from the message. Set intent to the PRIMARY action needed."""
        return await self.generate_json(prompt)

    async def process_message(self, message: str, conversation_history: list = None,
                               trip_context: dict = None) -> dict:
        """Process a user message and route to appropriate agent(s)."""

        # Step 1: Classify intent
        intent_data = await self.classify_intent(message, trip_context)

        if "error" in intent_data:
            # Fallback to general chat
            reply = await self.generate(f"""The user said: "{message}"
Respond as a helpful travel assistant. Be warm and ask what kind of trip they're planning.""")
            return {"reply": reply, "message_type": "text", "data": None, "trip_context": trip_context}

        intent = intent_data.get("intent", "chat")
        entities = intent_data.get("entities", {})

        # Merge entities into trip context
        if trip_context is None:
            trip_context = {}
        for key, value in entities.items():
            if value is not None and value != [] and value != "":
                trip_context[key] = value

        # Step 2: Check if clarification is needed
        if intent_data.get("needs_clarification", False):
            questions = intent_data.get("clarification_questions", [])
            reply = await self.generate(f"""The user said: "{message}"
You need more info. Ask these questions naturally in a conversational way: {questions}
Also mention what you've understood so far from: {json.dumps(trip_context)}""")
            return {"reply": reply, "message_type": "text", "data": None, "trip_context": trip_context}

        # Step 3: Route to specialized agent
        if intent == "destination":
            data = await self.destination_agent.suggest_destinations(trip_context)
            reply = await self.generate(f"""The user asked: "{message}"
Here are destination suggestions: {json.dumps(data)}
Present these destinations in a warm, exciting way. Mention key highlights and why each is a great fit.
Ask if they'd like to explore any of these further or generate a full itinerary.""")
            return {"reply": reply, "message_type": "destinations", "data": data, "trip_context": trip_context}

        elif intent == "flights":
            origin = trip_context.get("origin", "Delhi")
            destination = trip_context.get("destination", "")
            if not destination:
                reply = "I'd love to search flights for you! Where would you like to fly to? And from which city?"
                return {"reply": reply, "message_type": "text", "data": None, "trip_context": trip_context}

            data = await self.flight_agent.search_flights(
                origin=origin,
                destination=destination,
                departure_date=trip_context.get("start_date", "upcoming"),
                return_date=trip_context.get("end_date"),
                passengers=trip_context.get("travelers", 1),
                budget_max=trip_context.get("budget"),
            )
            reply = await self.generate(f"""The user asked: "{message}"
Here are flight results: {json.dumps(data)}
Summarize the flight options briefly. Highlight the best value and cheapest options.
Ask if they want to book any or search for hotels next.""")
            return {"reply": reply, "message_type": "flights", "data": data, "trip_context": trip_context}

        elif intent == "hotels":
            destination = trip_context.get("destination", "")
            if not destination:
                reply = "I'd love to find hotels for you! Which destination are you looking at?"
                return {"reply": reply, "message_type": "text", "data": None, "trip_context": trip_context}

            data = await self.hotel_agent.search_hotels(
                destination=destination,
                check_in=trip_context.get("start_date", "upcoming"),
                check_out=trip_context.get("end_date", "upcoming"),
                guests=trip_context.get("travelers", 1),
                budget_max=trip_context.get("budget"),
            )
            reply = await self.generate(f"""The user asked: "{message}"
Here are hotel results: {json.dumps(data)}
Summarize the hotel options. Highlight best value and highest rated.
Ask if they want to generate a full itinerary.""")
            return {"reply": reply, "message_type": "hotels", "data": data, "trip_context": trip_context}

        elif intent == "budget":
            destination = trip_context.get("destination", "")
            if not destination:
                reply = "I can help estimate your travel budget! Which destination are you considering?"
                return {"reply": reply, "message_type": "text", "data": None, "trip_context": trip_context}

            # Calculate days from dates or default
            days = trip_context.get("days", 5)
            data = await self.budget_agent.estimate_budget(
                destination=destination,
                days=days,
                travelers=trip_context.get("travelers", 1),
                style=trip_context.get("travel_style", "balanced"),
                total_budget=trip_context.get("budget"),
            )
            reply = await self.generate(f"""The user asked: "{message}"
Here's the budget breakdown: {json.dumps(data)}
Present the budget in a clear, friendly way. Mention if they're within budget.
Share the savings tips. Ask if they'd like a detailed itinerary.""")
            return {"reply": reply, "message_type": "budget", "data": data, "trip_context": trip_context}

        elif intent == "weather":
            destination = trip_context.get("destination", "")
            dates = f"{trip_context.get('start_date', '')} to {trip_context.get('end_date', '')}"
            data = await self.weather_agent.get_weather(destination, dates)
            reply = await self.generate(f"""The user asked: "{message}"
Here's the weather info: {json.dumps(data)}
Present the weather in a friendly, practical way.
Mention packing suggestions and any warnings.""")
            return {"reply": reply, "message_type": "weather", "data": data, "trip_context": trip_context}

        elif intent == "itinerary":
            destination = trip_context.get("destination", "")
            if not destination:
                reply = "I'd love to create an itinerary for you! Where are you planning to go, and for how many days?"
                return {"reply": reply, "message_type": "text", "data": None, "trip_context": trip_context}

            data = await self.itinerary_agent.generate_itinerary(
                destination=destination,
                start_date=trip_context.get("start_date", "upcoming"),
                end_date=trip_context.get("end_date", "upcoming"),
                budget=trip_context.get("budget"),
                travelers=trip_context.get("travelers", 1),
                preferences=trip_context.get("preferences", []),
                travel_style=trip_context.get("travel_style", "balanced"),
            )
            reply = await self.generate(f"""The user asked: "{message}"
Here's the itinerary: {json.dumps(data)}
Give a brief, exciting summary of the trip plan. Mention highlights from each day.
Ask if they'd like to modify anything or search for flights and hotels.""")
            return {"reply": reply, "message_type": "itinerary", "data": data, "trip_context": trip_context}

        else:
            # General chat
            history_text = ""
            if conversation_history:
                history_text = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}"
                                          for m in conversation_history[-6:]])

            reply = await self.generate(f"""Conversation history:
{history_text}

User: {message}
Trip context so far: {json.dumps(trip_context) if trip_context else 'None'}

Respond as a helpful, warm travel assistant. If the user hasn't specified a destination yet,
ask about their interests. If you have some context, proactively suggest next steps
like searching flights, hotels, or generating an itinerary.""")
            return {"reply": reply, "message_type": "text", "data": None, "trip_context": trip_context}
