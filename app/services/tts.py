# app/services/tts.py

import os
import tempfile
import simpleaudio as sa
from openai import OpenAI
from app.config import TTS_MODEL, TTS_VOICE

client = OpenAI()

def speak(text: str) -> None:
    """
    Convert text to speech with OpenAI and play it.
    Saves audio as a temporary .wav and plays with simpleaudio.
    """
    tmp_path = None
    try:
        # Create streaming TTS response and save as WAV
        with client.audio.speech.with_streaming_response.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text,
            response_format="wav",
        ) as response:
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            response.stream_to_file(tmp.name)
            tmp_path = tmp.name

        # Play WAV
        wave_obj = sa.WaveObject.from_wave_file(tmp_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    finally:
        if tmp_path:
            try: os.remove(tmp_path)
            except Exception: pass
