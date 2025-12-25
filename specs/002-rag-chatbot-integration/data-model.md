# Data Model: AI-Powered Book Assistant

## Core Entities

### BookContent
- **id**: string (unique identifier for content chunk)
- **title**: string (chapter/section title)
- **content**: text (the actual book content text)
- **chunk_text**: text (individual text chunk for embedding)
- **metadata**: object (chapter, section, position in book)
- **embedding_vector**: array<float> (vector representation for similarity search)
- **relations**: array<string> (references to related content)

**Validation rules**: Content must not be empty, metadata must include chapter and position

### UserQuery
- **id**: string (unique query identifier)
- **query_text**: text (the user's question)
- **query_type**: enum (GLOBAL_QA | SELECTION_QA)
- **selected_text**: text (optional, for selection-based queries)
- **book_content_ids**: array<string> (referenced content for selection mode)
- **timestamp**: datetime (when query was made)
- **session_id**: string (for conversation context)

**Validation rules**: Query text must not be empty, selection text must exist if query_type is SELECTION_QA

### Response
- **id**: string (unique response identifier)
- **query_id**: string (reference to the original query)
- **response_text**: text (AI-generated response)
- **source_chunks**: array<string> (content IDs used to generate response)
- **confidence_score**: float (confidence level of response)
- **timestamp**: datetime (when response was generated)
- **is_fallback**: boolean (true if response indicates lack of knowledge)

**Validation rules**: Response text must not be empty, source chunks must reference valid BookContent

### ChatSession
- **id**: string (unique session identifier)
- **user_id**: string (optional, for tracking if needed)
- **start_time**: datetime (session start)
- **last_activity**: datetime (last interaction)
- **active**: boolean (whether session is still active)

**Validation rules**: Session must have a start time

## Relationships
- One ChatSession can contain multiple UserQuery instances
- One UserQuery generates one Response
- One Response references multiple BookContent chunks as sources
- BookContent has parent-child relationships based on book structure (chapter/section hierarchy)

## State Transitions
- ChatSession: ACTIVE → INACTIVE (after period of inactivity)
- UserQuery: CREATED → PROCESSED → RESPONSE_GENERATED