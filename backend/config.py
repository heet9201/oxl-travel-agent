import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Fallback Models Priority List
MODEL_PRIORITY_LIST = [
    # Best Groq models for travel planning
    "groq/llama-3.3-70b-versatile",
    "groq/mixtral-8x7b-32768",
    # NVIDIA models as fallbacks
    "nvidia/meta/llama-3.1-70b-instruct",
    "nvidia/meta/llama-3.1-8b-instruct",
]



DEFAULT_CURRENCY = "INR"
DEFAULT_CURRENCY_SYMBOL = "₹"
