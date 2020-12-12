"""
app.py
- initializes the flask application
"""
from flask import Flask
from flask_cors import CORS
from src.jwt import jwt
from src.models import db
from src.api import api


def create_app():
    """This is an application factory"""
    app = Flask(__name__)
    app.config.from_object("src.config.BaseConfig")
    CORS(app)
    jwt.init_app(app)
    db.init_app(app)
    app.register_blueprint(api, url_prefix="/api")

    return app
