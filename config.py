# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///event_mgmt.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = 'Asia/Kolkata'
