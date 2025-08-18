import os
from supabase import create_client, Client
from typing import Optional, Dict, Any, List
from datetime import datetime

class SupabaseManager:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        try:
            # Create client without proxy settings to avoid compatibility issues
            self.client: Client = create_client(
                supabase_url=self.supabase_url,
                supabase_key=self.supabase_key
            )
        except Exception as e:
            print(f"Supabase client initialization error: {e}")
            # Try alternative initialization method
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
            except Exception as e2:
                print(f"Alternative Supabase initialization failed: {e2}")
                raise
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            response = self.client.table('users').select('*').eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            response = self.client.table('users').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def create_user(self, name: str, email: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Create a new user"""
        try:
            user_data = {
                'name': name,
                'email': email,
                'password_hash': password_hash,
                'created_at': datetime.utcnow().isoformat()
            }
            response = self.client.table('users').insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_submissions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all submissions for a user"""
        try:
            response = self.client.table('code_submissions').select('*').eq('user_id', user_id).order('timestamp', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error getting user submissions: {e}")
            return []
    
    def create_submission(self, user_id: int, code_text: str, language: str = None, 
                         detected_language: str = None, feedback: str = None, 
                         ai_score: int = None, comments: str = None, 
                         plagiarism_hints: str = None) -> Optional[Dict[str, Any]]:
        """Create a new code submission"""
        try:
            submission_data = {
                'user_id': user_id,
                'code_text': code_text,
                'language': language,
                'detected_language': detected_language,
                'feedback': feedback,
                'ai_score': ai_score,
                'comments': comments,
                'plagiarism_hints': plagiarism_hints,
                'timestamp': datetime.utcnow().isoformat()
            }
            response = self.client.table('code_submissions').insert(submission_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating submission: {e}")
            return None
    
    def update_submission(self, submission_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a submission"""
        try:
            response = self.client.table('code_submissions').update(kwargs).eq('id', submission_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating submission: {e}")
            return None
    
    def get_submission_by_id(self, submission_id: int) -> Optional[Dict[str, Any]]:
        """Get submission by ID"""
        try:
            response = self.client.table('code_submissions').select('*').eq('id', submission_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting submission by ID: {e}")
            return None
    
    def get_all_submissions(self) -> List[Dict[str, Any]]:
        """Get all submissions (for admin purposes)"""
        try:
            response = self.client.table('code_submissions').select('*').order('timestamp', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error getting all submissions: {e}")
            return []

# Global instance
supabase_manager = None

def get_supabase_manager():
    """Get or create the global Supabase manager instance"""
    global supabase_manager
    if supabase_manager is None:
        try:
            supabase_manager = SupabaseManager()
        except Exception as e:
            print(f"Failed to initialize Supabase, using mock manager: {e}")
            from .dev_config import get_mock_supabase_manager
            supabase_manager = get_mock_supabase_manager()
    return supabase_manager 