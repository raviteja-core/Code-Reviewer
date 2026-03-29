# Setup Guide for Code Reviewer

This guide will help you set up and run the Code Reviewer application.

## Local Development Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables (Optional for Development)

Create a `.env` file in the root directory with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Supabase Configuration (Optional for development)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key-here

# API Keys
GROQ_API_KEY=your-groq-api-key-here
```

**Note**: For local development, you can run the app without Supabase credentials. It will use a mock database that stores data in memory.

### 3. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Production Deployment

### 1. Set Up Supabase Database

1. Create a Supabase account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to the SQL Editor and run the contents of `supabase_setup.sql`
4. Get your project URL and anon key from Settings → API

### 2. Deploy to Render

1. Push your code to a Git repository
2. Go to [render.com](https://render.com) and create a new Blueprint service
3. Import your Git repository
4. Add the following environment variables:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase service role key
   - `SUPABASE_ANON_KEY`: Your Supabase anon key
   - `GROQ_API_KEY`: Your Groq API key
   - `SECRET_KEY`: A secure random string for sessions
   - `FLASK_ENV`: Set to "production"

5. Deploy and verify `https://your-service.onrender.com/healthz`

## Features

### Development Mode (No Supabase)
- Mock database stores data in memory
- All features work for testing
- Data is lost when the application restarts

### Production Mode (With Supabase)
- Persistent database storage
- Real-time capabilities
- Scalable and secure

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'supabase'**
   - Run: `pip install supabase`

2. **Supabase connection errors**
   - Check your `SUPABASE_URL` and `SUPABASE_ANON_KEY`
   - Ensure your Supabase project is active

3. **Groq API errors**
   - Verify your `GROQ_API_KEY` is correct
   - Check your API quota

### Getting API Keys

1. **Groq API Key**:
   - Go to [Groq Console](https://console.groq.com/keys)
   - Create a new API key

2. **Supabase Credentials**:
   - Go to your Supabase project dashboard
   - Navigate to Settings → API
   - Copy the Project URL and anon/public key

## File Structure

```
codereviewer/
├── api/
│   ├── index.py           # Alternate serverless entrypoint
│   └── requirements.txt   # Python dependencies for API
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Data models
│   ├── supabase_config.py   # Supabase connection manager
│   ├── dev_config.py        # Mock database for development
│   ├── routes/              # Flask routes
│   ├── templates/           # HTML templates
│   └── utils/               # Utility functions
├── instance/
│   └── config.py            # Configuration settings
├── supabase_setup.sql       # Database schema
├── requirements.txt         # Python dependencies
├── render.yaml             # Render deployment config
└── run.py                  # Application entry point
```
