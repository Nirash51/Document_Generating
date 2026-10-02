# LegalEase

LegalEase is an AI-powered legal document drafting application.

## Technologies

- Python
- FastAPI
- Streamlit
- Google Gemini
- Pydantic
- python-docx
- fpdf2
- Requests

## Features

- Employment contracts
- NDA generation
- Lease agreements
- Freelance contracts
- Service agreements
- Editable generated documents
- TXT export
- DOCX export
- PDF export
- Terms table
- FastAPI REST API
- Gemini AI integration
- API documentation
- Automated tests

## Installation

Create virtual environment:

Windows:

python -m venv .venv

Activate:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Environment

Create `.env`.

Example:

GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000

## Start backend

uvicorn backend.main:app --reload --port 8000

## Start frontend

streamlit run frontend/app.py

## Backend

http://127.0.0.1:8000

## Swagger

http://127.0.0.1:8000/docs

## Frontend

http://localhost:8501

## Testing

pytest -q

## Workflow

User
    |
    v
Streamlit
    |
    v
FastAPI
    |
    v
Gemini
    |
    v
Generated Legal Draft
    |
    +------> Edit
    |
    +------> TXT
    |
    +------> DOCX
    |
    +------> PDF

## Disclaimer

LegalEase provides AI-assisted drafting and does not constitute legal advice.
Generated documents should be reviewed by a qualified legal professional before use.