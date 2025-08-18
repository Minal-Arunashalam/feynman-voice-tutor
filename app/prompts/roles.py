from typing import Literal, Tuple
from app.constants import SYSTEM_KID, SYSTEM_EXPERT, SYSTEM_TEACHER

# roles
Role = Literal["kid", "expert", "teacher"]

def build_prompt(role: Role, user_instruction: str, recent_context: str) -> Tuple[str, str]:
    """
    Create the system and user prompt for the given role.
    Each role behaves differently based on its system instructions.
    """

    instruction = (user_instruction or "").strip()  # user’s command to the role
    ctx = f"RECENT CONTEXT (explanation or notes):\n{recent_context}\n"  # what user just explained

    # handle special trigger (like “any questions?”)
    instruction_lower = instruction.lower()
    if role in ("kid", "expert") and ("any question" in instruction_lower or "any questions" in instruction_lower):
        if role == "kid":
            user = (
                "Ask ONE short, simple question that would help a beginner understand the explanation.\n" +
                ctx
            )
        else:
            user = (
                "Ask ONE rigorous, high-leverage question to expose a flaw, assumption, or missing case.\n" +
                ctx
            )
    else:
        # if not asking for "any question", prompt goes to teacher role
        user = f"Follow this instruction in your role: {instruction}\n\n{ctx}"

    # return the right system and user prompt based on role
    if role == "kid":
        return SYSTEM_KID, user
    elif role == "expert":
        return SYSTEM_EXPERT, user
    else:
        # teacher
        return SYSTEM_TEACHER, user
