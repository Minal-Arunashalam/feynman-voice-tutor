# app/services/llm.py

from openai import OpenAI
from app.config import TEXT_MODEL 

# OpenAI client
client = OpenAI()

def ask_teacher(question: str, context: str = "") -> str:
    """
    Ask the 'Teacher' role to explain something in a clear, structured way.
    
    Parameters:
        question (str): what I want the teacher to explain
        context (str): optional prior context (e.g., what I've been teaching wiht feynman technique)

    Returns:
        str: a plain language teacher-style explanation
    """
    # system prompt for teacher role
    system_prompt = (
        "You are a teacher. Answer as if you're explaining to a smart student.\n"
        "Start with a three-sentence definition. Then give 2-3 key points. End with a concrete example.\n"
        "Avoid jargon unless it's explained. Be concise and clear."
    )

    # build user prompt
    user_prompt = f"Explain this topic: {question}"
    if context:
        user_prompt += f"\n\nContext:\n{context}"

    # get response from gpt
    response = client.responses.create(
        model=TEXT_MODEL,  # gpt4 or 4o
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.output_text.strip()  # return clean explanation
