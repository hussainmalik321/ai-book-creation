# Research Summary: AI-Powered Book Assistant

## Decision: Architecture Pattern
**Rationale**: Selected decoupled web application architecture (backend + frontend) to maintain separation of concerns, allow independent scaling, and ensure security by keeping AI processing and sensitive data on the server side.
**Alternatives considered**:
- Monolithic architecture (rejected due to security concerns and tight coupling)
- Client-side AI processing (rejected due to performance and security limitations)

## Decision: Technology Stack
**Rationale**: FastAPI provides excellent async performance for AI workloads and has strong OpenAPI integration. React components provide flexibility for embedding in Docusaurus site while maintaining custom UI/UX requirements.
**Alternatives considered**:
- Node.js/Express backend (rejected due to performance concerns for AI workloads)
- Vue.js frontend (rejected due to team familiarity with React)

## Decision: Data Storage Strategy
**Rationale**: Qdrant vector database for embeddings ensures optimal similarity search performance for RAG, while Neon Postgres handles structured metadata with ACID properties.
**Alternatives considered**:
- Single database solution (rejected due to suboptimal performance for vector operations)
- In-memory storage (rejected due to persistence and scaling requirements)

## Decision: Content Restriction Mechanism
**Rationale**: Server-side content filtering ensures that selection-based Q&A strictly uses only the selected text, preventing cross-chapter leakage and maintaining trust.
**Alternatives considered**:
- Client-side filtering (rejected due to security concerns - client could bypass restrictions)
- Pre-computed selection indexes (rejected due to complexity and real-time selection requirements)

## Decision: Frontend Integration Approach
**Rationale**: React components provide the custom UI experience required by the constitution while being embeddable in the Docusaurus site without disrupting the reading flow.
**Alternatives considered**:
- iFrame embedding (rejected due to integration and responsiveness issues)
- Native Docusaurus plugin (rejected due to flexibility limitations)