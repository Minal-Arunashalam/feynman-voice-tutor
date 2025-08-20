# app/ui/app.py

# import streamlit for web UI
import streamlit as st
# import queue for managing audio data
import queue
# import threading for background tasks
import threading

# import functions for LLM, TTS, audio, and voice control
from app.services.llm import ask_role
from app.services.tts import speak
from app.services.audio import record_and_transcribe_loop
from app.controllers.voice import handle_asr_queue
from app.config import TRANSCRIPT_MAX_LINES, DEFAULT_CONTEXT_SECS, TRANSCRIPT_CONTEXT_LINES

# set up the page title and layout
st.set_page_config(page_title="Feynman Voice Tutor", layout="wide")
st.title("🧠 Feynman Voice Tutor")

# initialize session state variables if not already set
if "asr_running" not in st.session_state: st.session_state.asr_running = False
if "asr_queue"  not in st.session_state: st.session_state.asr_queue = queue.Queue()
if "asr_stop"   not in st.session_state: st.session_state.asr_stop = threading.Event()
if "transcript" not in st.session_state: st.session_state.transcript = []
if "context_secs" not in st.session_state: st.session_state.context_secs = DEFAULT_CONTEXT_SECS

# create two columns for layout
left, right = st.columns([3,2], gap="large")

with left:
    # show text area for user explanation
    st.subheader("✍️ Your Explanation")
    context = st.text_area("Used as context for the roles", height=220, placeholder="Explain a topic here...")

    # show input for role instructions
    st.subheader("🎤 Ask a Role (typed)")
    instruction = st.text_input("e.g., 'Any questions?' or 'Explain entropy again'")

    # create three columns for role buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        # button to ask kid role
        if st.button("👶 Ask Kid"):
            out = ask_role("kid", instruction, context)
            st.success("Kid:")
            st.write(out)
            speak(f"Kid: {out}")
    with c2:
        # button to ask expert role
        if st.button("🧪 Ask Expert"):
            out = ask_role("expert", instruction, context)
            st.success("Expert:")
            st.write(out)
            speak(f"Expert: {out}")
    with c3:
        # button to ask teacher role
        if st.button("🎓 Ask Teacher"):
            out = ask_role("teacher", instruction, context)
            st.success("Teacher:")
            st.write(out)
            speak(f"Teacher: {out}")

with right:
    # show voice control instructions
    st.subheader("🎙️ Voice Control")
    st.caption("Say: “Kid, …”, “Expert, …”, or “Teacher, …”. Example: “Kid, any questions?”")

    # function to start audio recording
    def start_asr():
        st.session_state.asr_stop.clear()
        st.session_state.asr_running = True
        threading.Thread(
            target=record_and_transcribe_loop,
            args=(st.session_state.asr_stop, st.session_state.asr_queue),
            daemon=True
        ).start()

    # function to stop audio recording
    def stop_asr():
        st.session_state.asr_stop.set()
        st.session_state.asr_running = False

    # create two columns for start/stop buttons
    b1, b2 = st.columns(2)
    with b1:
        # button to start listening
        if not st.session_state.asr_running and st.button("Start Listening"):
            start_asr()
    with b2:
        # button to stop listening
        if st.session_state.asr_running and st.button("Stop Listening"):
            stop_asr()

    # show live transcript area
    st.markdown("**Live Transcript (most recent first)**")
    live = st.empty()

    # process audio queue and show role responses as toasts
    toasts = handle_asr_queue(st.session_state.asr_queue, st.session_state.transcript)
    for t in toasts:
        st.toast(t, icon="🎤")

    # show the last 20 lines of transcript
    if st.session_state.transcript:
        tail = st.session_state.transcript[-20:]
        st.session_state.transcript = st.session_state.transcript[-TRANSCRIPT_MAX_LINES:]
        live.code("\n".join(list(reversed(tail))), language=None)
    else:
        live.info("No speech yet. Click Start Listening and talk into your mic.")

# show divider and tips at the bottom
st.divider()
st.caption("Tips: speak clearly; start with the role name (e.g., “Teacher, define cross-entropy.”)")
