#!/bin/bash

# Start FastAPI backend in the background on port 8000
echo "Starting backend..."
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000 &

# Wait a moment to ensure backend starts
sleep 2

# Start Next.js frontend in the foreground
echo "Starting frontend..."
cd ./../frontend
# Render uses $PORT, if not set default to 3000
export PORT=${PORT:-3000}
npm start
