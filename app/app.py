import streamlit as st
import sys
import os

# This tells Python to look in the main project folder for the 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Syarifah's backend function
from src.chatbot import get_chatbot_response

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Awareness Assistant",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS (Simplified to ensure history bubbles show up correctly)
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Title styling */
    h1 {
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }

    /* Clear Chat Button Styling */
    .clear-btn > button {
        background: #ff4b4b !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and Description
st.title("🛡️ Cybersecurity Awareness Assistant")
st.markdown("Ask questions about cybersecurity awareness, online safety, and account protection.")

# --- CHAT HISTORY MANAGEMENT ---

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear Chat Button (Top right)
if st.button("🗑️ Clear Chat", use_container_width=False):
    st.session_state.messages = []
    st.rerun()

# Display chat messages from history on app rerun (THIS IS THE HISTORY PART)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------

# Suggested Questions Section
st.markdown("---")
st.markdown("💡 Suggested Questions")

# Create columns for suggested questions
col1, col2 = st.columns(2)

# Function to handle suggested question clicks
def handle_suggested_question(question):
    # Add user question to history
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Display user question
    with st.chat_message("user"):
        st.markdown(question)
    
    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_chatbot_response(question)
            except Exception as e:
                response = f"⚠️ Sorry, an error occurred: {str(e)}"
        st.markdown(response)
        
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

with col1:
    if st.button("🎣 What is phishing?", use_container_width=True):
        handle_suggested_question("What is phishing?")

with col2:
    if st.button("🔐 Why use MFA?", use_container_width=True):
        handle_suggested_question("Why should I use multi-factor authentication (MFA)?")

with col1:
    if st.button("🔑 Strong password?", use_container_width=True):
        handle_suggested_question("How do I create a strong password?")

with col2:
    if st.button("🦠 What is malware?", use_container_width=True):
        handle_suggested_question("What is malware?")

st.markdown("---")

# Chat Input Form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask your cybersecurity question...",
        key="input",
        placeholder="e.g., Is public Wi-Fi safe?"
    )
    submitted = st.form_submit_button("Ask")
    
    if submitted:
        # Input Validation
        if not user_input.strip():
            st.error("⚠️ Please enter a question before clicking Ask.")
        else:
            # 1. Add user message to history and display it
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # 2. Get response from backend
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Call Syarifah's backend function
                        response = get_chatbot_response(user_input)
                    except Exception as e:
                        response = f"⚠️ Sorry, an error occurred: {str(e)}"
                
                st.markdown(response)
                
            # 3. Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})