"""
RAG Chatbot - Retrieval Augmented Generation
This file handles retrieving relevant documents and generating answers
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from database import get_all_embeddings, save_chat_message, get_chat_history

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit(1)

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

with open("subjects.json", "r") as f:
    subjects_data = json.load(f)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Get configuration values
model = config["openai"]["model"]
temperature = config["openai"]["temperature"]
max_tokens = config["openai"]["max_tokens"]
top_k = config["rag"]["top_k_results"]

# Get response messages
unrelated_response = subjects_data["unrelated_question_response"]
greeting_responses = subjects_data["greeting_responses"]


def cosine_similarity(a, b):
    """
    Calculate cosine similarity between two vectors
    Args:
        a: First vector (list of floats)
        b: Second vector (list of floats)
    Returns:
        Similarity score between 0 and 1
    """
    import math
    
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    
    return dot_product / (magnitude_a * magnitude_b)


def create_query_embedding(query):
    """
    Create embedding for user query
    Args:
        query: User's question
    Returns:
        Embedding vector
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error creating query embedding: {e}")
        return None


def retrieve_relevant_chunks(query_embedding, top_k=3):
    """
    Retrieve most relevant document chunks based on query
    Args:
        query_embedding: Embedding of user's query
        top_k: Number of chunks to retrieve
    Returns:
        List of relevant chunks with similarity scores
    """
    # Get all embeddings from database
    all_embeddings = get_all_embeddings()
    
    if not all_embeddings:
        return []
    
    # Calculate similarity for each chunk
    similarities = []
    for emb in all_embeddings:
        if emb["embedding"]:
            # Convert embedding from string to list of floats if needed
            embedding_vector = emb["embedding"]
            if isinstance(embedding_vector, str):
                # Parse the string representation to list
                import ast
                embedding_vector = ast.literal_eval(embedding_vector)
            
            similarity = cosine_similarity(query_embedding, embedding_vector)
            similarities.append({
                "chunk_text": emb["chunk_text"],
                "grade": emb["grade"],
                "subject": emb["subject"],
                "similarity": similarity
            })
    
    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Return top k results
    return similarities[:top_k]


def is_greeting(query):
    """
    Check if the query is a greeting
    Args:
        query: User's message
    Returns:
        True if greeting, False otherwise
    """
    query_lower = query.lower().strip()
    
    # Check against greeting responses
    for greeting in greeting_responses.keys():
        if greeting in query_lower:
            return greeting
    
    return None


def generate_answer(query, relevant_chunks):
    """
    Generate answer using OpenAI based on relevant chunks
    Args:
        query: User's question
        relevant_chunks: List of relevant document chunks
    Returns:
        Generated answer
    """
    # If no relevant chunks found, return unrelated response
    if not relevant_chunks or relevant_chunks[0]["similarity"] < 0.3:
        return unrelated_response
    
    # Build context from relevant chunks
    context = "\n\n".join([chunk["chunk_text"] for chunk in relevant_chunks])
    
    # Create prompt for OpenAI
    prompt = f"""You are a helpful education assistant for Grade 1-5 students.
Answer the following question based ONLY on the provided context.
If the answer is not in the context, say "I don't have information about that in my documents."

Context:
{context}

Question: {query}

Answer:"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful education assistant for young students."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "Sorry, I encountered an error generating the answer."


def process_user_query(user_id, query):
    """
    Process a user query and return the answer
    Args:
        user_id: The user's ID
        query: User's question
    Returns:
        The answer from the chatbot
    """
    # Check if it's a greeting
    greeting = is_greeting(query)
    if greeting:
        return greeting_responses[greeting]
    
    # Create embedding for query
    query_embedding = create_query_embedding(query)
    
    if not query_embedding:
        return "Sorry, I couldn't process your question."
    
    # Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(query_embedding, top_k)
    
    # Generate answer
    answer = generate_answer(query, relevant_chunks)
    
    # Save to chat history
    save_chat_message(user_id, query, answer)
    
    return answer


# Test the RAG system
if __name__ == "__main__":
    print("Testing RAG Chatbot...")
    
    # Test query
    test_query = "What is 2 + 2?"
    print(f"\nQuery: {test_query}")
    
    # Process query (you need a valid user_id)
    answer = process_user_query("test-user-id", test_query)
    print(f"Answer: {answer}")
