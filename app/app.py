import streamlit as st

st.set_page_config(page_title="Cybersecurity Awareness Assistant", page_icon="🛡️")

st.title("🛡️ Cybersecurity Awareness Assistant")
st.markdown("Ask questions about cybersecurity awareness, online safety, and account protection.")

st.markdown("---")
st.markdown("💡 Suggested Questions")
st.markdown("- What is phishing?")
st.markdown("- Why should I use multi-factor authentication (MFA)?")
st.markdown("- How do I create a strong password?")
st.markdown("- What is malware?")
st.markdown("---")

user_input = st.text_input("Ask your cybersecurity question...", placeholder="e.g., Is public Wi-Fi safe?")

if st.button("Ask"):
    if not user_input.strip():
        st.error("⚠️ Please enter a question before clicking Ask.")
    else:
        st.write(f"**You asked:** {user_input}")
        st.write("**Bot:** Backend connection is not ready yet. This is a placeholder response.")