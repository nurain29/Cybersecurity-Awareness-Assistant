def test_chatbot_function_exists():
    from src.chatbot import get_chatbot_response

    assert callable(get_chatbot_response)