# Quickstart Guide: AI-Powered Book Assistant

## Development Environment Setup

### Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend/

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn openai qdrant-client psycopg2-binary python-dotenv

# Set environment variables
export OPENAI_API_KEY="your-key-here"
export QDRANT_URL="your-qdrant-url"
export DATABASE_URL="your-postgres-url"

# Run the server
uvicorn src.main:app --reload
```

### Frontend (React Component)
```bash
# Navigate to frontend directory
cd frontend/

# Install dependencies
npm install react react-dom

# Run development server
npm start
```

## API Integration

### Basic Query
```javascript
// General book question
const response = await fetch('/api/chat/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query_text: 'What does this book say about AI?',
    query_type: 'GLOBAL_QA',
    session_id: 'session-123'
  })
});
```

### Selection-Based Query
```javascript
// Question about selected text
const response = await fetch('/api/chat/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query_text: 'Explain this concept in detail',
    query_type: 'SELECTION_QA',
    selected_text: 'The concept of retrieval-augmented generation...',
    session_id: 'session-123'
  })
});
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for generation
- `QDRANT_URL`: Qdrant vector database connection URL
- `QDRANT_API_KEY`: Qdrant API key (if required)
- `DATABASE_URL`: Neon Postgres connection string
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins

### Key Settings
- Response timeout: 3 seconds (from spec)
- Rate limiting: 100 requests/hour
- Maximum query length: 10KB

## Testing

### Backend Tests
```bash
cd backend/
pytest tests/
```

### Frontend Tests
```bash
cd frontend/
npm test
```