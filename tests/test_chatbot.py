import os

def test_chatbot_function_exists():
    os.environ["GEMINI_API_KEY"] = "test-key"

    from src.chatbot import get_chatbot_response

    assert callable(get_chatbot_response)
