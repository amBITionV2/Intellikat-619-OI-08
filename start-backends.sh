#!/bin/bash

echo "Starting JOBPLEXITY Backend Services..."

echo ""
echo "Starting Resume Analyzer Service (Port 5001)..."
cd backend-resume-anaalyser
pip install -r requirements.txt
python main.py &
ANALYZER_PID=$!

echo ""
echo "Starting Resume Builder Service (Port 5000)..."
cd ../backend-tailured-resume-builder
pip install -r requirements.txt
python app.py &
BUILDER_PID=$!

echo ""
echo "Both backend services are starting..."
echo "Resume Analyzer: http://localhost:5001"
echo "Resume Builder: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $ANALYZER_PID 2>/dev/null
    kill $BUILDER_PID 2>/dev/null
    exit
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
