
from src.retrieval import retrieve_context


def test_retrieval_function_exists():
    assert callable(retrieve_context)


def test_retrieve_context_returns_top_three_results():
    context = retrieve_context("What is phishing?", top_k=3)

    assert context != ""
    assert context.count("Question:") == 3
    assert context.count("Answer:") == 3
