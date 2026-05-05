import google.generativeai as genai
from openai import AsyncOpenAI
from config import GEMINI_API_KEY, NVIDIA_API_KEY, MODEL_PRIORITY_LIST
import json
import re
import logging

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all specialized agents."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Configure NVIDIA NIM (OpenAI Client)
        self.nvidia_client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_API_KEY
        )

    async def _try_generate_with_model(self, model_name: str, prompt: str, is_json: bool = False) -> str:
        """Attempt to generate response with a specific model."""
        try:
            if "gemini" in model_name:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=self.system_prompt,
                )
                response = model.generate_content(prompt)
                return response.text
            else:
                # Use NVIDIA NIM
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
                completion = await self.nvidia_client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024,
                )
                return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Model {model_name} failed in {self.name}: {str(e)}")
            raise e

    async def _generate_with_fallback(self, prompt: str, is_json: bool = False) -> str:
        """Execute generation with fallback logic through the priority list."""
        for model_name in MODEL_PRIORITY_LIST:
            try:
                return await self._try_generate_with_model(model_name, prompt, is_json)
            except Exception:
                continue
                
        # If all models fail
        logger.error(f"All models failed in {self.name} for prompt: {prompt[:100]}...")
        raise Exception("All fallback models exhausted.")

    async def generate(self, prompt: str, response_format: str = "text") -> str:
        """Generate a response from the LLM."""
        try:
            return await self._generate_with_fallback(prompt)
        except Exception:
            return "We’re having trouble processing your request right now. Please try again."

    async def generate_json(self, prompt: str) -> dict:
        """Generate a JSON response from the LLM."""
        full_prompt = f"""{prompt}

IMPORTANT: Respond ONLY with valid JSON. No markdown, no code blocks, no extra text.
Do not wrap in ```json``` or any other formatting."""
        try:
            text = await self._generate_with_fallback(full_prompt, is_json=True)
            text = text.strip()
            # Strip markdown code blocks if present
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            text = text.strip()
            return json.loads(text)
        except json.JSONDecodeError:
            logger.error(f"JSON Parse Error in {self.name}. Raw text: {text}")
            return {"error": "Failed to parse JSON response"}
        except Exception as e:
            return {"error": "We’re having trouble processing your request right now. Please try again."}
