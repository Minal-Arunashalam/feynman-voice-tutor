from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import os
from app.config import STT_MODEL
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# record audio from microphone and save as wav
#duration in seconds, fs is standard sample rate
def record_audio(duration=5, fs=44100):
    print("🎙️ Recording...")
    #1 channel (mic)
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # wait until recording is finished
    print("✅ Done recording")
    
    # save to temp WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_file.name, fs, audio)
    return temp_file.name

# sennd wav file to Whisper API
def transcribe(file_path):
    print("🔁 Transcribing...")
    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model=STT_MODEL,
            file=f
        )
    return transcript.text
