# Resume Analyzer Service

This service analyzes uploaded resume PDFs and extracts structured data using AI.

## Features

- PDF text extraction using PyPDF2
- AI-powered resume parsing with OpenRouter API
- Structured JSON output
- Error handling for various PDF formats

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp env.example .env
# Edit .env and add your OpenRouter API key
```

3. Run the service:
```bash
python main.py
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /upload` - Upload and analyze resume PDF

## Environment Variables

- `API_KEY` - OpenRouter API key for AI processing

## Dependencies

- Flask - Web framework
- PyPDF2 - PDF text extraction
- requests - HTTP client
- python-dotenv - Environment variable management