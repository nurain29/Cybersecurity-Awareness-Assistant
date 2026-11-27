
from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.retrieval import retrieve_context

# Check API key
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Check your .env file.")

# Connect to Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# Create chatbot
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction="""
        
You are a Cybersecurity Awareness Assistant.

ROLE:
- Provide cybersecurity awareness information.
- Focus on cybersecurity, online safety, digital privacy, scams, and security protection.

KNOWLEDGE:
- Use retrieved FAQ context as the primary source when relevant.
- If the FAQ context contains the answer, use it to answer the question.
- If the FAQ context is insufficient or irrelevant, use your general cybersecurity knowledge.
- Do not invent facts or provide misleading information.
- If you are unsure, explain that clearly.

LANGUAGE:
- Understand English, Bahasa Melayu, and mixed Malay-English (Manglish).
- Understand common informal words and spelling variations.
- Reply using the language used by the user.
- Use simple, friendly, and clear language.

SAFETY:
- Only answer questions related to cybersecurity and online safety.
- Politely reject unrelated questions.
- Provide defensive cybersecurity advice.
- Do not provide instructions for stealing passwords, spreading malware, or attacking systems.

Always provide helpful, accurate, and easy-to-understand answers.

        """
    )
)

def get_chatbot_response(user_question):

    # Retrieve relevant information
    context = retrieve_context(user_question)

    
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
    response = chat.send_message(prompt)

    return response.text


def reset_chat():
    global chat

    chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction="""
You are a Cybersecurity Awareness Assistant.

ROLE:
- Provide cybersecurity awareness information.
- Focus on cybersecurity, online safety, digital privacy, scams, and security protection.

KNOWLEDGE:
- Use retrieved FAQ context as the primary source when relevant.
- If the FAQ context is insufficient or irrelevant, use your general cybersecurity knowledge.
- Do not invent facts or provide misleading information.
- If unsure, explain clearly.

LANGUAGE:
- Understand English, Bahasa Melayu, and Manglish.
- Reply using the language used by the user.
- Use simple, friendly, and clear language.

SAFETY:
- Only answer questions related to cybersecurity and online safety.
- Politely reject unrelated questions.
- Provide defensive cybersecurity advice only.
"""
        )
    )

