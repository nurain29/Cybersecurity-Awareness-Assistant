# Cybersecurity Awareness Assistant

A domain-specific chatbot that provides cybersecurity awareness information using Retrieval-Augmented Generation (RAG), a language model (LLM), and a Streamlit web interface.

## Project Overview

The Cybersecurity Awareness Assistant is designed to help users learn about common cybersecurity topics through an interactive chatbot.

The system combines:
- A Streamlit-based chatbot interface
- A cybersecurity-focused backend
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers for semantic processing
- Google Gemini for natural-language responses

## Main Features

- Interactive cybersecurity chatbot
- Cybersecurity awareness guidance
- AI-generated responses using Google Gemini
- RAG-based information retrieval
- Suggested cybersecurity questions
- Conversation history within the session
- Input validation for empty questions
- Streamlit web interface

## Example Questions

Users can ask questions such as:

- What is phishing?
- What is malware?
- Why should I use multi-factor authentication?
- How can I create a strong password?
- Is public Wi-Fi safe?


## Domain & Dataset

### Domain
The project focuses on cybersecurity awareness and online safety. It provides information about common cybersecurity threats, account protection, and safe online practices.

### Dataset
The system uses a custom cybersecurity FAQ dataset containing 40 question-and-answer pairs across 8 cybersecurity categories.

The FAQ dataset is stored in:
- `data/cybersecurity_faq.csv`

The dataset sources and references are documented in:
- [Data Sources](data/data_sources.md)


## Team Members

| No. |              Name            | Student ID |        Role        |   Username   |
|-----|------------------------------|------------|--------------------|--------------|
|  1  | Nurain Batrisyia binti Azman | 2024642036 |   Project Leader   |   nurain29   |
|  2  |       Syarifah Syahirah      | 2024224602 | Backend Developer  |  syasya-xd   |
|  3  | 'Aina Qistina binti Asqolani | 2024208608 | Frontend Developer |  ainaqiss13  | 
|  4  | Nurul Dayana binti Marzuki   | 2024426964 | Domain Specialist  |   dyanaazu   |


## System Architecture

The system uses Retrieval-Augmented Generation (RAG) to provide cybersecurity awareness responses.

The architecture consists of:
- Streamlit frontend for user interaction.
- Python backend for chatbot processing.
- Sentence Transformers for text embedding.
- Semantic Search to retrieve the Top 3 relevant FAQ entries.
- Google Gemini API to generate responses.

For more details, refer to:
- [System Architecture Documentation](docs/architecture.md)
- [System Architecture Diagram](docs/architecture-diagram.md)


## Model & Parameters

### Language Model (LLM)
- Model: Gemini 3.5 Flash Lite
- Provider: Google Gemini API
- Purpose: Generate natural-language cybersecurity awareness responses.

### Embedding Model
- Model: `all-MiniLM-L6-v2`
- Library: Sentence Transformers
- Purpose: Convert FAQ questions and user queries into embeddings for semantic similarity search.

### Retrieval Parameters
- Retrieval method: Semantic Search
- Top-K: 3
- Dataset: 40 cybersecurity FAQ question-and-answer pairs
- Similarity search: Retrieve the three FAQ entries with the highest semantic similarity to the user's question.

### Response Generation
The retrieved FAQ context is provided to the Gemini model as part of the prompt. The chatbot uses relevant FAQ information as its primary source and may use general cybersecurity knowledge when the retrieved context is insufficient.


## Demo

### Demo Video
[Watch the Cybersecurity Awareness Assistant Demo](PASTE_DEMO_VIDEO_LINK_HERE)

### Application Screenshots

#### Chatbot Interface
![Cybersecurity Awareness Assistant chatbot interface](docs/screenshots/chatbot-interface.png)

#### Chatbot Response
![Example cybersecurity awareness response](docs/screenshots/chatbot-response.png)


## Limitations

The Cybersecurity Awareness Assistant has the following limitations:

- The chatbot requires an active internet connection to communicate with the Google Gemini API.
- Response generation depends on the availability and usage limits of the Gemini API.
- The quality of retrieved information depends on the content and coverage of the FAQ dataset.
- The system retrieves only the Top 3 FAQ entries during semantic search.
- The chatbot may generate inaccurate or incomplete information when using general cybersecurity knowledge.
- The system is designed for cybersecurity awareness and educational purposes, not as a replacement for professional cybersecurity services.
- The application does not automatically detect, investigate, or resolve real cybersecurity incidents.


## Generative AI Use (Tahap 3)

This project uses Generative AI as part of its chatbot functionality and development process.

### Generative AI Tools
- **Google Gemini API:** Used to generate natural-language responses to users' cybersecurity questions.
- **ChatGPT:** Used as an assistance tool for brainstorming, code guidance, debugging, and documentation improvement.

### How Generative AI Is Used
- Generates cybersecurity awareness responses based on retrieved FAQ information.
- Provides general cybersecurity knowledge when the retrieved FAQ context is insufficient.
- Assists with improving the clarity and readability of project documentation.

### Human Verification
All AI-assisted outputs and generated responses should be reviewed and tested by the project team. The team remains responsible for the accuracy, safety, and quality of the final system.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nurain29/Cybersecurity-Awareness-Assistant.git
```

### 2. Navigate to the Project Folder

```bash
cd Cybersecurity-Awareness-Assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API Key

Create a `.env` file in the project root directory and add:

```env
GEMINI_API_KEY=your_api_key_here
```

### 7. Run the Application

```bash
python -m streamlit run app/app.py
```

The application will open in your browser at:

http://localhost:8501


## Requirements

The project requires the following:

- Python 3.10 or later
- Streamlit
- Google GenAI SDK
- Sentence Transformers
- PyTorch
- Pandas
- Python-dotenv

All required Python packages are listed in `requirements.txt`.

## Project Structure

```text
Cybersecurity-Awareness-Assistant/
│
├── app/
│   └── app.py
│
├── data/
│   └── cybersecurity_faq.csv
│
├── docs/
│   ├── architecture.md
│   └── architecture-diagram.md
│
├── src/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── config.py
│   └── retrieval.py
│
├── tests/
│   ├── test_chatbot.py
│   └── test_retrieval.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Testing

The project includes automated tests using Pytest to verify the chatbot and retrieval functionality.

To run the tests, use:

```bash
python -m pytest tests/ -v
```

The tests cover:
- Chatbot function availability.
- Retrieval function availability.
- Retrieval of the Top 3 relevant FAQ entries.

### Test Results

The backend automated tests achieved:

**3 passed**

Note: These results represent automated backend tests. Actual chatbot response quality is evaluated separately through manual testing.
