from flask import Flask
from flask_cors import CORS


def create_app():
    """This is an application factory"""
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def index():
        return "Hello World"

    return app
