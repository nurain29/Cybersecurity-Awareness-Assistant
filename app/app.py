import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Awareness Assistant",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for styling and colored chat bubbles
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
    
    /* Chat message bubbles */
    .stChatMessageContent {
        padding: 12px 16px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        max-width: 85%;
    }
    
    /* User message bubble (Light Blue) */
    .stChatMessage:has(img[alt="user"]) .stChatMessageContent {
        background-color: #bbdefb !important;
        border-radius: 15px 15px 0 15px;
    }
    
    /* Assistant message bubble (Light Green) */
    .stChatMessage:has(img[alt="assistant"]) .stChatMessageContent {
        background-color: #e8f5e9 !important;
        border-radius: 15px 15px 15px 0;
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
</style>
""", unsafe_allow_html=True)

# Title and Description
st.title("🛡️ Cybersecurity Awareness Assistant")
st.markdown("Ask questions about cybersecurity awareness, online safety, and account protection.")

# Initialize chat history in session state (This makes it persist!)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Suggested Questions Section
st.markdown("---")
st.markdown("💡 Suggested Questions")

# Create columns for suggested questions
col1, col2 = st.columns(2)

# Function to handle suggested question clicks
def handle_suggested_question(question):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    
    # Placeholder response (will be replaced by backend later)
    response = "🤖 Backend connection is not ready yet. This is a placeholder response."
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

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
            
            # 2. Get response (placeholder for now)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # This is where Syahirah's backend will go later
                    response = "🤖 Backend connection is not ready yet. This is a placeholder response."
                st.markdown(response)
            
            # 3. Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})