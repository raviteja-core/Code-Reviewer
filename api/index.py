import sys
import os
from flask import Flask, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and create the Flask app
from app import create_app

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Vercel serverless function handler
def handler(request):
    # Create a simple WSGI environment
    environ = {
        'REQUEST_METHOD': request.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string or '',
        'SERVER_NAME': request.headers.get('host', 'localhost'),
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': request.body,
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': True,
        'HTTP_HOST': request.headers.get('host', 'localhost'),
    }
    
    # Add headers
    for key, value in request.headers.items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # WSGI response
    response_data = []
    response_headers = []
    status_code = [200]
    
    def start_response(status, headers, exc_info=None):
        status_code[0] = int(status.split()[0])
        response_headers.extend(headers)
        return response_data.append
    
    # Call Flask app
    with app.app_context():
        try:
            response = app(environ, start_response)
            response_body = b''.join(response)
            
            return Response(
                response_body,
                status=status_code[0],
                headers=dict(response_headers)
            )
            
        except Exception as e:
            return Response(
                f'Internal Server Error: {str(e)}',
                status=500,
                content_type='text/plain'
            )

# For local testing
if __name__ == '__main__':
    app.run(debug=True) 