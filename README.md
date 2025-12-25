# AI-Powered Book Assistant

An AI-powered chatbot that answers questions about book content using Retrieval-Augmented Generation (RAG).

## Features

- Q&A about book content
- Context-aware responses
- Source attribution
- Session management
- Integration with existing book platforms

## Tech Stack

- Backend: FastAPI
- Frontend: React
- Vector Database: Qdrant
- LLM: Google Gemini
- Deployment: Hugging Face Spaces

## Installation

1. Clone the repository
2. Navigate to the backend directory:
```bash
cd backend
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```bash
GEMINI_API_KEY=your_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

5. Start the backend:
```bash
uvicorn main:app --reload
```

## Environment Variables

The following environment variables are required:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key

## Deployment to Hugging Face Spaces

This project is configured for deployment to Hugging Face Spaces with Docker.

## API Endpoints

- `POST /api/chat/query` - Submit a query to the AI assistant
- `POST /api/chat/session` - Create a new chat session
- `POST /api/content/ingest` - Ingest book content for indexing

## License

[Specify your license here]