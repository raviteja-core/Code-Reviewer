"""
Development configuration for when Supabase is not available
"""
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

class MockSupabaseManager:
    """Mock Supabase manager for development without database"""
    
    def __init__(self):
        self.users = {}
        self.submissions = {}
        self.next_user_id = 1
        self.next_submission_id = 1
        print("Running in development mode with mock database")
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        for user in self.users.values():
            if user['email'] == email:
                return user
        return None
    
    def create_user(self, name: str, email: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Create a new user"""
        user_data = {
            'id': self.next_user_id,
            'name': name,
            'email': email,
            'password_hash': password_hash,
            'created_at': datetime.utcnow()
        }
        self.users[self.next_user_id] = user_data
        self.next_user_id += 1
        return user_data
    
    def get_user_submissions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all submissions for a user"""
        return [sub for sub in self.submissions.values() if sub['user_id'] == user_id]
    
    def create_submission(self, user_id: int, code_text: str, language: str = None, 
                         detected_language: str = None, feedback: str = None, 
                         ai_score: int = None, comments: str = None, 
                         plagiarism_hints: str = None) -> Optional[Dict[str, Any]]:
        """Create a new code submission"""
        submission_data = {
            'id': self.next_submission_id,
            'user_id': user_id,
            'code_text': code_text,
            'language': language,
            'detected_language': detected_language,
            'feedback': feedback,
            'ai_score': ai_score,
            'comments': comments,
            'plagiarism_hints': plagiarism_hints,
            'timestamp': datetime.utcnow()
        }
        self.submissions[self.next_submission_id] = submission_data
        self.next_submission_id += 1
        return submission_data
    
    def update_submission(self, submission_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a submission"""
        if submission_id in self.submissions:
            self.submissions[submission_id].update(kwargs)
            return self.submissions[submission_id]
        return None
    
    def get_submission_by_id(self, submission_id: int) -> Optional[Dict[str, Any]]:
        """Get submission by ID"""
        return self.submissions.get(submission_id)
    
    def get_all_submissions(self) -> List[Dict[str, Any]]:
        """Get all submissions"""
        return list(self.submissions.values())

def get_mock_supabase_manager():
    """Get mock Supabase manager for development"""
    return MockSupabaseManager() 