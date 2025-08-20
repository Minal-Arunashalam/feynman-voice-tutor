import time
import numpy as np
#for recording audio
import sounddevice as sd
# queue for passing data between threads
from queue import Queue
# for stopping the recording loop
from threading import Event
from openai import OpenAI
# sample rate for how many samples per second, vad level is energy threshold for speech detection, 
# max utterance per sec is max seconds to record before stopping
from app.config import SAMPLE_RATE, VAD_LEVEL, MAX_UTTER_SEC, STT_MODEL
# convert audio to wav format
from app.utils.wav import float32_to_wav_bytes
import tempfile
import os

client = OpenAI()

# internal helper function to transcribe numpy audio array to text.
# takes audio data and sample rate, converts audio to wav, sends to OpenAI STT, gets text back
def _transcribe_numpy(audio_f32: np.ndarray, sample_rate: int) -> str:
    """Convert float32 audio array -> temp WAV -> OpenAI STT -> text."""
    # convert audio array to WAV bytes
    wav_bytes = float32_to_wav_bytes(audio_f32, sample_rate)
    # create temp wav file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(wav_bytes)
        tmp_path = f.name
    try:
        # open temp wav file
        with open(tmp_path, "rb") as f:
            try:
                # get transcription
                tr = client.audio.transcriptions.create(model=STT_MODEL, file=f)
            except Exception:
                # if fails, use whisper model
                f.seek(0)
                tr = client.audio.transcriptions.create(model="whisper-1", file=f)
        # retunr the transcribed text
        return (tr.text or "").strip()
    finally:
        # delete the temp file
        try: os.remove(tmp_path)
        except Exception: pass

# function to record audio and transcribe in a loop
# runs in background, segments speech, transcribes, and puts text in a queue
def record_and_transcribe_loop(stop_event: Event, q: Queue, sample_rate: int = SAMPLE_RATE, level: float = VAD_LEVEL, max_sec: int = MAX_UTTER_SEC):
    # Initialize conversation history at the start
    conversation_history = []
    """
    Background loop:
    - records mic audio continuously
    - segments utterances using energy threshold
    - transcribes each utterance and pushes the text to queue
    """
    # analysis window (how often we check for speech)
    window = int(0.25 * sample_rate)  
    # buffer to hold audio data
    buf = np.zeros(0, dtype=np.float32)

    audio_q = Queue()

    def callback(indata, frames, time_info, status):
        # push audio safely into the queue
        audio_q.put(indata.copy().flatten())

    print("hi")
    # start recording from the microphone
    with sd.InputStream(samplerate=sample_rate, channels=1, dtype="float32", callback=callback):
        # keep looping until stop_event is set
        while not stop_event.is_set():
            time.sleep(0.1)  # wait a bit

            # drain audio_q into buf
            while not audio_q.empty():
                buf = np.concatenate([buf, audio_q.get()])

            # if enough audio is in buffer, process it
            if len(buf) >= window:
                chunk = buf[:window]
                print("energy:", np.mean(np.abs(chunk)))
                #print("chunk with", len(chunk), "samples")
                
                buf = buf[window:]
                # check if chunk is above the energy threshold (loud enough to be speech)
                if np.mean(np.abs(chunk)) > level:
                    seg = [chunk]
                    print("Captured chunk with", len(chunk), "samples")
                    start = time.time()
                    # keep collecting audio until silence or max seconds
                    while time.time() - start < max_sec and not stop_event.is_set():
                        time.sleep(0.1)
                        # pull more audio into buf
                        while not audio_q.empty():
                            buf = np.concatenate([buf, audio_q.get()])
                        if len(buf) >= window:
                            c = buf[:window]
                            buf = buf[window:]
                            seg.append(c)
                            # stop if silence is detected
                            if np.mean(np.abs(c)) <= level:
                                break
                    # combine all segments into one audio array
                    audio = np.concatenate(seg)
                    try:
                        # transcribe the audio
                        text = _transcribe_numpy(audio, sample_rate)
                        # if transcription is not empty, process it immediately
                        if text:
                            # put in queue and process immediately
                            q.put(text)
                            # force queue processing right away
                            from app.controllers.voice import handle_asr_queue
                            handle_asr_queue(q, conversation_history)
                    except Exception as e:
                        # if error, put error message in the queue
                        q.put(f"[ASR error: {e}]")
