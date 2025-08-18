import os
from dotenv import load_dotenv
load_dotenv()

# Basic Flask configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Production settings
if os.getenv('FLASK_ENV') == 'production':
    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Disable debug mode in production
    DEBUG = False
else:
    DEBUG = True 