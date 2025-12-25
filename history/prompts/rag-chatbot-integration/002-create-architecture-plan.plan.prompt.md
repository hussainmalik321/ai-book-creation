---
id: 002
title: create-architecture-plan
stage: plan
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot-integration
branch: 002-rag-chatbot-integration
user: Claude Code User
command: /sp.plan
labels: ["plan", "architecture", "ai", "chatbot", "backend", "frontend"]
links:
  spec: specs/002-rag-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-rag-chatbot-integration/plan.md
 - specs/002-rag-chatbot-integration/research.md
 - specs/002-rag-chatbot-integration/data-model.md
 - specs/002-rag-chatbot-integration/quickstart.md
 - specs/002-rag-chatbot-integration/contracts/chat-api.yaml
 - .specify/memory/constitution.md
tests:
 - No automated tests created yet
---

## Prompt

================================
SYSTEM ARCHITECTURE PLAN
================================

This plan translates the approved RAG chatbot specification into a concrete,
scalable, and production-ready architecture.

No code is written here.
No tasks are defined here.
This plan defines HOW the system will be structured.

================================
HIGH-LEVEL ARCHITECTURE
================================

The system consists of four major layers:

1. Frontend (Book + Chat UI)
2. Backend API (RAG Orchestration)
3. Retrieval Layer (Vector + Relational DB)
4. AI Agent Layer (OpenAI Agents / ChatKit)

All layers are decoupled and communicate via well-defined contracts.

================================
FRONTEND INTEGRATION PLAN
================================

Environment:
- Existing Docusaurus-based book (static site)
- Custom UI components only (no default widgets)

Frontend Responsibilities:
- Render embedded chatbot UI inside the book
- Allow users to:
  - Ask free-form questions about the book
  - Ask questions based ONLY on selected text
- Capture user-selected text context
- Send queries + optional selected text to backend API

Frontend Integration Strategy:
- Chat UI implemented as a reusable React component
- Component mounted globally (persistent chat)
- Also mountable per chapter or per page
- Selection-based queries triggered via contextual UI (e.g. tooltip or button)

No AI logic on frontend.
Frontend is a pure client.

================================
BACKEND ARCHITECTURE (FASTAPI)
================================

Framework:
- FastAPI (async, production-ready)

Backend Responsibilities:
- Accept chat requests from frontend
- Validate input and mode (global vs selected-text)
- Orchestrate retrieval + generation
- Enforce conffline
- Repeatable
- Idempotent

================================
SECURITY & BOUNDARIES
================================

- No database credentials exposed to frontend
- API keys stored server-side only
- CORS restricted to book domain
- Rate limiting at API level

================================
DEPLOYMENT PLAN
================================

Frontend:
- Remains static
- Deployed on GitHub Pages

Backend:
- Deployed separately (serverless or container)
- Independent scaling
- Environment-based configuration

================================
PHASE BOUNDARY
================================

This plan defines HOW the RAG system is structured.
No task breakdown.
No implementation.

Proceed only to /sp.tasks when instructed.

## Response snapshot

Created comprehensive system architecture plan for AI-powered book assistant with:

- Technical Context: Defined Python 3.11/JavaScript tech stack with FastAPI, React, OpenAI, Qdrant, Neon
- Constitution Check: Verified all 7 constitution gates passed before and after design
- Project Structure: Detailed backend (FastAPI) and frontend (React) architecture with file structure
- Research Summary: Documented key architectural decisions and alternatives considered
- Data Model: Created entities for BookContent, UserQuery, Response, and ChatSession with relationships
- API Contracts: Defined chat API endpoints with request/response schemas
- Quickstart Guide: Provided development setup and integration instructions

Architecture follows decoupled web application pattern with clean separation of concerns. Backend handles AI processing and data, frontend provides custom UI experience embedded in Docusaurus book site.

## Outcome

- ✅ Impact: Created complete architecture plan enabling implementation of AI-powered book assistant
- 🧪 Tests: No automated tests created yet
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.yaml
- 🔁 Next prompts: Ready for /sp.tasks to create implementation tasks
- 🧠 Reflection: Architecture successfully translates feature spec into concrete technical implementation plan

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with task creation phase