import os
from dotenv import load_dotenv

load_dotenv()

# Flask‑WTF will automatically use the main secret_key for generating and validating csrf tokens unless specified with:
# WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', 'another-secret-key')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'SessionLoginCookieSecurity&antiCSRFformAttack')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_dev_secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOCKETIO_MESSAGE_QUEUE = os.getenv('SOCKETIO_MESSAGE_QUEUE', 'redis://')
    LOG_FILE = os.getenv('LOG_FILE', 'server.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10 * 1024 * 1024))  # 10 Mo
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    CLIENT_TIMEOUT = int(os.getenv('CLIENT_TIMEOUT', 180))  # secondes
    ROOM_TIMEOUT = int(os.getenv('ROOM_TIMEOUT', 300))  # secondes
    MAX_PLAYERS_PER_ROOM = int(os.getenv('MAX_PLAYERS_PER_ROOM', 5))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'production')
    SESSION_COOKIE_SAMESITE='Strict'
    SESSION_COOKIE_SECURE=True
    SESSION_COOKIE_HTTPONLY=True
    REMEMBER_COOKIE_SAMESITE = 'Strict'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
