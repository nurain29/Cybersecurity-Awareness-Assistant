# System Architecture

## 1. Project Overview

The Cybersecurity Awareness Assistant is a domain-specific chatbot designed to provide users with cybersecurity awareness information.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from a custom cybersecurity FAQ dataset before generating responses using the Google Gemini API.

The chatbot allows users to ask cybersecurity-related questions through a Streamlit web interface. It supports English, Bahasa Melayu, and mixed Malay-English (Manglish).

## 2. System Architecture Flow

The system follows these steps:

1. The user enters a cybersecurity-related question through the Streamlit interface.
2. The frontend sends the question to the chatbot backend.
3. The backend passes the question to the retrieval module.
4. The retrieval module uses Sentence Transformers to convert the question into an embedding.
5. Semantic search identifies the three most relevant questions and answers from the cybersecurity FAQ dataset.
6. The retrieved information is passed to the Gemini API as context.
7. Gemini generates a response using the retrieved FAQ information when relevant. If the FAQ does not contain the answer, Gemini can use its general cybersecurity knowledge.
8. The generated response is returned to the Streamlit interface.
9. The response is displayed to the user.

## 3. Main System Components

| Component | Description |
|---|---|
| Streamlit Frontend | Provides the chatbot user interface and allows users to submit questions and view responses. |
| Chatbot Backend | Handles chatbot processing, prepares prompts, and connects the retrieval module with the Gemini API. |
| Cybersecurity FAQ Dataset | Stores cybersecurity questions and answers in CSV format. |
| Retrieval Module | Processes user questions and retrieves relevant FAQ information. |
| Sentence Transformers | Converts text into embeddings for semantic processing. |
| Semantic Search | Identifies the three most relevant FAQ entries based on similarity. |
| Gemini API | Generates natural language responses using retrieved context or general cybersecurity knowledge when appropriate. |

## 4. Retrieval-Augmented Generation (RAG)

The system applies RAG to improve the relevance of chatbot responses.

The RAG process consists of:

1. Receiving the user's question.
2. Converting the question into an embedding using Sentence Transformers.
3. Comparing the question embedding with FAQ question embeddings.
4. Retrieving the Top 3 most relevant FAQ entries.
5. Combining the retrieved questions and answers into context.
6. Sending the context and user question to the Gemini API.
7. Generating a response based on the available context and cybersecurity knowledge.

This approach helps the chatbot provide responses supported by the custom cybersecurity FAQ dataset.

## 5. Chatbot Behaviour and Scope

The chatbot is designed to:

- Answer questions related to cybersecurity, online safety, digital privacy, scams, and security awareness.
- Understand English, Bahasa Melayu, and mixed Malay-English (Manglish).
- Provide simple and easy-to-understand explanations.
- Answer general cybersecurity questions even when the exact information is not available in the FAQ dataset.
- Provide practical cybersecurity protection advice.
- Politely reject questions unrelated to cybersecurity.
- Avoid providing harmful instructions related to cyberattacks, password theft, and malware distribution.

## 6. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming language. |
| Streamlit | Web-based chatbot interface. |
| Google Gemini API | Generates natural language responses. |
| Gemini 3.5 Flash Lite | Language model used by the chatbot. |
| Sentence Transformers | Generates text embeddings. |
| all-MiniLM-L6-v2 | Embedding model used for semantic processing. |
| Semantic Search | Retrieves relevant FAQ entries. |
| Pandas | Handles the cybersecurity FAQ dataset. |
| CSV | Stores cybersecurity questions and answers. |
| Pytest | Tests backend functionality. |
| GitHub | Version control and project collaboration. |

## 7. Dataset Description

The system uses a custom cybersecurity FAQ dataset stored in:

`data/cybersecurity_faq.csv`

The dataset contains 40 question-and-answer pairs across 8 cybersecurity categories.

The dataset is used as the knowledge source for the retrieval process. The retrieval module searches for relevant FAQ entries based on the user's question.

## 8. Testing

Automated backend testing is performed using Pytest.

The tests cover:

- Chatbot function availability.
- Retrieval function availability.
- Retrieval of the Top 3 relevant FAQ entries.

The latest recorded automated test result was:

**3 tests passed.**

Manual testing is also used to evaluate chatbot responses, language support, cybersecurity knowledge, and responses to unrelated questions.

## 9. System Architecture Summary

The Cybersecurity Awareness Assistant combines a Streamlit frontend, Python backend, custom cybersecurity FAQ dataset, Sentence Transformers, semantic search, and the Google Gemini API.

The RAG approach retrieves relevant FAQ information before generating responses. When the retrieved FAQ information is insufficient, the chatbot can use general cybersecurity knowledge to answer relevant questions.

Overall, the system aims to provide users with accessible, understandable, and useful cybersecurity awareness information through an interactive chatbot.