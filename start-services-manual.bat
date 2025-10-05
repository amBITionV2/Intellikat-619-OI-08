@echo off
echo Starting JOBPLEXITY Backend Services Manually...

echo.
echo Step 1: Starting Resume Analyzer Service...
cd backend-resume-anaalyser
echo API_KEY=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 > .env
start "Resume Analyzer" cmd /k "python main.py"

echo.
echo Step 2: Starting Resume Builder Service...
cd ..\backend-tailured-resume-builder
echo OPENROUTER_API_KEY=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 > .env
start "Resume Builder" cmd /k "python app.py"

echo.
echo Step 3: Starting Frontend...
cd ..\front-end
start "Frontend" cmd /k "npm run dev"

echo.
echo All services are starting...
echo Resume Analyzer: http://localhost:5001
echo Resume Builder: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Wait for all services to start, then test the resume extraction!
pause
