"""
Script to ingest book content into Qdrant (vector DB) and Neon (Postgres DB)
This will process all markdown files from the ai-book/docs directory
"""

import os
import sys
import asyncio
from pathlib import Path
import re
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import psycopg2
from psycopg2.extras import execute_values

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")

# Initialize clients
genai.configure(api_key=GEMINI_API_KEY)
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Collection name
COLLECTION_NAME = "book_content"

def parse_markdown_file(file_path: str) -> Dict:
    """Parse markdown file and extract metadata and content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from front matter or first heading
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(file_path).stem

    # Extract chapter number from filename
    chapter_match = re.search(r'chapter-(\d+)', file_path)
    chapter_number = int(chapter_match.group(1)) if chapter_match else 0

    # Remove front matter if present
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    return {
        'title': title,
        'chapter': chapter_number,
        'file_path': file_path,
        'content': content
    }

def chunk_content(content: str, chunk_size: int = 500) -> List[str]:
    """Split content into chunks for embedding"""
    # Split by paragraphs first
    paragraphs = content.split('\n\n')

    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_length = len(para.split())

        if current_length + para_length > chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_length = para_length
        else:
            current_chunk.append(para)
            current_length += para_length

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks

def generate_embedding(text: str) -> List[float]:
    """Generate embedding using Gemini API"""
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def create_qdrant_collection():
    """Create or recreate Qdrant collection"""
    try:
        # Delete collection if exists
        try:
            qdrant_client.delete_collection(collection_name=COLLECTION_NAME)
            print(f"Deleted existing collection: {COLLECTION_NAME}")
        except:
            pass

        # Create new collection (Gemini embeddings are 768 dimensions)
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        print(f"Created collection: {COLLECTION_NAME}")
        return True
    except Exception as e:
        print(f"Error creating collection: {e}")
        return False

def setup_database():
    """Create database tables if they don't exist"""
    try:
        conn = psycopg2.connect(NEON_DATABASE_URL)
        cursor = conn.cursor()

        # Create book_chapters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_chapters (
                id SERIAL PRIMARY KEY,
                chapter_number INTEGER NOT NULL,
                title VARCHAR(500) NOT NULL,
                file_path VARCHAR(500),
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create book_chunks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_chunks (
                id SERIAL PRIMARY KEY,
                chapter_id INTEGER REFERENCES book_chapters(id),
                chunk_index INTEGER NOT NULL,
                chunk_text TEXT NOT NULL,
                vector_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database tables created successfully")
        return True
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

def ingest_book_content():
    """Main function to ingest all book content"""
    print("Starting book content ingestion...")

    # Setup
    if not create_qdrant_collection():
        print("Failed to create Qdrant collection")
        return

    if not setup_database():
        print("Failed to setup database")
        return

    # Find all markdown files
    docs_dir = Path(__file__).parent.parent / "ai-book" / "docs"
    md_files = list(docs_dir.glob("chapter-*.mdx")) + list(docs_dir.glob("chapter-*.md"))
    md_files.sort()

    print(f"Found {len(md_files)} chapter files")

    # Connect to database
    conn = psycopg2.connect(NEON_DATABASE_URL)
    cursor = conn.cursor()

    point_id = 0

    for md_file in md_files:
        print(f"\nProcessing: {md_file.name}")

        # Parse file
        parsed = parse_markdown_file(str(md_file))

        # Insert chapter into database
        cursor.execute("""
            INSERT INTO book_chapters (chapter_number, title, file_path, content)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (parsed['chapter'], parsed['title'], parsed['file_path'], parsed['content']))

        chapter_id = cursor.fetchone()[0]
        conn.commit()

        # Chunk content
        chunks = chunk_content(parsed['content'])
        print(f"  Created {len(chunks)} chunks")

        # Process each chunk
        points = []
        chunk_records = []

        for idx, chunk in enumerate(chunks):
            if not chunk.strip():
                continue

            # Generate embedding
            embedding = generate_embedding(chunk)
            if embedding is None:
                continue

            # Prepare Qdrant point
            vector_id = f"ch{parsed['chapter']}_chunk{idx}"
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "chapter": parsed['chapter'],
                    "title": parsed['title'],
                    "chunk_text": chunk,
                    "chunk_index": idx,
                    "vector_id": vector_id
                }
            ))

            # Prepare database record
            chunk_records.append((chapter_id, idx, chunk, vector_id))

            point_id += 1

        # Insert into Qdrant
        if points:
            qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            print(f"  Inserted {len(points)} vectors into Qdrant")

        # Insert into Postgres
        if chunk_records:
            execute_values(
                cursor,
                """
                INSERT INTO book_chunks (chapter_id, chunk_index, chunk_text, vector_id)
                VALUES %s
                """,
                chunk_records
            )
            conn.commit()
            print(f"  Inserted {len(chunk_records)} chunks into Postgres")

    cursor.close()
    conn.close()

    print(f"\n✅ Ingestion complete! Processed {len(md_files)} chapters with {point_id} total chunks")

if __name__ == "__main__":
    # Check environment variables
    if not all([GEMINI_API_KEY, QDRANT_URL, NEON_DATABASE_URL]):
        print("❌ Error: Missing required environment variables")
        print("Please set: GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DATABASE_URL")
        sys.exit(1)

    ingest_book_content()
