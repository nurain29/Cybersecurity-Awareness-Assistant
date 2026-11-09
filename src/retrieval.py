
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load cybersecurity dataset
df = pd.read_csv("data/cybersecurity_faq.csv")

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Convert dataset questions into embeddings
question_embeddings = embedder.encode(
    df["Question"].tolist(),
    convert_to_tensor=True
)

def retrieve_context(user_question, top_k=3):

    # Convert user question into embedding
    user_embedding = embedder.encode(
        user_question,
        convert_to_tensor=True
    )

    # Find the most similar questions
    hits = util.semantic_search(
        user_embedding,
        question_embeddings,
        top_k=top_k
    )[0]

    # Retrieve matching questions and answers
    results = df.iloc[[hit["corpus_id"] for hit in hits]]

    # Prepare context for chatbot
    context = ""

    for _, row in results.iterrows():
        context += f"Question: {row['Question']}\n"
        context += f"Answer: {row['Answer']}\n\n"

    return context
