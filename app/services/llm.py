from typing import Literal  
from openai import OpenAI 
from app.config import TEXT_MODEL
from app.prompts.roles import build_prompt 

client = OpenAI()

# role must be one of these
Role = Literal["kid", "expert", "teacher"]

def ask_role(role: Role, instruction: str, context: str = "") -> str:
    """
    Ask one of the roles (kid, expert, teacher) to respond.

    Parameters:
        role (str): 'kid', 'expert', or 'teacher'
        instruction (str): the user's request (e.g., 'any questions?')
        context (str): prior explanation or transcript

    Returns:
        str: role-specific reply
    """
    # get the system prompt and user prompt for that role
    system, user = build_prompt(role, instruction, context)

    # send it to the gpt Responses API
    response = client.responses.create(
        model=TEXT_MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )

    # return the text (no formatting or json)
    return response.output_text.strip()
