def test_retrieval_function_exists():
    from src.retrieval import retrieve_context

    assert callable(retrieve_context)