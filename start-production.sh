#!/bin/bash

echo "Starting JobPlexity Production Services..."
echo

echo "Starting Resume Analyzer Service (Port 5001)..."
cd backend-resume-anaalyser
python main.py &
ANALYZER_PID=$!

sleep 3

echo "Starting Resume Builder Service (Port 5000)..."
cd ../backend-tailured-resume-builder
python app.py &
BUILDER_PID=$!

sleep 3

echo "Starting Frontend Development Server (Port 5173)..."
cd ../front-end
npm run dev &
FRONTEND_PID=$!

echo
echo "All services started successfully!"
echo
echo "Resume Analyzer: http://localhost:5001"
echo "Resume Builder: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill $ANALYZER_PID 2>/dev/null
    kill $BUILDER_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for user to stop
wait
