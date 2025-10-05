@echo off
echo Starting JobPlexity Production Services...
echo.

echo Starting Resume Analyzer Service (Port 5001)...
start "Resume Analyzer" cmd /k "cd backend-resume-anaalyser && python main.py"

timeout 3

echo Starting Resume Builder Service (Port 5000)...
start "Resume Builder" cmd /k "cd backend-tailured-resume-builder && python app.py"

timeout 3

echo Starting Frontend Development Server (Port 5173)...
start "Frontend" cmd /k "cd front-end && npm run dev"

echo.
echo All services started successfully!
echo.
echo Resume Analyzer: http://localhost:5001
echo Resume Builder: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit...
pause > nul
