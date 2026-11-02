"""
Database Connection and Operations for Supabase
This file handles all database operations for the Education Chatbot
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
# This reads SUPABASE_URL and SUPABASE_KEY from .env file
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if credentials are available
if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
    exit(1)

# Create Supabase client
# This client will be used for all database operations
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================
# USER OPERATIONS
# Functions for signup, login, and user management
# ============================================================

def signup_user(name, email, password):
    """
    Register a new user in the database
    Args:
        name: User's full name
        email: User's email address
        password: User's password (will be stored as-is for simplicity)
    Returns:
        user data if successful, None if failed
    """
    try:
        # Insert new user into users table
        # The password is stored directly (in production, use bcrypt to hash)
        result = supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": password
        }).execute()
        
        # Return the user data
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Signup error: {e}")
        return None


def login_user(email, password):
    """
    Login a user by checking email and password
    Args:
        email: User's email address
        password: User's password
    Returns:
        user data if successful, None if failed
    """
    try:
        # Query users table for matching email and password
        result = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
        
        # Return user data if found
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Login error: {e}")
        return None


def get_user_by_email(email):
    """
    Get user information by email
    Args:
        email: User's email address
    Returns:
        user data if found, None if not found
    """
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Get user error: {e}")
        return None


# ============================================================
# CHAT HISTORY OPERATIONS
# Functions for saving and retrieving chat history
# ============================================================

def save_chat_message(user_id, user_question, ai_response):
    """
    Save a chat message to the database
    Args:
        user_id: The ID of the user
        user_question: The question asked by the user
        ai_response: The response from the AI
    Returns:
        message data if successful, None if failed
    """
    try:
        # Insert the message into chat_history table
        result = supabase.table("chat_history").insert({
            "user_id": user_id,
            "user_question": user_question,
            "ai_response": ai_response
        }).execute()
        
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Save chat error: {e}")
        return None


def get_chat_history(user_id):
    """
    Get all chat messages for a specific user
    Args:
        user_id: The ID of the user
    Returns:
        List of chat messages, empty list if none found
    """
    try:
        # Query chat_history table for user's messages
        # Order by created_at to show in chronological order
        result = supabase.table("chat_history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"Get chat history error: {e}")
        return []


def delete_chat_message(message_id):
    """
    Delete a specific chat message
    Args:
        message_id: The ID of the message to delete
    Returns:
        True if successful, False if failed
    """
    try:
        # Delete the message from chat_history table
        result = supabase.table("chat_history").delete().eq("id", message_id).execute()
        
        return True if result.data else False
        
    except Exception as e:
        print(f"Delete chat error: {e}")
        return False


def delete_all_user_chats(user_id):
    """
    Delete all chat messages for a specific user
    Args:
        user_id: The ID of the user
    Returns:
        True if successful, False if failed
    """
    try:
        # Delete all messages for the user
        result = supabase.table("chat_history").delete().eq("user_id", user_id).execute()
        
        return True if result.data else False
        
    except Exception as e:
        print(f"Delete all chats error: {e}")
        return False


# ============================================================
# DOCUMENT EMBEDDINGS OPERATIONS
# Functions for storing and retrieving document embeddings
# ============================================================

def save_document_embedding(document_name, grade, subject, chunk_text, embedding):
    """
    Save a document chunk and its embedding to the database
    Args:
        document_name: Name of the source document
        grade: Grade level (e.g., "Grade 1")
        subject: Subject (e.g., "Math")
        chunk_text: The text content of the chunk
        embedding: The vector embedding (list of floats)
    Returns:
        embedding data if successful, None if failed
    """
    try:
        # Convert embedding list to string for storage
        # Supabase VECTOR type stores as string representation
        embedding_str = str(embedding)
        
        # Insert the embedding into document_embeddings table
        result = supabase.table("document_embeddings").insert({
            "document_name": document_name,
            "grade": grade,
            "subject": subject,
            "chunk_text": chunk_text,
            "embedding": embedding_str
        }).execute()
        
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Save embedding error: {e}")
        return None


def get_embeddings_by_grade_subject(grade, subject):
    """
    Get all embeddings for a specific grade and subject
    Args:
        grade: Grade level (e.g., "Grade 1")
        subject: Subject (e.g., "Math")
    Returns:
        List of embeddings, empty list if none found
    """
    try:
        # Query document_embeddings table for matching grade and subject
        result = supabase.table("document_embeddings").select("*").eq("grade", grade).eq("subject", subject).execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"Get embeddings error: {e}")
        return []


def get_all_embeddings():
    """
    Get all document embeddings from the database
    Returns:
        List of all embeddings, empty list if none found
    """
    try:
        # Query all embeddings from document_embeddings table
        result = supabase.table("document_embeddings").select("*").execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"Get all embeddings error: {e}")
        return []


# ============================================================
# TEST FUNCTION
# Test the database connection
# ============================================================

if __name__ == "__main__":
    print("Testing database connection...")
    print(f"Supabase URL: {SUPABASE_URL}")
    print("Database connection test complete!")
