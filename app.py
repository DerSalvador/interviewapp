# app.py
import streamlit as st
import openai
from prompts import (
    get_zero_shot_prompt,
    get_few_shot_prompt,
    get_chain_of_thought_prompt,
    get_persona_prompt,
    get_role_specific_prompt,
)
from utils import get_openai_api_key, call_openai, moderate_input

# Initialize
st.set_page_config(page_title="AI Interview Trainer", layout="wide")
st.title("🧠 AI Interview Preparation Tool")


# Sidebar options
st.sidebar.header("🛠️ Configuration")
role = st.sidebar.selectbox("Choose Interview Role", ["Frontend Developer", "Data Scientist", "Product Manager", "UX Designer"])
level = st.sidebar.radio("Experience Level", ["Junior", "Mid", "Senior"])
prompt_style = st.sidebar.selectbox("Prompt Style", [
    "Zero-shot",
    "Few-shot",
    "Chain-of-thought",
    "Persona Interview",
    "Role-specific"
])
temperature = st.sidebar.slider("Creativity Level (temperature)", 0.0, 1.0, 0.7)

# Chat UI
st.subheader(f"💬 Interview for a {level} {role}")
chat_history = st.session_state.get('history', [])

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

# Prompt selector
if prompt_style == "Zero-shot":
    st.session_state.current_prompt = get_zero_shot_prompt(role, level)
elif prompt_style == "Few-shot":
    st.session_state.current_prompt = get_few_shot_prompt(role, level)
elif prompt_style == "Chain-of-thought":
    st.session_state.current_prompt = get_chain_of_thought_prompt(role, level)
elif prompt_style == "Persona Interview":
    st.session_state.current_prompt = get_persona_prompt(role)
elif prompt_style == "Role-specific":
    st.session_state.current_prompt = get_role_specific_prompt(role, level)

# Start with an initial question
if len(chat_history) == 0:
    chat_history.append({"role": "ai", "message": "Welcome to your mock interview. Let's begin!\n\nFirst question: Tell me about yourself."})

# Show chat
for entry in chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["message"])

# User input
if user_input := st.chat_input("Answer here..."):
    # Check for prompt injection
    if moderate_input(user_input):
        st.error("⚠️ Inappropriate input detected. Please try again with a valid answer.")
    else:
        chat_history.append({"role": "user", "message": user_input})

        # Get AI reply
        with st.spinner("Analyzing your answer..."):
            ai_response = call_openai(st.session_state.current_prompt, user_input, temperature)
        chat_history.append({"role": "ai", "message": ai_response})

        st.session_state.history = chat_history
        st.rerun()

