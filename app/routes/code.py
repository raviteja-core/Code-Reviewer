from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..models import CodeSubmission
from ..utils.ai_utils import analyze_code_with_gemini
from ..supabase_config import get_supabase_manager
import os

bp = Blueprint('code', __name__)

@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_code():
    if request.method == 'POST':
        code_text = request.form.get('code_text', '').strip()
        language = request.form.get('language', 'python')
        
        if not code_text:
            flash('Please enter some code to review.')
            return redirect(url_for('code.submit_code'))
        
        # Analyze code with Gemini API
        try:
            feedback, score, comments = analyze_code_with_gemini(code_text, language)
            
            # Get detected language for storage
            from ..utils.ai_utils import detect_language
            detected_lang = detect_language(code_text)
            
            # Create submission in Supabase
            supabase_manager = get_supabase_manager()
            submission_data = supabase_manager.create_submission(
                user_id=current_user.id,
                code_text=code_text,
                language=language,
                detected_language=detected_lang if detected_lang != 'unknown' else None,
                feedback=feedback,
                ai_score=score,
                comments=comments
            )
            
            if submission_data:
                # Check if this was a fallback analysis
                if "basic analysis" in feedback.lower() or "note: this is a basic analysis" in feedback.lower():
                    flash('⚠️ AI service was temporarily unavailable. Showing basic analysis instead.')
                
                return redirect(url_for('code.view_feedback', submission_id=submission_data['id']))
            else:
                flash('❌ Error saving submission. Please try again.')
                return redirect(url_for('code.submit_code'))
            
        except Exception as e:
            error_message = str(e)
            if "quota exceeded" in error_message.lower():
                flash(f'⚠️ {error_message}')
            elif "API key" in error_message.lower():
                flash(f'❌ {error_message}')
            else:
                flash(f'❌ Error analyzing code: {error_message}')
            return redirect(url_for('code.submit_code'))
    
    return render_template('submit_code.html')

@bp.route('/feedback/<int:submission_id>')
@login_required
def view_feedback(submission_id):
    try:
        supabase_manager = get_supabase_manager()
        submission_data = supabase_manager.get_submission_by_id(submission_id)
        
        if not submission_data or submission_data['user_id'] != current_user.id:
            flash('Submission not found.')
            return redirect(url_for('dashboard.dashboard'))
        
        submission = CodeSubmission.from_dict(submission_data)
        return render_template('feedback.html', submission=submission)
    except Exception as e:
        flash('Error loading submission.')
        return redirect(url_for('dashboard.dashboard'))

@bp.route('/history')
@login_required
def history():
    try:
        supabase_manager = get_supabase_manager()
        all_submissions_data = supabase_manager.get_user_submissions(current_user.id)
        
        # Convert to CodeSubmission objects
        all_submissions = [CodeSubmission.from_dict(sub) for sub in all_submissions_data]
        
        # Apply filters
        language_filter = request.args.get('language', '')
        score_filter = request.args.get('score', '')
        
        filtered_submissions = all_submissions
        
        if language_filter:
            filtered_submissions = [s for s in filtered_submissions if s.language == language_filter]
        
        if score_filter:
            if score_filter == 'high':
                filtered_submissions = [s for s in filtered_submissions if s.ai_score and s.ai_score >= 80]
            elif score_filter == 'medium':
                filtered_submissions = [s for s in filtered_submissions if s.ai_score and 50 <= s.ai_score < 80]
            elif score_filter == 'low':
                filtered_submissions = [s for s in filtered_submissions if s.ai_score and s.ai_score < 50]
        
        # Simple pagination
        page = request.args.get('page', 1, type=int)
        per_page = 10
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        submissions_page = filtered_submissions[start_idx:end_idx]
        total_pages = (len(filtered_submissions) + per_page - 1) // per_page
        
        # Create a simple pagination object
        class SimplePagination:
            def __init__(self, items, page, per_page, total):
                self.items = items
                self.page = page
                self.per_page = per_page
                self.total = total
                self.pages = (total + per_page - 1) // per_page
                self.has_prev = page > 1
                self.has_next = page < self.pages
                self.prev_num = page - 1 if self.has_prev else None
                self.next_num = page + 1 if self.has_next else None
        
        pagination = SimplePagination(
            submissions_page, page, per_page, len(filtered_submissions)
        )
        
        return render_template('history.html', submissions=pagination, 
                             language_filter=language_filter, score_filter=score_filter)
    except Exception as e:
        print(f"History error: {e}")
        return render_template('history.html', submissions=None, 
                             language_filter='', score_filter='') 