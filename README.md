# Code Reviewer Project

A Flask-based web application that provides AI-powered code review and analysis using Groq AI.

## Features

- User authentication and registration
- Code submission and analysis
- AI-powered code review with Groq
- Programming language detection
- Code quality scoring
- Plagiarism detection hints
- Submission history tracking

## Tech Stack

- **Backend**: Flask, Flask-Login
- **Database**: Supabase (PostgreSQL)
- **AI**: Groq AI (Model: openai/gpt-oss-120b)
- **Development**: Mock database for local testing

## Local Development

### Prerequisites

- Python 3.11+
- pip
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd codereviewer-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (Optional)**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

**Note**: For local development, the app uses a mock database. No external database setup is required. 
