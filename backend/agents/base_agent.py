import google.generativeai as genai
from config import GEMINI_API_KEY, LLM_MODEL
import json
import re


class BaseAgent:
    """Base class for all specialized agents."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=LLM_MODEL,
            system_instruction=system_prompt,
        )

    async def generate(self, prompt: str, response_format: str = "text") -> str:
        """Generate a response from the LLM."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error from {self.name}: {str(e)}"

    async def generate_json(self, prompt: str) -> dict:
        """Generate a JSON response from the LLM."""
        full_prompt = f"""{prompt}

IMPORTANT: Respond ONLY with valid JSON. No markdown, no code blocks, no extra text.
Do not wrap in ```json``` or any other formatting."""
        try:
            response = self.model.generate_content(full_prompt)
            text = response.text.strip()
            # Strip markdown code blocks if present
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            text = text.strip()
            return json.loads(text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response", "raw": response.text if response else ""}
        except Exception as e:
            return {"error": str(e)}
