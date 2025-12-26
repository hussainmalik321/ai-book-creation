FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend directory
COPY backend/ ./backend/

# Copy root level files if they exist
COPY main.py . 2>/dev/null || true
COPY .env.example . 2>/dev/null || true

# Expose port
EXPOSE 7860

# Run the application - try backend/main.py first, fallback to root main.py
CMD ["sh", "-c", "if [ -f backend/main.py ]; then cd backend && uvicorn main:app --host 0.0.0.0 --port 7860; else uvicorn main:app --host 0.0.0.0 --port 7860; fi"]# Force update
