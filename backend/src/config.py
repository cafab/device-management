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
