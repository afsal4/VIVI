<div align="center">

# VIVI

### AI-Assisted Virtual Interview Platform

A Django-based interview prototype that helps organizations create job-specific interview sessions and invite candidates through a dedicated link.

</div>

---

## Overview

VIVI explores how AI can support the early stages of a hiring interview. A company provides its details and a job description, then candidates can access the associated interview flow. The application uses an OpenAI-powered language model to generate interview questions and text-to-speech to read questions aloud.

## Features

- **Company and job setup** – Register company details and provide the role description.
- **Candidate registration** – Associate candidate information with the relevant company.
- **Context-aware questions** – Generate interview questions using the job description as context.
- **Question narration** – Convert generated questions into speech with the OpenAI Text-to-Speech API.
- **Answer scoring utilities** – Includes LLM-based answer evaluation and question weighting logic.
- **Resume matching utility** – Includes code to compare a resume with a job description; this helper is not currently part of the web interview flow.

## Tech Stack

| Area | Technologies |
| --- | --- |
| Backend | Python, Django |
| AI integration | OpenAI API, LangChain |
| Audio | OpenAI Text-to-Speech, Whisper, PyAudio, Pydub |
| Database | SQLite, `cs50.SQL` |
| Frontend | HTML, CSS, JavaScript, Bootstrap |

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/afsal4/VIVI.git
cd VIVI
python -m venv .venv
```

Activate the environment, then install the project dependencies:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install Django==5.0.2 cs50 langchain langchain-openai langchain-community openai python-dotenv pydub pyaudio keyboard openai-whisper faiss-cpu scikit-learn
```

> **Audio dependency note:** PyAudio and Pydub may require system audio libraries, and Pydub requires FFmpeg. Install the relevant system packages for your operating system if setup fails.

### 2. Configure and run

Create a `.env` file in the project root and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

The current application also connects to a separate SQLite database through an absolute path defined in `home/views.py`. Update that path for your machine and ensure the database contains the `company`, `candidate`, and `qna` tables. Once the configuration is in place, apply the Django migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.

## Project Structure

```text
VIVI/
├── home/
│   ├── audio_transcription.py  # Audio recording and Whisper transcription helpers
│   ├── qna.py                  # Interview question and answer logic
│   ├── score.py                # Answer and resume scoring utilities
│   ├── text_to_speech.py       # OpenAI text-to-speech integration
│   ├── urls.py                 # Application routes
│   └── views.py                # Django views and database operations
├── project1/                   # Django project configuration
├── templates/                  # HTML templates
├── db.sqlite3
└── manage.py
```

## Development Notes

VIVI is currently a prototype; some supporting modules are not yet fully integrated into the browser-based interview flow:

- The browser recording control currently displays a placeholder alert.
- The interview answer handler uses sample text rather than passing recorded audio through the Whisper transcription helper.
- The resume-scoring helper is present but is not connected to the interview workflow.
- The separate SQLite database path and its expected tables need to be configured locally.

Before deploying beyond local development, move Django's secret key into environment configuration, disable `DEBUG`, configure `ALLOWED_HOSTS`, and review database access and API-key handling.

---

<div align="center">

**VIVI — Exploring AI-assisted interviews.**

</div>
