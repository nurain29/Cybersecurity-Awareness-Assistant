import os
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

os.environ.setdefault("GEMINI_API_KEY", "test-key")

import src.chatbot as chatbot_module
from src.chatbot import (
    MAX_OUTPUT_TOKENS,
    MODEL_NAME,
    SYSTEM_INSTRUCTION,
    TEMPERATURE,
    _is_cybersecurity_question,
    get_chatbot_response,
    reset_chat,
)
from src.retrieval import DATA_PATH


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


def test_domain_check_accepts_english_cybersecurity_questions():
    assert _is_cybersecurity_question("What is phishing and how can I recognize it?")
    assert _is_cybersecurity_question("Is it safe to use the same password for all my accounts?")
    assert _is_cybersecurity_question("What should I do if I accidentally clicked a phishing link?")
    assert _is_cybersecurity_question("I'm really scared. I think someone hacked my account. What should I do?")


def test_domain_check_accepts_bahasa_melayu_questions():
    assert _is_cybersecurity_question("Apa itu phishing dan bagaimana saya boleh mengenal pasti mesej phishing?")
    assert _is_cybersecurity_question("Bagaimana cara buat kata laluan yang kuat?")
    assert _is_cybersecurity_question("Apa itu keselamatan siber dan privasi?")


def test_domain_check_accepts_manglish_questions():
    assert _is_cybersecurity_question("Macam mana nak buat password yang lebih secure?")
    assert _is_cybersecurity_question("Password saya 12345678, selamat tak?")
    assert _is_cybersecurity_question("Kalau terklik link scam macam mana?")
    assert _is_cybersecurity_question("Akaun kena hack, nak buat apa?")


def test_domain_check_rejects_unrelated_questions():
    assert not _is_cybersecurity_question("Can you help me calculate my monthly loan payment?")
    assert not _is_cybersecurity_question("Give me a nasi lemak recipe")
    assert not _is_cybersecurity_question("What is the weather in Kuala Lumpur today?")
    assert not _is_cybersecurity_question("Recommend me a good action movie")


def test_domain_check_covers_all_faq_questions():
    df = pd.read_csv(DATA_PATH)
    missed = [q for q in df["Question"].tolist() if not _is_cybersecurity_question(q)]
    assert missed == [], f"FAQ questions rejected by domain check: {missed}"


def test_out_of_domain_question_returns_deterministic_reply_without_calling_llm():
    with patch.object(chatbot_module.chat, "send_message") as mock_send:
        reply = get_chatbot_response("Can you help me calculate my monthly loan payment?")
        assert "outside my domain" in reply.lower()
        mock_send.assert_not_called()


def test_system_instruction_does_not_delegate_ood_classification_to_llm():
    assert "outside my domain" not in SYSTEM_INSTRUCTION.lower()
    assert "di luar skop" not in SYSTEM_INSTRUCTION.lower()


def test_reset_chat_replaces_active_session():
    fake_chat = MagicMock()
    with patch.object(chatbot_module, "_create_chat", return_value=fake_chat) as mock_create:
        reset_chat()
        mock_create.assert_called_once()
        assert chatbot_module.chat is fake_chat


def test_connection_error_propagates_for_ui_retry_handling():
    fake_chat = MagicMock()
    fake_chat.send_message.side_effect = ConnectionError("Network unreachable")
    with patch.object(chatbot_module, "chat", fake_chat):
        with pytest.raises(ConnectionError):
            get_chatbot_response("What is phishing?")
