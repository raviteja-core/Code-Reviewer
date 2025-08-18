from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict, Any, Optional
from datetime import datetime

class User(UserMixin):
    def __init__(self, user_data: Dict[str, Any]):
        self.id = user_data.get('id')
        self.name = user_data.get('name')
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password_hash')
        self.created_at = user_data.get('created_at')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def from_dict(cls, user_data: Dict[str, Any]) -> 'User':
        return cls(user_data)

class CodeSubmission:
    def __init__(self, submission_data: Dict[str, Any]):
        self.id = submission_data.get('id')
        self.user_id = submission_data.get('user_id')
        self.code_text = submission_data.get('code_text')
        self.language = submission_data.get('language')
        self.detected_language = submission_data.get('detected_language')
        self.feedback = submission_data.get('feedback')
        self.ai_score = submission_data.get('ai_score')
        self.comments = submission_data.get('comments')
        self.plagiarism_hints = submission_data.get('plagiarism_hints')
        
        # Handle timestamp conversion
        timestamp = submission_data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                # Try to parse ISO format timestamp
                self.timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                try:
                    # Try to parse other common formats
                    self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # If all parsing fails, use current time
                    self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp or datetime.now()
    
    @classmethod
    def from_dict(cls, submission_data: Dict[str, Any]) -> 'CodeSubmission':
        return cls(submission_data) 