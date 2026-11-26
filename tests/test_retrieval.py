def test_retrieval_function_exists():
    from src.retrieval import retrieve_context

    assert callable(retrieve_context)
    
def test_dataset_path_exists():
    from pathlib import Path
    from src.retrieval import DATA_PATH

    assert isinstance(DATA_PATH, Path)
    assert DATA_PATH.exists()


def test_retrieve_context_returns_top_three_results():
    from src.retrieval import retrieve_context

    context = retrieve_context("What is phishing?", top_k=3)

    assert context != ""
    assert context.count("Question:") == 3
    assert context.count("Answer:") == 3


def test_retrieve_context_matches_password_query():
    from src.retrieval import retrieve_context

    context = retrieve_context(
        "My password is 12345678, is it safe?",
        top_k=3
    )

    assert "password" in context.lower()
    