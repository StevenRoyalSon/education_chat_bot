# Education Chatbot Project - Complete Setup Prompt

Copy this entire prompt and paste it to an AI assistant to recreate the complete Education Chatbot project.

---

## PROJECT OVERVIEW

Create an Education Chatbot for Grade 1-5 students using:
- Python for backend
- Streamlit for user interface
- Supabase for database
- LangChain and RAG for answering questions from documents
- OpenAI for generating answers
- JSON files for configuration

## PROJECT STRUCTURE

```
education_chat_bot/
├── app.py                      # Main Streamlit application
├── database.py                 # Supabase database operations
├── document_loader.py          # Load educational documents
├── rag_chatbot.py              # RAG chatbot logic
├── create_embeddings.py        # Create embeddings for documents
├── config.json                 # Application configuration
├── subjects.json               # Grades and subjects data
├── requirements.txt            # Python libraries
├── README.md                   # Project documentation
├── SETUP_GUIDE.md              # Database setup guide
├── .env.example                # Environment variables template
├── database.sql                # Complete database schema
├── step1_users_table.sql       # Users table creation
├── step2_chat_history_table.sql # Chat history table
├── step3_document_embeddings_simple.sql # Document embeddings table
├── step4_security_policies.sql # Security policies
├── create_users_table.sql      # Users table creation (alternative)
├── test_database.py            # Database connection test
├── test_connection_simple.py   # Simple connection test
├── test_with_insert.py         # Test with data insertion
├── education_data/            # Educational documents folder
│   ├── Grade_1_English.txt
│   ├── Grade_1_Math.txt
│   ├── Grade_1_EVS.txt
│   ├── Grade_2_English.txt
│   ├── Grade_2_Math.txt
│   ├── Grade_2_EVS.txt
│   ├── Grade_3_English.txt
│   ├── Grade_3_Math.txt
│   ├── Grade_3_EVS.txt
│   ├── Grade_4_English.txt
│   ├── Grade_4_Math.txt
│   ├── Grade_4_EVS.txt
│   ├── Grade_5_English.txt
│   ├── Grade_5_Math.txt
│   └── Grade_5_EVS.txt
└── .env                        # Your API keys (not in git)
```

---

## STEP 1: CREATE PROJECT FOLDER

1. Create a folder named `education_chat_bot`
2. Inside it, create a folder named `education_data`

---

## STEP 2: CREATE requirements.txt

Create a file named `requirements.txt` with this content:

```
streamlit
supabase
openai
langchain
langchain-openai
langchain-community
python-dotenv
pypdf
```

---

## STEP 3: CREATE .env.example

Create a file named `.env.example` with this content:

```
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

---

## STEP 4: CREATE .gitignore

Create a file named `.gitignore` with this content:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Virtual environments
education_chat_bot/

# Streamlit
.streamlit/
```

---

## STEP 5: CREATE config.json

Create a file named `config.json` with this content:

```json
{
  "app_name": "Education Chatbot",
  "app_description": "Grade 1-5 Learning Assistant",
  "openai": {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 500
  },
  "rag": {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "top_k_results": 3
  },
  "documents": {
    "folder": "education_data",
    "file_types": [".txt", ".pdf"]
  }
}
```

---

## STEP 6: CREATE subjects.json

Create a file named `subjects.json` with this content:

```json
{
  "grades": [
    {
      "grade": "Grade 1",
      "subjects": ["Math", "English", "EVS"]
    },
    {
      "grade": "Grade 2",
      "subjects": ["Math", "English", "EVS"]
    },
    {
      "grade": "Grade 3",
      "subjects": ["Math", "English", "EVS"]
    },
    {
      "grade": "Grade 4",
      "subjects": ["Math", "English", "EVS"]
    },
    {
      "grade": "Grade 5",
      "subjects": ["Math", "English", "EVS"]
    }
  ],
  "unrelated_question_response": "It's not my job to explain this. Please reach out to the administrator to provide your required information.",
  "greeting_responses": {
    "hi": "Hello! How can I help you with your studies today?",
    "hello": "Hi there! What would you like to learn about?",
    "good morning": "Good morning! Ready to learn something new?",
    "good afternoon": "Good afternoon! How can I assist you?",
    "good evening": "Good evening! What can I help you with today?",
    "hey": "Hey! What would you like to learn?"
  }
}
```

---

## STEP 7: CREATE database.py

Create a file named `database.py` with this content:

```python
"""
Database Connection and Operations for Supabase
This file handles all database operations for the Education Chatbot
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if credentials are available
if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
    exit(1)

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# USER OPERATIONS
def signup_user(name, email, password):
    """
    Register a new user in the database
    """
    try:
        result = supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": password
        }).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Signup error: {e}")
        return None


def login_user(email, password):
    """
    Login a user by checking email and password
    """
    try:
        result = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Login error: {e}")
        return None


def get_user_by_email(email):
    """
    Get user information by email
    """
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Get user error: {e}")
        return None


# CHAT HISTORY OPERATIONS
def save_chat_message(user_id, user_question, ai_response):
    """
    Save a chat message to the database
    """
    try:
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
    """
    try:
        result = supabase.table("chat_history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Get chat history error: {e}")
        return []


def delete_all_user_chats(user_id):
    """
    Delete all chat messages for a specific user
    """
    try:
        result = supabase.table("chat_history").delete().eq("user_id", user_id).execute()
        return True if result.data else False
    except Exception as e:
        print(f"Delete all chats error: {e}")
        return False


# DOCUMENT EMBEDDINGS OPERATIONS
def save_document_embedding(document_name, grade, subject, chunk_text, embedding):
    """
    Save a document chunk and its embedding to the database
    """
    try:
        # Convert embedding list to string for storage
        embedding_str = str(embedding)
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


def get_all_embeddings():
    """
    Get all document embeddings from the database
    """
    try:
        result = supabase.table("document_embeddings").select("*").execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Get all embeddings error: {e}")
        return []


# Test the database connection
if __name__ == "__main__":
    print("Testing database connection...")
    print(f"Supabase URL: {SUPABASE_URL}")
    print("Database connection test complete!")
```

---

## STEP 8: CREATE document_loader.py

Create a file named `document_loader.py` with this content:

```python
"""
Document Loader
This file reads educational documents from the education_data folder
"""

import os
import json

# Load configuration from config.json
with open("config.json", "r") as f:
    config = json.load(f)

DOCUMENT_FOLDER = config["documents"]["folder"]
FILE_TYPES = config["documents"]["file_types"]


def load_documents():
    """
    Load all documents from the education_data folder
    """
    documents = []
    
    if not os.path.exists(DOCUMENT_FOLDER):
        print(f"Error: Folder '{DOCUMENT_FOLDER}' not found")
        return documents
    
    files = os.listdir(DOCUMENT_FOLDER)
    
    for file_name in files:
        file_path = os.path.join(DOCUMENT_FOLDER, file_name)
        
        if os.path.isdir(file_path):
            continue
        
        file_ext = os.path.splitext(file_name)[1].lower()
        if file_ext not in FILE_TYPES:
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            name_without_ext = os.path.splitext(file_name)[0]
            parts = name_without_ext.split("_")
            
            if len(parts) >= 3:
                grade = parts[0] + "_" + parts[1]
                subject = parts[2]
                
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
    """
    chunks = []
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
```

---

## STEP 9: CREATE rag_chatbot.py

Create a file named `rag_chatbot.py` with this content:

```python
"""
RAG Chatbot - Retrieval Augmented Generation
This file handles retrieving relevant documents and generating answers
"""

import os
import json
import math
import ast
from dotenv import load_dotenv
from openai import OpenAI
from database import get_all_embeddings, save_chat_message

# Load environment variables
load_dotenv()

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

model = config["openai"]["model"]
temperature = config["openai"]["temperature"]
max_tokens = config["openai"]["max_tokens"]
top_k = config["rag"]["top_k_results"]

unrelated_response = subjects_data["unrelated_question_response"]
greeting_responses = subjects_data["greeting_responses"]


def cosine_similarity(a, b):
    """
    Calculate cosine similarity between two vectors
    """
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    
    return dot_product / (magnitude_a * magnitude_b)


def create_query_embedding(query):
    """
    Create embedding for user query
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
    """
    all_embeddings = get_all_embeddings()
    
    if not all_embeddings:
        return []
    
    similarities = []
    for emb in all_embeddings:
        if emb["embedding"]:
            # Convert embedding from string to list of floats if needed
            embedding_vector = emb["embedding"]
            if isinstance(embedding_vector, str):
                embedding_vector = ast.literal_eval(embedding_vector)
            
            similarity = cosine_similarity(query_embedding, embedding_vector)
            similarities.append({
                "chunk_text": emb["chunk_text"],
                "grade": emb["grade"],
                "subject": emb["subject"],
                "similarity": similarity
            })
    
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:top_k]


def is_greeting(query):
    """
    Check if the query is a greeting
    """
    query_lower = query.lower().strip()
    
    for greeting in greeting_responses.keys():
        if greeting in query_lower:
            return greeting
    
    return None


def generate_answer(query, relevant_chunks):
    """
    Generate answer using OpenAI based on relevant chunks
    """
    if not relevant_chunks or relevant_chunks[0]["similarity"] < 0.3:
        return unrelated_response
    
    context = "\n\n".join([chunk["chunk_text"] for chunk in relevant_chunks])
    
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
    """
    greeting = is_greeting(query)
    if greeting:
        return greeting_responses[greeting]
    
    query_embedding = create_query_embedding(query)
    
    if not query_embedding:
        return "Sorry, I couldn't process your question."
    
    relevant_chunks = retrieve_relevant_chunks(query_embedding, top_k)
    answer = generate_answer(query, relevant_chunks)
    save_chat_message(user_id, query, answer)
    
    return answer
```

---

## STEP 10: CREATE create_embeddings.py

Create a file named `create_embeddings.py` with this content:

```python
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
        
        chunks = chunk_document(doc['content'], chunk_size, chunk_overlap)
        print(f"  Created {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            print(f"  Processing chunk {i+1}/{len(chunks)}...", end=" ")
            
            embedding = create_embedding(chunk)
            
            if embedding:
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


if __name__ == "__main__":
    print("="*50)
    print("Creating Embeddings for Educational Documents")
    print("="*50)
    process_and_store_embeddings()
```

---

## STEP 11: CREATE app.py

Create a file named `app.py` with this content:

```python
"""
Education Chatbot - Main Streamlit Application
This is the main application file with Signup, Login, and Chatbot pages
"""

import streamlit as st
from database import signup_user, login_user, get_user_by_email, get_chat_history, delete_all_user_chats
from rag_chatbot import process_user_query

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Education Chatbot",
    page_icon="📚",
    layout="centered"
)

# SESSION STATE MANAGEMENT
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "login"


# NAVIGATION FUNCTIONS
def go_to_login():
    st.session_state.current_page = "login"


def go_to_signup():
    st.session_state.current_page = "signup"


def go_to_chatbot():
    st.session_state.current_page = "chatbot"


def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.current_page = "login"


# LOGIN PAGE
def login_page():
    st.title("📚 Education Chatbot")
    st.subheader("Login to Continue")
    
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login", use_container_width=True):
        if not email or not password:
            st.error("Please enter both email and password")
            return
        
        user = login_user(email, password)
        
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user["id"]
            st.session_state.user_name = user["name"]
            st.success(f"Welcome back, {user['name']}!")
            go_to_chatbot()
            st.rerun()
        else:
            st.error("Invalid email or password")
    
    st.divider()
    st.write("Don't have an account?")
    if st.button("Sign Up", use_container_width=True):
        go_to_signup()
        st.rerun()


# SIGNUP PAGE
def signup_page():
    st.title("📚 Education Chatbot")
    st.subheader("Create Your Account")
    
    name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    if st.button("Sign Up", use_container_width=True):
        if not name or not email or not password or not confirm_password:
            st.error("Please fill in all fields")
            return
        
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        
        existing_user = get_user_by_email(email)
        if existing_user:
            st.error("This email is already registered")
            return
        
        user = signup_user(name, email, password)
        
        if user:
            st.success("Account created successfully! Please login.")
            go_to_login()
            st.rerun()
        else:
            st.error("Failed to create account. Please try again.")
    
    st.divider()
    st.write("Already have an account?")
    if st.button("Login", use_container_width=True):
        go_to_login()
        st.rerun()


# CHATBOT PAGE
def chatbot_page():
    st.title("📚 Education Chatbot")
    st.subheader(f"Welcome, {st.session_state.user_name}!")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("Delete All Chats", use_container_width=True):
            if st.session_state.get("confirm_delete", False):
                delete_all_user_chats(st.session_state.user_id)
                st.session_state.messages = []
                st.session_state.confirm_delete = False
                st.success("All chats deleted from database!")
                st.rerun()
            else:
                st.session_state.confirm_delete = True
                st.warning("Click Delete All Chats again to confirm!")
                st.rerun()
    
    with col3:
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
    
    st.divider()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if not st.session_state.messages:
        chat_history = get_chat_history(st.session_state.user_id)
        for msg in reversed(chat_history):
            st.session_state.messages.append({
                "role": "user",
                "content": msg["user_question"]
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": msg["ai_response"]
            })
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask a question about your studies..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = process_user_query(st.session_state.user_id, prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


# MAIN APPLICATION
def main():
    if st.session_state.logged_in:
        chatbot_page()
    else:
        if st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "signup":
            signup_page()
        else:
            login_page()


if __name__ == "__main__":
    main()
```

---

## STEP 12: CREATE DATABASE SQL FILES

### step1_users_table.sql
```sql
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE users IS 'Stores user registration details';
```

### step2_chat_history_table.sql
```sql
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_question TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE chat_history IS 'Stores conversation history';
```

### step3_document_embeddings_simple.sql
```sql
DROP TABLE IF EXISTS document_embeddings;

CREATE TABLE document_embeddings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    grade VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE document_embeddings IS 'Stores document chunks and embeddings as JSON';
```

### step4_security_policies.sql
```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_embeddings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public signup" ON users;
DROP POLICY IF EXISTS "Users can read own data" ON users;
DROP POLICY IF EXISTS "Users can insert own messages" ON chat_history;
DROP POLICY IF EXISTS "Users can read own history" ON chat_history;
DROP POLICY IF EXISTS "Users can delete own messages" ON chat_history;
DROP POLICY IF EXISTS "Allow read access to embeddings" ON document_embeddings;

CREATE POLICY "Allow public signup" ON users
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can read own data" ON users
    FOR SELECT
    USING (email = current_setting('app.current_user_email', true));

CREATE POLICY "Users can insert own messages" ON chat_history
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Users can read own history" ON chat_history
    FOR SELECT
    USING (true);

CREATE POLICY "Users can delete own messages" ON chat_history
    FOR DELETE
    USING (true);

CREATE POLICY "Allow read access to embeddings" ON document_embeddings
    FOR SELECT
    USING (true);
```

---

## STEP 13: CREATE EDUCATIONAL DOCUMENTS

Create these files in the `education_data/` folder with educational content for each grade and subject:

### Grade_1_English.txt
```
GRADE: 1
SUBJECT: English
SOURCE: Educational Content

NOUN: A noun is a naming word. It names people, places, animals, and things.
Examples: cat, dog, school, teacher, book, pencil.

VERB: A verb is an action word. It tells what someone or something does.
Examples: run, jump, eat, sleep, play, read.

ADJECTIVE: An adjective describes a noun. It tells us about color, size, or how something looks.
Examples: big, small, red, blue, happy, sad.
```

### Grade_1_Math.txt
```
GRADE: 1
SUBJECT: Math
SOURCE: Educational Content

ADDITION: Addition is putting numbers together to get a total.
Example: 2 + 3 = 5 (two plus three equals five)

SUBTRACTION: Subtraction is taking away from a number.
Example: 5 - 2 = 3 (five minus two equals three)

COUNTING: Counting from 1 to 10: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

SHAPES: Basic shapes include circle, square, triangle, and rectangle.
```

### Grade_1_EVS.txt
```
GRADE: 1
SUBJECT: EVS (Environmental Studies)
SOURCE: Educational Content

PLANTS: Plants need water, sunlight, and soil to grow.
Parts of a plant: roots, stem, leaves, flowers.

ANIMALS: Animals are living things that move and eat.
Examples: dog, cat, bird, fish, cow.

SEASONS: There are four seasons: summer, rainy, winter, and spring.
```

(Repeat similar structure for Grade 2, 3, 4, 5 with age-appropriate content for each subject)

---

## STEP 14: CREATE DOCUMENTATION FILES

### README.md
```markdown
# Education Chatbot for Grades 1-5

A simple chatbot to help Grade 1-5 students learn using educational documents.

## Setup Instructions

### 1. Install Python Libraries
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Add your Supabase URL and Key
3. Add your OpenAI API Key

### 3. Create Supabase Tables
1. Go to your Supabase project dashboard
2. Open SQL Editor
3. Execute the SQL files in order: step1, step2, step3, step4

### 4. Create Embeddings
```bash
python create_embeddings.py
```

### 5. Run the Application
```bash
streamlit run app.py
```
```

### SETUP_GUIDE.md
```markdown
# Database Setup Guide

## Execute These SQL Files One by One in Supabase

### Step 1: Create Users Table
Open `step1_users_table.sql`, copy, paste in SQL Editor, click "Run"

### Step 2: Create Chat History Table
Open `step2_chat_history_table.sql`, copy, paste in SQL Editor, click "Run"

### Step 3: Create Document Embeddings Table
Open `step3_document_embeddings_simple.sql`, copy, paste in SQL Editor, click "Run"

### Step 4: Add Security Policies
Open `step4_security_policies.sql`, copy, paste in SQL Editor, click "Run"

## Then Create Embeddings:
1. Make sure you have OPENAI_API_KEY in your .env file
2. Run: `python create_embeddings.py`
```

---

## STEP 15: CREATE TEST FILES

### test_database.py
```python
"""
Test Database Connection
"""

from database import supabase, SUPABASE_URL

print("Testing Supabase connection...")
print(f"Supabase URL: {SUPABASE_URL}")

try:
    result = supabase.table("users").select("count").execute()
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")
```

### test_connection_simple.py
```python
"""
Simple connection test
"""

from database import supabase, SUPABASE_URL

print("Testing basic Supabase connection...")
print(f"Supabase URL: {SUPABASE_URL}")

try:
    response = supabase.table("users").select("*").execute()
    print("Success! Users table exists and is accessible.")
except Exception as e:
    print(f"Error: {e}")
```

---

## FINAL SETUP INSTRUCTIONS

1. Install Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API keys:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Set up Supabase database:
   - Go to https://supabase.com/dashboard
   - Create a new project
   - Open SQL Editor
   - Execute step1, step2, step3, step4 SQL files in order

4. Create embeddings:
   ```bash
   python create_embeddings.py
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## FEATURES

- User signup and login
- Chat with AI using educational documents
- Chat history saved in database
- Clear chat and delete chat buttons
- Greeting responses
- Unrelated question handling
- Grade 1-5 educational content

---

That's it! This prompt contains everything needed to recreate the complete Education Chatbot project.
