# Code Reviewer Project

A Flask-based web application that provides AI-powered code review and analysis using Google's Gemini AI.

## Features

- User authentication and registration
- Code submission and analysis
- AI-powered code review with Gemini
- Programming language detection
- Code quality scoring
- Plagiarism detection hints
- Submission history tracking

## Tech Stack

- **Backend**: Flask, Flask-Login
- **Database**: Supabase (PostgreSQL)
- **AI**: Google Gemini AI
- **Deployment**: Vercel (Serverless)
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

## Deployment to Vercel

### Prerequisites

- Vercel account
- GitHub repository with your code
- Supabase account and project
- Google Gemini API key

### Deployment Steps

1. **Set up Supabase Database**
   - Create a Supabase project at [supabase.com](https://supabase.com)
   - Run the SQL script from `supabase_setup.sql` in the SQL Editor
   - Get your project URL and anon key from Settings → API

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project" → Import your Git repository
   - Vercel will automatically detect the configuration

3. **Configure Environment Variables**
   In Vercel dashboard, add these variables:
   ```
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_ANON_KEY=your-supabase-anon-key
   GEMINI_API_KEY=your-gemini-api-key
   SECRET_KEY=your-secret-key
   FLASK_ENV=production
   ```

For detailed deployment instructions, see `VERCEL_DEPLOYMENT.md`.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `FLASK_ENV` | Environment (production/development) | Yes |
| `SUPABASE_URL` | Supabase project URL | Yes (production) |
| `SUPABASE_ANON_KEY` | Supabase anon/public key | Yes (production) |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

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
├── vercel.json             # Vercel deployment config
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