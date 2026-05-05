import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")

# Fallback Models Priority List
MODEL_PRIORITY_LIST = [
    # "gemini-2.5-flash",
    # "gemini-2.5-flash-lite",
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-8b-instruct",
]


DEFAULT_CURRENCY = "INR"
DEFAULT_CURRENCY_SYMBOL = "₹"
