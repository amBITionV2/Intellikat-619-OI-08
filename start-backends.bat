@echo off
echo Starting JOBPLEXITY Backend Services...

echo.
echo Starting Resume Analyzer Service (Port 5001)...
start "Resume Analyzer" cmd /k "cd /d %~dp0backend-resume-anaalyser & python -m pip install -r requirements.txt & python main.py"

echo.
echo Starting Resume Builder Service (Port 5000)...
start "Resume Builder" cmd /k "cd /d %~dp0backend-tailured-resume-builder & python -m pip install -r requirements.txt & python app.py"

echo.
echo Both backend services are starting...
echo Resume Analyzer: http://localhost:5001
echo Resume Builder: http://localhost:5000
echo.
echo Press any key to continue...
pause > nul
