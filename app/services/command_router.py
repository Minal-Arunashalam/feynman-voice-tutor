from app.services.llm import ask_role

# for doing voice based role routing
def route_voice_command(text, context):
    text = text.lower().strip()
    # ask the corresponding role based on the command. slice away the role prefix
    if text.startswith("kid,"):
        return "kid", ask_role("kid", text[4:].strip(), context)
    elif text.startswith("expert,"):
        return "expert", ask_role("expert", text[7:].strip(), context)
    elif text.startswith("teacher,"):
        return "teacher", ask_role("teacher", text[8:].strip(), context)
    else:
        return "unknown", "Sorry, I didn't understand who to talk to. Please say 'Kid, ...' or 'Teacher, ...'"
