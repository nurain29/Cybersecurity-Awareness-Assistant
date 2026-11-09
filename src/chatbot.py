
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
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="""
        You are a Cybersecurity Awareness Assistant.

        Your role is to provide cybersecurity awareness
        information to users.

        Answer using only the information provided
        in the retrieved context.

        If the answer is not available in the context,
        politely say that you do not have enough
        information to answer.

        Do not answer unrelated questions.
        Use simple and clear language.
        """
    )
)

def get_chatbot_response(user_question):

    # Retrieve relevant information
    context = retrieve_context(user_question)

    # Prepare prompt
    prompt = f"""
    Retrieved Context:
    {context}

    User Question:
    {user_question}

    Answer based on the retrieved context only.
    """

    # Generate response
    response = chat.send_message(prompt)

    return response.text
