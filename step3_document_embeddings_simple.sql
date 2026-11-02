-- Step 3: Create Document Embeddings Table (Simplified)
-- This version stores embeddings as JSON text instead of VECTOR type
-- Run this after Step 2

-- Drop the old table if it exists
DROP TABLE IF EXISTS document_embeddings;

CREATE TABLE document_embeddings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    grade VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding TEXT NOT NULL,  -- Store as JSON string
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE document_embeddings IS 'Stores document chunks and embeddings as JSON';
