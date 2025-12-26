# Book Content Ingestion Instructions

This script will upload your book content to Qdrant (vector database) and Neon (PostgreSQL database).

## Prerequisites

1. **Environment Variables**: Make sure your `.env` file has:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   NEON_DATABASE_URL=your_neon_database_url
   ```

2. **Install Dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

## Running the Ingestion Script

### Option 1: From the backend directory
```bash
cd backend
python ingest_book_content.py
```

### Option 2: From the root directory
```bash
python backend/ingest_book_content.py
```

## What the Script Does

1. **Creates Qdrant Collection**: Sets up a vector collection named `book_content`
2. **Creates Database Tables**:
   - `book_chapters`: Stores chapter metadata
   - `book_chunks`: Stores text chunks with references to vectors
3. **Processes Markdown Files**: Reads all `chapter-*.md` and `chapter-*.mdx` files from `ai-book/docs/`
4. **Chunks Content**: Splits each chapter into ~500-word chunks
5. **Generates Embeddings**: Uses Google Gemini to create vector embeddings
6. **Uploads to Databases**:
   - Vectors → Qdrant
   - Metadata & text → Neon PostgreSQL

## Expected Output

```
Starting book content ingestion...
Created collection: book_content
Database tables created successfully
Found 5 chapter files

Processing: chapter-1.mdx
  Created 12 chunks
  Inserted 12 vectors into Qdrant
  Inserted 12 chunks into Postgres

...

✅ Ingestion complete! Processed 5 chapters with 67 total chunks
```

## Troubleshooting

### Error: Missing required environment variables
- Check that your `.env` file exists and has all required variables
- Make sure you're running from the correct directory

### Error: Connection refused
- Verify your Qdrant URL and API key are correct
- Check that your Neon database URL is accessible

### Error: Import errors
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.11+

## After Ingestion

Once ingestion is complete:
1. Your chatbot will now have access to the book content
2. Test the chatbot at: https://ai-book-creation-phi.vercel.app/
3. Ask questions like "What is the purpose of this book?"

## Re-running the Script

The script is **destructive** - it will:
- Delete the existing Qdrant collection
- Recreate all tables (using IF NOT EXISTS)
- Re-upload all content

This ensures clean data without duplicates.
