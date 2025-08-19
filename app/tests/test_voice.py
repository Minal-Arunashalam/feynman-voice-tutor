from app.services.audio import record_audio, transcribe

path = record_audio(duration=5)  # record 5 seconds
text = transcribe(path)
print("Transcript:", text)
