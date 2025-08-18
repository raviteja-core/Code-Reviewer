# Vercel Deployment Guide

This guide will help you deploy your Code Reviewer Flask application to Vercel.

## Prerequisites

1. A Vercel account (free tier available)
2. Your code pushed to a Git repository (GitHub, GitLab, etc.)
3. A Supabase account and project
4. A Gemini API key

## Setup Steps

### 1. Set Up Supabase Database

1. **Create a Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Sign up or log in to your account
   - Click "New Project"
   - Choose your organization and enter project details
   - Wait for the project to be created

2. **Set Up Database Tables**
   - In your Supabase dashboard, go to the SQL Editor
   - Copy and paste the contents of `supabase_setup.sql`
   - Run the SQL script to create the necessary tables

3. **Get Your Supabase Credentials**
   - Go to Settings → API in your Supabase dashboard
   - Copy your Project URL and anon/public key
   - These will be your `SUPABASE_URL` and `SUPABASE_ANON_KEY`

### 2. Prepare Your Repository

Make sure your code is pushed to a Git repository with the following files:
- `vercel.json` (Vercel configuration)
- `api/index.py` (Serverless function entry point)
- `api/requirements.txt` (Python dependencies for API)
- `app/` (Your Flask application)
- `supabase_setup.sql` (Database schema)

### 3. Deploy to Vercel

#### Option A: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add SUPABASE_URL
   vercel env add SUPABASE_ANON_KEY
   vercel env add GEMINI_API_KEY
   vercel env add SECRET_KEY
   ```

#### Option B: Deploy via Vercel Dashboard

1. **Connect Repository**
   - Go to [vercel.com](https://vercel.com)
   - Sign up or log in to your account
   - Click "New Project"
   - Import your Git repository

2. **Configure Project**
   - Vercel will automatically detect the `vercel.json` configuration
   - Set the following environment variables in the project settings:
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_ANON_KEY`: Your Supabase anon key
     - `GEMINI_API_KEY`: Your Gemini API key
     - `SECRET_KEY`: A secure random string for Flask sessions
     - `FLASK_ENV`: Set to "production"

3. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your application

### 4. Access Your Application

Once deployed, Vercel will provide you with a URL like:
`https://your-project-name.vercel.app`

## Environment Variables

Make sure to set these in your Vercel project settings:

- `SUPABASE_URL`: Your Supabase project URL (e.g., https://your-project.supabase.co)
- `SUPABASE_ANON_KEY`: Your Supabase anon/public key
- `GEMINI_API_KEY`: Your Gemini API key from Google AI Studio
- `SECRET_KEY`: A secure random string for Flask sessions
- `FLASK_ENV`: Set to "production"

## Vercel Configuration

The `vercel.json` file configures:

- **Builds**: Uses `@vercel/python` to build the Flask app
- **Routes**: Routes all requests to the serverless function
- **Functions**: Sets max duration to 30 seconds for AI processing
- **Environment**: Sets production environment

## File Structure for Vercel

```
codereviewer/
├── api/
│   ├── index.py           # Vercel serverless function
│   └── requirements.txt   # Python dependencies
├── app/
│   ├── __init__.py        # Flask app initialization
│   ├── models.py          # Data models
│   ├── supabase_config.py # Supabase connection manager
│   ├── dev_config.py      # Mock database for development
│   ├── routes/            # Flask routes
│   ├── templates/         # HTML templates
│   └── utils/             # Utility functions
├── instance/
│   └── config.py          # Configuration settings
├── supabase_setup.sql     # Database schema
├── vercel.json            # Vercel deployment config
└── requirements.txt       # Main Python dependencies
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check the build logs in Vercel dashboard
   - Ensure all dependencies are in `api/requirements.txt`
   - Verify Python version compatibility

2. **Environment Variable Issues**
   - Make sure all environment variables are set in Vercel
   - Check that variable names match exactly
   - Verify Supabase credentials are correct

3. **Function Timeout**
   - AI processing can take time
   - The function is configured for 30-second max duration
   - Consider optimizing AI calls for faster responses

4. **Database Connection Issues**
   - Verify your Supabase project is active
   - Check that the database schema is properly set up
   - Ensure your Supabase credentials are correct

### Performance Optimization

1. **Cold Starts**
   - Vercel functions have cold starts
   - Consider using Vercel Pro for better performance
   - Optimize imports and initialization

2. **AI Processing**
   - Gemini API calls can be slow
   - Consider implementing caching
   - Use async processing where possible

## Free Tier Limitations

- Vercel free tier includes:
  - 100GB bandwidth per month
  - 100GB function execution time per month
  - 10-second function timeout (upgraded to 30s in config)
  - Cold starts on function invocations

## Support

If you encounter issues:
1. Check Vercel's documentation
2. Review build and function logs
3. Verify all environment variables are set correctly
4. Ensure the database schema is properly set up in Supabase

## Alternative Deployment Options

If Vercel doesn't meet your needs, consider:
- **Render**: Better for long-running processes
- **Railway**: Good for full-stack applications
- **Heroku**: Traditional platform with more resources
- **DigitalOcean App Platform**: More control and resources 