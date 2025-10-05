# Tailored Resume Builder Service

This service generates customized resumes for specific job positions using AI.

## Features

- AI-powered resume tailoring
- Professional PDF generation using ReportLab
- Job-specific customization
- Base64 PDF output for web delivery

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
python app.py
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /upload` - Upload resume data
- `POST /generate` - Generate tailored resume PDF

## Environment Variables

- `OPENROUTER_API_KEY` - OpenRouter API key for AI processing

## Dependencies

- Flask - Web framework
- ReportLab - PDF generation
- requests - HTTP client
- python-dotenv - Environment variable management