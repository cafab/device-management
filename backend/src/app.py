"""
app.py
- initializes the flask application
"""
from flask import Flask
from flask_cors import CORS
from src.models import db


def create_app():
    """This is an application factory"""
    app = Flask(__name__)
    app.config.from_object("src.config.BaseConfig")
    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return "Hello Fabio!"

    return app
