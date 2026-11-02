# Education Chatbot for Grades 1-5

A simple chatbot to help Grade 1-5 students learn using educational documents.

## Project Structure
```
education_chat_bot/
├── education_data/          # Educational documents (already exists)
│   ├── Grade_1_English.txt
│   ├── Grade_1_Math.txt
│   ├── Grade_1_EVS.txt
│   └── ... (other grades)
├── app_data/               # Application data
├── config.json             # Application configuration
├── subjects.json           # Grades and subjects
├── database.sql            # Supabase database schema
├── .env                    # API keys (not in git)
├── .env.example            # Example .env file
├── requirements.txt        # Python libraries
└── app.py                  # Main Streamlit application
```

## Setup Instructions

### Step 1: Install Python Libraries
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Add your Supabase URL and Key
3. Add your OpenAI API Key

### Step 3: Create Supabase Tables
1. Go to your Supabase project dashboard
2. Open SQL Editor
3. Copy and execute the contents of `database.sql`

### Step 4: Run the Application
```bash
streamlit run app.py
```
