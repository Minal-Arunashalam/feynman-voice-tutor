**Feynman Voice Tutor** is an interactive learning assistant that helps you practice the Feynman technique by letting you “teach out loud” and receive real-time feedback. 
The app continuously records your speech, transcribes it with OpenAI’s speech-to-text, and updates a live transcript. 

When you address a role—**Kid**, **Expert**, or **Teacher**—your request is routed through role-specific prompts to an LLM, which replies concisely, then speaks the response aloud using text-to-speech.

The **Kid** role asks simple questions to uncover gaps in your understanding ("if you can't explain it to a six year old, then you don't understand it yourself").
The **Expert** asks deeper, more specific questions to challenge your reasoning and push for depth.
The **Teacher** is there to give you explanations, examples, and definitions when you get stuck.

Built with Streamlit, Python, and OpenAI APIs (GPT-5, 4o Transcribe, 4o TTS), running locally with a modular design (services, controllers, UI) for easy extension. 
Latency is reduced through short fixed audio chunks, compact context windows, and streaming TTS, making the conversation feel fast and natural.
