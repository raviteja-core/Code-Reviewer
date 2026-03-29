import os

from flask import Flask, jsonify
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

from .models import User
from .supabase_config import get_supabase_manager
from dotenv import load_dotenv


def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    is_production = app.config.get('ENVIRONMENT') == 'production'
    if is_production and not app.config.get('SECRET_KEY'):
        raise RuntimeError('SECRET_KEY must be set in production.')

    # Initialize Supabase
    try:
        get_supabase_manager()
        app.logger.info("Supabase connection established")
    except Exception as e:
        if is_production:
            raise RuntimeError(f"Failed to initialize Supabase in production: {e}") from e
        app.logger.warning(
            "Supabase unavailable in development; using mock database manager instead."
        )

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

    @app.get('/healthz')
    def healthcheck():
        return jsonify({"status": "ok"}), 200

    return app
