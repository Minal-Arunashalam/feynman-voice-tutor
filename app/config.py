import os
from dotenv import load_dotenv  # load from .env file (for dev only)

load_dotenv()

# the OpenAI model to use for LLM responses
TEXT_MODEL = os.getenv("FEYNMAN_TEXT_MODEL", "gpt-5")  # default = gpt5

TTS_MODEL  = os.getenv("FEYNMAN_TTS_MODEL",  "gpt-4o-mini-tts")
TTS_VOICE  = os.getenv("FEYNMAN_TTS_VOICE",  "shimmer")

STT_MODEL = os.getenv("FEYNMAN_STT_MODEL", "gpt-4o-mini-transcribe")