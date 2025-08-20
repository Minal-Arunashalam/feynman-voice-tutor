import os
from dotenv import load_dotenv  # load from .env file (for dev only)

load_dotenv()

# the OpenAI model to use for LLM responses
TEXT_MODEL = os.getenv("FEYNMAN_TEXT_MODEL", "gpt-5")  # default = gpt5

TTS_MODEL  = os.getenv("FEYNMAN_TTS_MODEL",  "gpt-4o-mini-tts")
TTS_VOICE  = os.getenv("FEYNMAN_TTS_VOICE",  "shimmer")

STT_MODEL = os.getenv("FEYNMAN_STT_MODEL", "gpt-4o-mini-transcribe")

# in app/config.py
SAMPLE_RATE   = int(16000)
VAD_LEVEL     = float(0.010)
MAX_UTTER_SEC = int(8)
VOICE_TRIGGER_REGEX = r"^(kid|expert|teacher)[:,]?\s*(.+)$"
TRANSCRIPT_MAX_LINES = 100
TRANSCRIPT_CONTEXT_LINES = 12
DEFAULT_CONTEXT_SECS = 90
