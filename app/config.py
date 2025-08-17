import os
from dotenv import load_dotenv  # load from .env file (for dev only)

load_dotenv()

# the OpenAI model to use for LLM responses
TEXT_MODEL = os.getenv("FEYNMAN_TEXT_MODEL", "gpt-5")  # default = gpt5

# STT and TTS models will go here later
