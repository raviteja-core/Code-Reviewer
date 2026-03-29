import os
from dotenv import load_dotenv
load_dotenv()

ENVIRONMENT = os.getenv('FLASK_ENV', 'development').lower()
IS_PRODUCTION = ENVIRONMENT == 'production'

# Basic Flask configuration
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY and not IS_PRODUCTION:
    SECRET_KEY = 'dev-secret-key-change-in-production'

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# API Keys
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Production settings
if IS_PRODUCTION:
    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    PREFERRED_URL_SCHEME = 'https'

    # Disable debug mode in production
    DEBUG = False
else:
    DEBUG = True
