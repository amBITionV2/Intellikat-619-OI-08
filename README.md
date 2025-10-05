# JobPlexity - AI-Powered Resume Builder & Job Matcher

JobPlexity is a comprehensive platform that helps job seekers create tailored resumes and find matching job opportunities using AI technology.

## Features

- **Resume Analysis**: Upload your resume and extract structured data using AI
- **Tailored Resume Generation**: Generate job-specific resumes using AI tailoring
- **Job Matching**: Find relevant job opportunities based on your profile
- **Interview Preparation**: Get AI-powered interview questions and feedback
- **Real-time Application Tracking**: Track your job applications

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Shadcn/ui components
- React Router for navigation

### Backend
- Flask (Python) for API services
- OpenRouter API for AI processing
- ReportLab for PDF generation
- PyPDF2 for PDF text extraction

## Project Structure

```
JOBPLEXITY-5/
├── front-end/                    # React frontend application
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/              # Application pages
│   │   ├── services/           # API service layer
│   │   ├── utils/              # Utility functions
│   │   └── contexts/           # React contexts
│   └── package.json
├── backend-resume-anaalyser/    # Resume analysis service
│   ├── main.py                 # Flask application
│   ├── requirements.txt        # Python dependencies
│   └── env.example            # Environment variables template
├── backend-tailured-resume-builder/ # Resume generation service
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   └── env.example           # Environment variables template
└── README.md
```

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- OpenRouter API key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd JOBPLEXITY-5
```

### 2. Backend Setup

#### Resume Analyzer Service

```bash
cd backend-resume-anaalyser
pip install -r requirements.txt
cp env.example .env
# Edit .env and add your OpenRouter API key
python main.py
```

#### Resume Builder Service

```bash
cd backend-tailured-resume-builder
pip install -r requirements.txt
cp env.example .env
# Edit .env and add your OpenRouter API key
python app.py
```

### 3. Frontend Setup

```bash
cd front-end
npm install
npm run dev
```

### 4. Environment Variables

Create `.env` files in both backend directories with your OpenRouter API key:

```bash
# backend-resume-anaalyser/.env
API_KEY=your_openrouter_api_key_here

# backend-tailured-resume-builder/.env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## API Endpoints

### Resume Analyzer (Port 5001)

- `GET /health` - Health check
- `POST /upload` - Upload and analyze resume PDF

### Resume Builder (Port 5000)

- `GET /health` - Health check
- `POST /upload` - Upload resume data
- `POST /generate` - Generate tailored resume PDF

## Usage

1. **Upload Resume**: Upload your resume PDF to extract structured data
2. **Generate Tailored Resume**: Provide job details to generate a customized resume
3. **Download PDF**: Download the generated resume as a PDF file

## Development

### Running in Development Mode

Use the provided scripts to start all services:

**Windows:**
```bash
start-backends.bat
```

**Linux/Mac:**
```bash
./start-backends.sh
```

### Building for Production

**Frontend:**
```bash
cd front-end
npm run build
```

**Backend:**
The Python services are ready for production deployment with proper WSGI servers like Gunicorn.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.