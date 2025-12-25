# Backend Setup Guide

## Port Configuration

The backend runs on port 8001 instead of the default port 8000 due to conflicts with other services. If you need to run on port 8000, ensure no other services are using that port.

## Running the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the server:
   ```bash
   python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
   ```

## API Endpoints

- Root: `http://127.0.0.1:8001`
- Chat Session: `http://127.0.0.1:8001/api/chat/session`
- Chat Query: `http://127.0.0.1:8001/api/chat/query`

## Frontend Configuration

The frontend is already configured to use port 8001 for API calls.

## Troubleshooting

If you encounter "Address already in use" errors, make sure to:
1. Stop any other backend services that might be running
2. Use `npx kill-port 8001` to kill any processes using port 8001