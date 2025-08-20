# in-memory byte streams
import io
import wave
import numpy as np
from app.config import SAMPLE_RATE

# function to convert float32 audio array to WAV bytes
# sample_rate: number of samples per second
def float32_to_wav_bytes(audio_f32: np.ndarray, sample_rate: int = SAMPLE_RATE) -> bytes:
    # Convert float32 audio to int16 (wav standard)
    audio_i16 = np.int16(np.clip(audio_f32 * 32767, -32768, 32767))
    # create in mem byte stream
    bio = io.BytesIO()
    # open byte stream as a wave file
    with wave.open(bio, "wb") as wf:
        # one channel (mic)
        wf.setnchannels(1)
        # 2 bytes (16 bit samples)
        wf.setsampwidth(2)
        # sample rate
        wf.setframerate(sample_rate)
        # write audio data to wav file
        wf.writeframes(audio_i16.tobytes())
    # return wav file as bytes
    return bio.getvalue()
