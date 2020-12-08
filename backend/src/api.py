from flask import Blueprint, jsonify
#from flask_jwt_extended import jwt_required
#from src.models import db, User, Computer, PurchaseDetails

api = Blueprint("api", __name__)


@api.route("/devices", methods=["GET"])
def index():
    return "Devices Route!"
