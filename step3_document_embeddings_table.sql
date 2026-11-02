-- Step 3: Create Document Embeddings Table
-- Run this after Step 2
-- Note: This uses pgvector extension for embeddings

-- Enable pgvector extension (needed for VECTOR type)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_embeddings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    grade VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE document_embeddings IS 'Stores document chunks and embeddings';
