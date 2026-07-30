from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from ..supabase_config import get_supabase_manager

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        try:
            supabase_manager = get_supabase_manager()
            
            # Check if user already exists
            existing_user = supabase_manager.get_user_by_email(email)
            if existing_user:
                current_app.logger.warning(f"Registration attempt with existing email: {email}")
                flash('Email already registered.')
                return redirect(url_for('auth.register'))
            
            # Create new user
            user = User({'name': name, 'email': email})
            user.set_password(password)
            
            # Save to Supabase
            user_data = supabase_manager.create_user(name, email, user.password_hash)
            if user_data:
                current_app.logger.info(f"User registered successfully: {email}")
                flash('Registration successful. Please log in.')
                return redirect(url_for('auth.login'))
            else:
                current_app.logger.error(f"Failed to create user record in DB: {email}")
                flash('Registration failed. Please try again.')
                
        except Exception as e:
            current_app.logger.error(f"Registration error for {email}: {e}")
            flash('Registration failed. Please try again.')
            
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            supabase_manager = get_supabase_manager()
            user_data = supabase_manager.get_user_by_email(email)
            
            if user_data:
                user = User.from_dict(user_data)
                if user.check_password(password):
                    login_user(user)
                    current_app.logger.info(f"User logged in successfully: {email}")
                    return redirect(url_for('dashboard.dashboard'))
            
            current_app.logger.warning(f"Failed login attempt for email: {email}")
            flash('Invalid email or password.')
            
        except Exception as e:
            current_app.logger.error(f"Login error for {email}: {e}")
            flash('Login failed. Please try again.')
            
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    user_email = getattr(current_user, 'email', 'Unknown')
    logout_user()
    current_app.logger.info(f"User logged out: {user_email}")
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))