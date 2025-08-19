import os
import tempfile
import simpleaudio as sa #audio plays from laptop, not in browser
from openai import OpenAI
from app.config import TTS_MODEL, TTS_VOICE

client = OpenAI()

def speak(text: str) -> None:
    """
    Convert text to speech using OpenAI TTS and play it synchronously.
    """
    #create speech file from text, in wav format
    audio = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        format="wav"
    )
    # get the audio bytes from the response
    audio_bytes = audio.read()

    # write audio bytes to a temp wav file so we can play it
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name
        # get the wave object and play it
        wave_obj = sa.WaveObject.from_wave_file(tmp_path)
        play_obj = wave_obj.play()
        # block until file is done playing
        play_obj.wait_done()  
    finally:
        # clean up temp file
        if tmp_path:
            try:
                os.remove(tmp_path)
            except Exception:
                pass
