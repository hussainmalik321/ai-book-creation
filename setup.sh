#!/bin/bash
# Setup script for AI-Powered Book Assistant

echo "AI-Powered Book Assistant Setup"

# Check if running in Hugging Face environment
if [ -n "$SPACE_ID" ]; then
    echo "Running in Hugging Face Space environment"
    echo "Environment: Hugging Face Spaces"
else
    echo "Running in local environment"
fi

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Check if environment variables are set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Warning: GEMINI_API_KEY environment variable not set"
fi

if [ -z "$QDRANT_URL" ]; then
    echo "Warning: QDRANT_URL environment variable not set"
fi

if [ -z "$QDRANT_API_KEY" ]; then
    echo "Warning: QDRANT_API_KEY environment variable not set"
fi

echo "Setup complete!"
echo "Backend ready to run on port $PORT (default: 7860)"