from flask import Flask
from flask_login import LoginManager
from .models import User
from .supabase_config import get_supabase_manager
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
    # Initialize Supabase
    try:
        supabase_manager = get_supabase_manager()
        app.logger.info("Supabase connection established")
    except Exception as e:
        app.logger.error(f"Failed to initialize Supabase: {e}")
        app.logger.info("Running in development mode without database - set SUPABASE_URL and SUPABASE_ANON_KEY for full functionality")
        # Continue without Supabase for development/testing
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    # Register blueprints
    from .routes import auth, dashboard, code
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(code.bp)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            supabase_manager = get_supabase_manager()
            user_data = supabase_manager.get_user_by_id(int(user_id))
            if user_data:
                return User.from_dict(user_data)
            return None
        except Exception as e:
            app.logger.error(f"Error loading user: {e}")
            return None

    return app 