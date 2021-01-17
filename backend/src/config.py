"""
config.py
- settings for the flask application object
"""
import os


class BaseConfig:
    """Config parameters"""

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        default="postgresql://postgres:postgres@db:5432/postgres"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-JWT-Extended
    JWT_ACCESS_TOKEN_EXPIRES = 10  # 5 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 43200  # 12 hours
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_SECRET_KEY = "mysecretkey"  # CHANGE THE KEY!
