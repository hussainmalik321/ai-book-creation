FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire application first to ensure directory structure
COPY . .

# Install Python dependencies from the backend directory
WORKDIR /app/backend
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run the application from backend directory on port 7860 (Hugging Face default)
CMD ["sh", "-c", "cd /app/backend && uvicorn main:app --host 0.0.0.0 --port 7860"]