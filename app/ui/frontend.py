import streamlit as st
from app.services.llm import ask_role
from app.services.tts import speak

st.set_page_config(page_title="Feynman Voice Tutor", layout="wide")
st.title("🧠 Feynman Voice Tutor")

context = st.text_area("✍️ Your Explanation", height=250, placeholder="Explain a topic here...")
instruction = st.text_input("🎤 Ask a Role", placeholder="e.g., 'Any questions?' or 'Explain entropy again'")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👶 Ask Kid"):
        with st.spinner("Kid is thinking..."):
            output = ask_role("kid", instruction, context)
            st.success("Kid:")
            st.write(output)
            speak(f"Kid: {output}") # speak the reply

with col2:
    if st.button("🧪 Ask Expert"):
        with st.spinner("Expert is thinking..."):
            output = ask_role("expert", instruction, context)
            st.success("Expert:")
            st.write(output)
            speak(f"Expert: {output}") 

with col3:
    if st.button("🎓 Ask Teacher"):
        with st.spinner("Teacher is thinking..."):
            output = ask_role("teacher", instruction, context)
            st.success("Teacher:")
            st.write(output)
            speak(f"Teacher: {output}")
