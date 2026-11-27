
from pathlib import Path

import pandas as pd
from sentence_transformers import SentenceTransformer, util


# Safe absolute path to dataset
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cybersecurity_faq.csv"


# Load cybersecurity dataset
df = pd.read_csv(DATA_PATH)


# Load lightweight semantic embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)


# Pre-compute normalized FAQ question embeddings
question_embeddings = embedder.encode(
    df["Question"].tolist(),
    convert_to_tensor=True,
    normalize_embeddings=True,
)


def retrieve_context(user_question: str, top_k: int = 3) -> str:
    """Retrieve Top-K most semantically similar FAQ entries as formatted context."""

    # Convert user question into embedding
    user_embedding = embedder.encode(
        user_question,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    # Find the most similar questions using dot-product similarity
    scores = util.dot_score(user_embedding, question_embeddings)[0]

    top_results = scores.topk(
        k=min(top_k, len(question_embeddings))
    )

    hits = [
        {"corpus_id": idx.item(), "score": score.item()}
        for score, idx in zip(
            top_results.values,
            top_results.indices,
        )
    ]

    # Retrieve matching questions and answers
    results = df.iloc[
        [hit["corpus_id"] for hit in hits]
    ]

    # Prepare context for chatbot
    context = ""

    for _, row in results.iterrows():
        context += f"Question: {row['Question']}\n"
        context += f"Answer: {row['Answer']}\n\n"

    return context
