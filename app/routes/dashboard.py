from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import CodeSubmission
from ..supabase_config import get_supabase_manager

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    try:
        supabase_manager = get_supabase_manager()
        submissions_data = supabase_manager.get_user_submissions(current_user.id)
        # Convert to CodeSubmission objects and limit to 5
        recent_submissions = [CodeSubmission.from_dict(sub) for sub in submissions_data[:5]]
        return render_template('dashboard.html', submissions=recent_submissions)
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', submissions=[])

@bp.route('/')
def home():
    return render_template('home.html') 