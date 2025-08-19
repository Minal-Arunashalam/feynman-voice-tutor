from app.services.audio import record_audio, transcribe
from app.services.command_router import route_voice_command

context = "Entropy measures disorder or uncertainty in a system."

path = record_audio(duration=5)
text = transcribe(path)
role, reply = route_voice_command(text, context)

print(f"Role: {role}")
print(f"Reply: {reply}")
