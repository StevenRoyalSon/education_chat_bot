"""
Create Embeddings and Store in Supabase
This script reads documents, creates embeddings using OpenAI, and stores them in Supabase
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from document_loader import load_documents, chunk_document
from database import save_document_embedding

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file")
    print("Please add your OpenAI API key to .env file:")
    print("OPENAI_API_KEY=sk-your-key-here")
    exit(1)

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

chunk_size = config["rag"]["chunk_size"]
chunk_overlap = config["rag"]["chunk_overlap"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def create_embedding(text):
    """
    Create an embedding for the given text using OpenAI
    Args:
        text: The text to create embedding for
    Returns:
        List of floats representing the embedding
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None


def process_and_store_embeddings():
    """
    Load documents, create embeddings, and store in Supabase
    """
    print("Loading documents...")
    documents = load_documents()
    
    if not documents:
        print("No documents found!")
        return
    
    total_chunks = 0
    success_count = 0
    
    for doc in documents:
        print(f"\nProcessing: {doc['file_name']}")
        
        # Split document into chunks
        chunks = chunk_document(doc['content'], chunk_size, chunk_overlap)
        print(f"  Created {len(chunks)} chunks")
        
        # Create and store embeddings for each chunk
        for i, chunk in enumerate(chunks):
            print(f"  Processing chunk {i+1}/{len(chunks)}...", end=" ")
            
            # Create embedding
            embedding = create_embedding(chunk)
            
            if embedding:
                # Store in database
                result = save_document_embedding(
                    document_name=doc['file_name'],
                    grade=doc['grade'],
                    subject=doc['subject'],
                    chunk_text=chunk,
                    embedding=embedding
                )
                
                if result:
                    success_count += 1
                    print("✓")
                else:
                    print("✗ (database error)")
            else:
                print("✗ (embedding error)")
            
            total_chunks += 1
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Total chunks processed: {total_chunks}")
    print(f"Successfully stored: {success_count}")
    print(f"Failed: {total_chunks - success_count}")


# Run the script
if __name__ == "__main__":
    print("="*50)
    print("Creating Embeddings for Educational Documents")
    print("="*50)
    process_and_store_embeddings()
