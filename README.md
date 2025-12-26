---
title: AI-Powered Book Assistant
emoji: 🤖
colorFrom: blue
colorTo: red
sdk: docker
sdk_version: "1.0.0"
app_file: app.py
pinned: false
---

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

## Environment Variables

The following environment variables are required:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key

## API Endpoints

- `POST /api/chat/query` - Submit a query to the AI assistant
- `POST /api/chat/session` - Create a new chat session
- `POST /api/content/ingest` - Ingest book content for indexing