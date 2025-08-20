import re
from typing import List
from queue import Queue
from app.config import VOICE_TRIGGER_REGEX, TRANSCRIPT_CONTEXT_LINES, TRANSCRIPT_MAX_LINES
from app.services.llm import ask_role
from app.services.tts import speak

# compile voice trigger regex for matching role commands
ROLE_RE = re.compile(VOICE_TRIGGER_REGEX, re.IGNORECASE)

def handle_asr_queue(speech_queue: Queue, conversation_history: List[str]) -> List[str]:
    """
    Handle new spoken lines from the speech queue.

    For each spoken sentence:
      - Add it to the conversation history
      - If it starts with a role (like "Kid, ..."), ask the LLM and speak the response
      - Return all AI replies so they can be shown in the UI
    """
    # store LLM replies to return later
    spoken_responses = []

    # go through everything that’s in the speech queue (new things the user just said)
    while not speech_queue.empty():
        # get the next spoken sentence from the queue
        spoken_text = speech_queue.get()

        # add it to our full chat history
        conversation_history.append(spoken_text)

        # if the history is getting too long, remove the oldest lines
        del conversation_history[:-TRANSCRIPT_MAX_LINES]

        # try to match this sentence to the expected format: "Role, instruction"
        match = ROLE_RE.match(spoken_text)

        # if the sentence doesn’t match that format, skip it and move to the next one
        if not match:
            print("No role match:", spoken_text)
            continue
         
        # get the role from the sentence ("kid", "expert", "teacher")
        role = match.group(1).lower()
        print("Matched role:", role)

        # get the instruction part from the sentence (like "any questions?")
        instruction = match.group(2).strip()

        # take the most recent lines from the conversation to give context to LLM
        context = "\n".join(conversation_history[-TRANSCRIPT_CONTEXT_LINES:])

        # get reply using the role, instruction, and recent conversation
        reply = ask_role(role, instruction, context)

        # speak the reply out loud using tts function
        speak(f"{role.capitalize()}: {reply}")

        # store reply to dislpay in ui
        spoken_responses.append(f"{role.capitalize()}: {reply}")

    # after handling everything in the speech queue, return all the LLM replies
    return spoken_responses
