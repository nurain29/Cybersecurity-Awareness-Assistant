import os

os.environ.setdefault("GEMINI_API_KEY", "test-key")

from src.chatbot import (
    MAX_OUTPUT_TOKENS,
    MODEL_NAME,
    TEMPERATURE,
    get_chatbot_response,
    reset_chat,
)


def test_chatbot_function_exists():
    assert callable(get_chatbot_response)


def test_reset_chat_function_exists():
    assert callable(reset_chat)


def test_model_parameters_configured():
    assert MODEL_NAME == "gemini-3.5-flash-lite"
    assert 0.0 <= TEMPERATURE <= 1.0
    assert MAX_OUTPUT_TOKENS == 400


def test_empty_question_returns_prompt():
    reply = get_chatbot_response("   ")
    assert "question" in reply.lower()