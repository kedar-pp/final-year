import os

class Config:
    SECRET_KEY = 'your_secret_key_here'  # Used for session security
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:password123@localhost/parking_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
