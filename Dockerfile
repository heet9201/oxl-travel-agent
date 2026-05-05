# Use Python slim as base image
FROM python:3.12-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install frontend dependencies
COPY frontend/package.json frontend/package-lock.json frontend/
RUN cd frontend && npm install

# Copy all source code
COPY . .

# Set environment variable so Next.js uses relative URL for API calls
ENV NEXT_PUBLIC_API_URL=/api

# Build frontend
RUN cd frontend && npm run build

# Make start script executable
RUN chmod +x start.sh

# Start both frontend and backend
CMD ["./start.sh"]
