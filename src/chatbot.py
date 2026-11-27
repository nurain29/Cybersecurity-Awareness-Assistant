
from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.retrieval import retrieve_context


MODEL_NAME = "gemini-3.5-flash-lite"
TEMPERATURE = 0.3
MAX_OUTPUT_TOKENS = 400


if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Check your .env file.")


client = genai.Client(api_key=GEMINI_API_KEY)


SYSTEM_INSTRUCTION = """
You are CyberSafe Assistant, a cybersecurity awareness assistant.

Your role is to help users understand cybersecurity topics such as:
- phishing and suspicious links
- online scams
- passwords and password safety
- MFA / 2FA
- malware
- social engineering
- Wi-Fi security
- privacy
- device security

Answer in the same language used by the user.
You may respond in English, Bahasa Melayu, or Manglish.

Use the retrieved FAQ context as your main source of information.
Give clear, practical and simple cybersecurity awareness advice.

If the user is stressed, worried, angry, or says their account may have
been hacked, respond calmly and empathetically and provide safe next steps.

Never ask users for their real password, OTP, IC number, banking PIN,
or other sensitive personal information.

Never provide instructions for hacking, cyberattacks, bypassing security,
stealing credentials, or harming another system.

If the question is outside cybersecurity awareness, politely say:
"Outside my domain. I can only help with cybersecurity awareness questions."

For Bahasa Melayu:
"Di luar skop saya. Saya hanya boleh membantu dengan soalan kesedaran
keselamatan siber."

Answer based on the retrieved context whenever possible.
"""


def _create_chat():
    return client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )


chat = _create_chat()


def reset_chat():
    """
    Reset the Gemini conversation and start a fresh chat.
    """
    global chat
    chat = _create_chat()


def get_chatbot_response(user_question):
    """
    Retrieve relevant FAQ context and generate a cybersecurity response.
    """

    if not user_question or not user_question.strip():
        return "Please enter a cybersecurity question."

    # Retrieve relevant information
    context = retrieve_context(user_question, top_k=3)

    # Prepare prompt
    prompt = f"""
    Retrieved FAQ Context:
    {context}

    User Question:
    {user_question}

    Instructions:
    1. Check whether the retrieved FAQ context is relevant.
    2. If relevant, use the FAQ information as the primary source.
    3. If the FAQ context is insufficient or irrelevant,
       use your general cybersecurity knowledge.
    4. If the question is unrelated to cybersecurity,
       politely reject it.
    5. Answer in the same language used by the user.
    """

    # Generate response
    try:
        response = chat.send_message(prompt)
        return response.text

    except (genai.errors.APIError, ConnectionError, TimeoutError):
        # Let the Streamlit application handle the service error.
        raise
