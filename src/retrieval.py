import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load cybersecurity dataset
df = pd.read_csv("data/cybersecurity_faq.csv")

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Convert dataset questions into embeddings
question_embeddings = embedder.encode(
    df["Question"].tolist(),
    convert_to_tensor=True,
    normalize_embeddings=True
)

def retrieve_context(user_question, top_k=3):

    # Convert user question into embedding
    user_embedding = embedder.encode(
        user_question,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    # Find the most similar questions
    scores = util.dot_score(
        user_embedding,
        question_embeddings
    )[0]

    top_results = scores.topk(k=min(top_k, len(question_embeddings)))

    hits = [
        {"corpus_id": idx.item(), "score": score.item()}
        for score, idx in zip(top_results.values, top_results.indices)
    ]

    # Retrieve matching questions and answers
    results = df.iloc[[hit["corpus_id"] for hit in hits]]

    # Prepare context for chatbot
    context = ""

    for _, row in results.iterrows():
        context += f"Question: {row['Question']}\n"
        context += f"Answer: {row['Answer']}\n\n"

    return context
