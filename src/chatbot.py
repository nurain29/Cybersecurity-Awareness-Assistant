import re

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
You are CyberSafe Assistant, a friendly, calm, and empathetic Cybersecurity Awareness Assistant.

Every user question you receive has already been validated as a cybersecurity awareness topic.
Always answer the user's cybersecurity question directly and helpfully.

Your role is to help users understand cybersecurity topics such as:
- phishing, suspicious links, and online scams
- passwords, passphrases, and account security
- multi-factor authentication (MFA / 2FA) and OTP safety
- malware, viruses, spyware, ransomware, and antivirus limits
- social engineering and impersonation scams
- Wi-Fi security, HTTPS, VPN, and safe browsing
- personal data protection and digital privacy
- device, smartphone, and software update security

Rules:
1. Language: Reply in the same language and style used by the user — English, Bahasa Melayu, or Manglish (mixed English and Bahasa Melayu, including informal wording, slang, or typos).
2. Grounding: Prioritize the retrieved FAQ context when relevant. If a valid cybersecurity question is not directly covered in the FAQ, still give accurate, clear, and practical cybersecurity awareness advice.
3. Empathy: If the user sounds scared, stressed, worried, angry, or says their account may have been hacked or compromised, reassure them warmly and calmly first, then provide clear numbered recovery steps.
4. Safety:
   - Never ask users for their real password, OTP, IC number, banking PIN, or other sensitive personal information.
   - Never provide instructions for hacking, cyberattacks, stealing passwords or credentials, bypassing security, or harming another system. If a user asks how to hack someone or perform a cyberattack, politely refuse by stating you cannot assist with hacking or unauthorized access, and briefly suggest safe account protection practices instead.
   - Remind users when appropriate that this is educational cybersecurity awareness guidance, not professional legal or banking advice.
"""


# Word-boundary patterns for short acronyms to avoid accidental substring matches
_CYBER_ACRONYM_RE = re.compile(
    r"\b(mfa|2fa|otp|vpn|https|dns|dos|ddos|ic|pin)\b",
    re.IGNORECASE,
)

# Deterministic English, Bahasa Melayu, and Manglish cybersecurity terms
_CYBER_KEYWORDS = (
    # English — core cybersecurity & threats
    "cybersecurity",
    "cyber security",
    "cyberattack",
    "cyber attack",
    "cyber",
    "password",
    "passwords",
    "pasword",
    "passwrd",
    "passphrase",
    "phishing",
    "phish",
    "pishing",
    "scam",
    "scams",
    "scammer",
    "malware",
    "malwer",
    "virus",
    "antivirus",
    "anti-virus",
    "trojan",
    "spyware",
    "ransomware",
    "keylogger",
    "hack",
    "hacked",
    "hacking",
    "hacker",
    "account",
    "accounts",
    "multi-factor",
    "multifactor",
    "two-factor",
    "authenticator",
    "passkey",
    "one-time code",
    "social engineering",
    "impersonat",
    "remote-access",
    "remote access",
    "urgent money",
    "money transfer",
    "suspicious link",
    "suspicious email",
    "suspicious message",
    "phishing link",
    "scam link",
    "bad link",
    "fake link",
    "clicked a link",
    "clicked link",
    "click link",
    "privacy",
    "personal data",
    "personal information",
    "sensitive information",
    "identity theft",
    "identity card",
    "data breach",
    "breach",
    "online safety",
    "safe browsing",
    "wi-fi",
    "wifi",
    "hotspot",
    "padlock",
    "firewall",
    "security",
    "secure",
    "credential",
    "software update",
    "security update",
    "software updated",
    "update software",
    "update its software",
    "unknown websites",
    "unknown sources",
    "lock my computer",
    "lock computer",
    "screen lock",
    "sharing online",
    "share online",
    # Bahasa Melayu / Manglish
    "kata laluan",
    "kata password",
    "kata sandi",
    "akaun",
    "kena hack",
    "godam",
    "digodam",
    "penipuan",
    "penipu",
    "link scam",
    "pautan scam",
    "pautan mencurigakan",
    "pautan palsu",
    "pautan",
    "terklik",
    "klik link",
    "emel mencurigakan",
    "mesej mencurigakan",
    "keselamatan siber",
    "keselamatan internet",
    "keselamatan online",
    "keselamatan dalam talian",
    "siber",
    "privasi",
    "maklumat peribadi",
    "data peribadi",
    "kad pengenalan",
    "pengesahan dua faktor",
    "kod pengesahan",
    "kemas kini perisian",
    "kemaskini perisian",
    "kemas kini keselamatan",
    "perbankan dalam talian",
)


def _is_cybersecurity_question(user_question: str) -> bool:
    """
    Deterministically check whether a question is related to
    cybersecurity awareness.
    """
    question = user_question.lower().strip()
    if not question:
        return False

    if _CYBER_ACRONYM_RE.search(question):
        return True

    return any(keyword in question for keyword in _CYBER_KEYWORDS)


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
    This function can be connected to the Streamlit Clear button.
    """
    global chat
    chat = _create_chat()


def get_chatbot_response(user_question):
    """
    Retrieve relevant FAQ context and generate a cybersecurity response.
    """

    if not user_question or not user_question.strip():
        return "Please enter a cybersecurity question."

    if not _is_cybersecurity_question(user_question):
        return (
            "Outside my domain. I can only help with cybersecurity "
            "awareness questions."
        )

    context = retrieve_context(user_question, top_k=3)

    prompt = f"""Retrieved Cybersecurity FAQ Context:
{context}

User Question:
{user_question}

Answer the user's cybersecurity question directly using the retrieved FAQ context when relevant, or general cybersecurity awareness guidance if needed.
Match the user's language and style:
- English -> English
- Bahasa Melayu -> Bahasa Melayu
- Manglish -> natural Manglish

Keep the answer clear, concise, empathetic when needed, and practical."""

    try:
        response = chat.send_message(prompt)
        return response.text

    except (genai.errors.APIError, ConnectionError, TimeoutError):
        # Let the Streamlit application handle the service error.
        raise
