#!/usr/bin/env python3
"""
Test script for Vercel deployment
This script tests the serverless function locally
"""

import sys
import os
from unittest.mock import Mock

# Add the api directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

def test_vercel_function():
    """Test the Vercel serverless function"""
    try:
        from index import handler
        
        # Create a mock request
        mock_request = Mock()
        mock_request.method = 'GET'
        mock_request.path = '/'
        mock_request.query_string = ''
        mock_request.body = b''
        mock_request.headers = {
            'host': 'localhost:3000',
            'user-agent': 'test-agent'
        }
        
        # Call the handler
        response = handler(mock_request)
        
        print("✅ Vercel function test passed!")
        print(f"Response status: {response.status}")
        print(f"Response headers: {response.headers}")
        
        return True
        
    except Exception as e:
        print(f"❌ Vercel function test failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing Vercel serverless function...")
    success = test_vercel_function()
    
    if success:
        print("\n🎉 Your Flask app is ready for Vercel deployment!")
        print("Next steps:")
        print("1. Push your code to a Git repository")
        print("2. Connect your repository to Vercel")
        print("3. Set up your environment variables")
        print("4. Deploy!")
    else:
        print("\n⚠️  Please fix the issues before deploying to Vercel") 