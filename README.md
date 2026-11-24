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

## Team Members

| No. |              Name            | Student ID |        Role        |
|-----|------------------------------|------------|--------------------|
|  1  | Nurain Batrisyia binti Azman | 2024642036 |   Project Leader   |
|  2  |       Syarifah Syahirah      | 2024224602 | Backend Developer  |
|  3  | 'Aina Qistina binti Asqolani | 2024208608 | Frontend Developer |
|  4  | Nurul Dayana binti Marzuki   | 2024426964 | Domain Specialist  |


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
