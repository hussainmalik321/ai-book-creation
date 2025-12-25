FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire application first
COPY . .

# Install Python dependencies
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# Expose port
EXPOSE 7860

# Run the application from backend directory
CMD ["sh", "-c", "cd /app/backend && uvicorn main:app --host 0.0.0.0 --port $PORT"]