from dotenv import load_dotenv
load_dotenv()  # load all the environment variables from .env

import google.generativeai as genai
import streamlit as st

# Configure Streamlit App Title
st.title("Jagunmólú Chat Bot")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Session State for Messages and Model
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-1.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle New User Input
if prompt := st.chat_input("What is up?"):
    # Save User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Assistant Response
    with st.chat_message("assistant"):
        try:

            response = model.generate_content(prompt)

            st.markdown(response.text)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
