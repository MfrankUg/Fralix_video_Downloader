"""
WSGI entry point for Render deployment
This file is used by gunicorn to start the Flask application
"""
from app import app

# Gunicorn will look for a variable named 'application'
# We export the Flask app as 'application'
application = app

if __name__ == "__main__":
    application.run()

