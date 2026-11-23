
# System Architecture

## 1. Project Overview

The Cybersecurity Awareness Assistant is a domain-specific chatbot designed to provide users with cybersecurity awareness information. The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from a custom cybersecurity FAQ dataset before generating responses using the Gemini API.

## 2. System Architecture Flow

The system follows this process:

1. User enters a cybersecurity-related question through the Streamlit interface.
2. The frontend sends the question to the backend.
3. The backend passes the question to the retrieval module.
4. The retrieval module uses Sentence Transformers to convert the question into an embedding.
5. Semantic search identifies the most relevant questions and answers from the cybersecurity FAQ dataset.
6. The retrieved information is passed to the Gemini API as context.
7. Gemini generates a response based on the retrieved context.
8. The response is returned to the Streamlit interface and displayed to the user.

## 3. Main System Components

| Component | Description |
|---|---|
| Streamlit Frontend | Provides the chatbot user interface. |
| Backend | Handles chatbot processing and connects the frontend with the retrieval and Gemini modules. |
| Cybersecurity FAQ Dataset | Stores cybersecurity questions and answers in CSV format. |
| Sentence Transformers | Converts questions into embeddings for semantic search. |
| Semantic Search | Retrieves the most relevant FAQ entries. |
| Gemini API | Generates natural language responses using retrieved context. |

## 4. Technologies Used

- Programming Language: Python
- Frontend Framework: Streamlit
- Language Model: Google Gemini API
- Retrieval Method: Semantic Search
- Embedding Model: all-MiniLM-L6-v2
- Data Format: CSV
- Version Control: GitHub

## 5. System Architecture Summary

The system combines a custom cybersecurity FAQ dataset, semantic search, and the Gemini API to provide relevant cybersecurity awareness responses. The RAG approach helps ground chatbot responses in the information retrieved from the dataset.
