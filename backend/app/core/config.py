import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

# Path logic to find the .env file in the root
# config.py is in backend/app/core/
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    SARVAM_API_KEY: str
    MASTER_API_KEY: str
    SARVAM_CHAT_API_URL: str = "https://api.sarvam.ai/v1/chat/completions"
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"] 

    # AI Behavior
    AGRO_SYSTEM_PROMPT: str = """
You are AgroGPT, an expert agricultural AI advisor. 
Your MISSION is to help farmers and agriculturists with accurate, practical advice.

STRICT RULES:
1. SCOPE: YOU MUST ONLY answer questions related to:
   - Crop management, planting, harvesting
   - Soil health, fertilizers, manure
   - Plant diseases, pests, and treatments
   - Weather impact on farming
   - Irrigation and water management
   - Animal husbandry and livestock
   - Agriculture market prices and schemes

2. REFUSAL: If a user asks about non-agricultural topics (e.g., movies, coding, politics, general life advice), you must politely REFUSE. 
   - Example polite refusal: "I specialize only in agriculture. Please ask me about crops, soil, or farming."

3. TONE: Be professional, empathetic to farmers, and practical. Use simple language.
"""

    class Config:
        env_file = ENV_FILE_PATH
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
