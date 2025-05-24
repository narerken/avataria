import os

# Get the absolute path to the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session and CSRF protection
    SECRET_KEY = 'ava_tar'
    OPENAI_API_KEY = 'your_openAI_api_key'
    # SQLite database path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

    # Disable unnecessary tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directory to store uploaded files
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')

    # Maximum file upload size (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
