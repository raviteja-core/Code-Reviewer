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
- **Deployment**: Render + Supabase
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

## Deployment to Render

### Prerequisites

- Render account
- GitHub repository with your code
- Supabase account and project
- Groq API key

### Deployment Steps

1. **Set up Supabase Database**
   - Create a Supabase project at [supabase.com](https://supabase.com)
   - Run the SQL script from `supabase_setup.sql` in the SQL Editor
   - Get your project URL and anon key from Settings → API

2. **Deploy to Render**
   - Push this repository to GitHub
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Select your GitHub repository
   - Render will read `render.yaml` and create the web service

3. **Configure Environment Variables**
   In the Render dashboard, add these variables:
   ```
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
   SUPABASE_ANON_KEY=your-supabase-anon-key
   GROQ_API_KEY=your-groq-api-key
   SECRET_KEY=your-secret-key
   FLASK_ENV=production
   ```

   `SUPABASE_SERVICE_ROLE_KEY` is recommended for server-side inserts and reads.

4. **Deploy**
   - Save the environment variables
   - Trigger the first deploy
   - Once the build finishes, open the Render URL

5. **Verify**
   - Visit `/healthz` and confirm you get `{"status":"ok"}`
   - Register a user
   - Submit a sample code review and confirm data is stored in Supabase

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `FLASK_ENV` | Environment (production/development) | Yes |
| `SUPABASE_URL` | Supabase project URL | Yes (production) |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase server-side key | Recommended |
| `SUPABASE_ANON_KEY` | Supabase anon/public key | Optional fallback |
| `GROQ_API_KEY` | Groq API key | Yes |

## Project Structure

```
codereviewer-project/
├── api/
│   ├── index.py           # Vercel serverless function
│   └── requirements.txt   # Python dependencies for API
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Data models
│   ├── supabase_config.py   # Supabase connection manager
│   ├── dev_config.py        # Mock database for development
│   ├── routes/              # Route blueprints
│   │   ├── auth.py          # Authentication routes
│   │   ├── dashboard.py     # Dashboard routes
│   │   └── code.py          # Code submission routes
│   ├── templates/           # HTML templates
│   └── utils/
│       └── ai_utils.py      # AI analysis utilities
├── instance/
│   └── config.py            # Configuration
├── supabase_setup.sql       # Database schema
├── requirements.txt         # Python dependencies
├── render.yaml             # Render deployment config
└── run.py                  # Application entry point
```

## API Endpoints

- `GET /` - Home page
- `GET /login` - Login page
- `POST /login` - Login form submission
- `GET /register` - Registration page
- `POST /register` - Registration form submission
- `GET /dashboard` - User dashboard
- `GET /submit` - Code submission page
- `POST /submit` - Submit code for analysis
- `GET /history` - Submission history
- `GET /feedback/<id>` - View specific feedback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository. 
