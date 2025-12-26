FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY backend/requirements.txt /app/backend/requirements.txt

# Install Python dependencies
WORKDIR /app/backend
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
WORKDIR /app
COPY . .

# Expose port
EXPOSE 7860

# Run the application from backend directory
CMD ["sh", "-c", "cd /app/backend && uvicorn main:app --host 0.0.0.0 --port $PORT"]