"""
Document Loader
This file reads educational documents from the education_data folder
"""

import os
import json
from pathlib import Path

# Load configuration from config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Get document folder from config
DOCUMENT_FOLDER = config["documents"]["folder"]
FILE_TYPES = config["documents"]["file_types"]


def load_documents():
    """
    Load all documents from the education_data folder
    Returns:
        List of dictionaries with document information
    """
    documents = []
    
    # Check if folder exists
    if not os.path.exists(DOCUMENT_FOLDER):
        print(f"Error: Folder '{DOCUMENT_FOLDER}' not found")
        return documents
    
    # Get all files in the folder
    files = os.listdir(DOCUMENT_FOLDER)
    
    for file_name in files:
        # Check if file has the right extension
        file_path = os.path.join(DOCUMENT_FOLDER, file_name)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Check file extension
        file_ext = os.path.splitext(file_name)[1].lower()
        if file_ext not in FILE_TYPES:
            continue
        
        # Read the file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract grade and subject from filename
            # Example: "Grade_1_English.txt" -> grade="Grade 1", subject="English"
            name_without_ext = os.path.splitext(file_name)[0]
            parts = name_without_ext.split("_")
            
            if len(parts) >= 3:
                grade = parts[0] + "_" + parts[1]  # "Grade_1"
                subject = parts[2]  # "English"
                
                documents.append({
                    "file_name": file_name,
                    "grade": grade,
                    "subject": subject,
                    "content": content
                })
                print(f"Loaded: {file_name} ({grade} - {subject})")
            
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
    
    return documents


def chunk_document(content, chunk_size=500, chunk_overlap=50):
    """
    Split document content into smaller chunks
    Args:
        content: The full document text
        chunk_size: Size of each chunk (default 500)
        chunk_overlap: Overlap between chunks (default 50)
    Returns:
        List of text chunks
    """
    chunks = []
    
    # Split content into chunks
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap
    
    return chunks


# Test the document loader
if __name__ == "__main__":
    print("Loading documents...")
    documents = load_documents()
    print(f"\nTotal documents loaded: {len(documents)}")
    
    if documents:
        print("\nDocument summary:")
        for doc in documents:
            print(f"- {doc['file_name']}: {len(doc['content'])} characters")
            # Show first chunk
            chunks = chunk_document(doc['content'])
            print(f"  Number of chunks: {len(chunks)}")
            print(f"  First chunk preview: {chunks[0][:100]}...")
