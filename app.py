"""
Education Chatbot - Main Streamlit Application
This is the main application file with Signup, Login, and Chatbot pages
"""

import streamlit as st
from database import signup_user, login_user, get_user_by_email, get_chat_history, delete_all_user_chats
from rag_chatbot import process_user_query

# ============================================================
# PAGE CONFIGURATION
# Set up the Streamlit page
# ============================================================

st.set_page_config(
    page_title="Education Chatbot",
    page_icon="📚",
    layout="centered"
)

# ============================================================
# SESSION STATE MANAGEMENT
# Store user login state and current page
# ============================================================

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "login"


# ============================================================
# NAVIGATION FUNCTIONS
# Functions to switch between pages
# ============================================================

def go_to_login():
    """Navigate to login page"""
    st.session_state.current_page = "login"


def go_to_signup():
    """Navigate to signup page"""
    st.session_state.current_page = "signup"


def go_to_chatbot():
    """Navigate to chatbot page"""
    st.session_state.current_page = "chatbot"


def logout():
    """Logout user and go to login page"""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.current_page = "login"


# ============================================================
# LOGIN PAGE
# User login form
# ============================================================

def login_page():
    """Display the login page"""
    st.title("📚 Education Chatbot")
    st.subheader("Login to Continue")
    
    # Login form
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    # Login button
    if st.button("Login", use_container_width=True):
        # Validate inputs
        if not email or not password:
            st.error("Please enter both email and password")
            return
        
        # Try to login
        user = login_user(email, password)
        
        if user:
            # Login successful
            st.session_state.logged_in = True
            st.session_state.user_id = user["id"]
            st.session_state.user_name = user["name"]
            st.success(f"Welcome back, {user['name']}!")
            go_to_chatbot()
            st.rerun()
        else:
            # Login failed
            st.error("Invalid email or password")
    
    # Link to signup page
    st.divider()
    st.write("Don't have an account?")
    if st.button("Sign Up", use_container_width=True):
        go_to_signup()
        st.rerun()


# ============================================================
# SIGNUP PAGE
# User registration form
# ============================================================

def signup_page():
    """Display the signup page"""
    st.title("📚 Education Chatbot")
    st.subheader("Create Your Account")
    
    # Signup form
    name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    # Signup button
    if st.button("Sign Up", use_container_width=True):
        # Validate inputs
        if not name or not email or not password or not confirm_password:
            st.error("Please fill in all fields")
            return
        
        # Check if passwords match
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        
        # Check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            st.error("This email is already registered")
            return
        
        # Try to signup
        user = signup_user(name, email, password)
        
        if user:
            # Signup successful
            st.success("Account created successfully! Please login.")
            go_to_login()
            st.rerun()
        else:
            # Signup failed
            st.error("Failed to create account. Please try again.")
    
    # Link to login page
    st.divider()
    st.write("Already have an account?")
    if st.button("Login", use_container_width=True):
        go_to_login()
        st.rerun()


# ============================================================
# CHATBOT PAGE
# Main chatbot interface with chat functionality
# ============================================================

def chatbot_page():
    """Display the chatbot page with full functionality"""
    st.title("📚 Education Chatbot")
    st.subheader(f"Welcome, {st.session_state.user_name}!")
    
    # Logout button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("Delete All Chats", use_container_width=True):
            if st.session_state.get("confirm_delete", False):
                # User confirmed deletion
                delete_all_user_chats(st.session_state.user_id)
                st.session_state.messages = []
                st.session_state.confirm_delete = False
                st.success("All chats deleted from database!")
                st.rerun()
            else:
                # Ask for confirmation
                st.session_state.confirm_delete = True
                st.warning("Click Delete All Chats again to confirm!")
                st.rerun()
    
    with col3:
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
    
    st.divider()
    
    # Initialize chat messages in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Load chat history from database
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
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your studies..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = process_user_query(st.session_state.user_id, prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


# ============================================================
# MAIN APPLICATION
# Routes to the correct page based on state
# ============================================================

def main():
    """Main application router"""
    
    # Check if user is logged in
    if st.session_state.logged_in:
        # Show chatbot page
        chatbot_page()
    else:
        # Check which page to show
        if st.session_state.current_page == "login":
            login_page()
        elif st.session_state.current_page == "signup":
            signup_page()
        else:
            # Default to login page
            login_page()


# Run the main application
if __name__ == "__main__":
    main()
