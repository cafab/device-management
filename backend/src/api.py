from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from src.models import (
    db, 
    User, 
    Computer,
    Accounts, 
    PurchaseDetails, 
    ComputerSchema, 
    PurchaseDetailsSchema
)
from src.jwt import blacklist
from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHash,
    VerificationError,
    VerifyMismatchError,
)

api = Blueprint("api", __name__)


@api.route("/script-device", methods=["POST"])
#@jwt_required()
def post_script_device():
    data = request.get_json()
    computer = Computer.query.filter_by(serial_number=data['serialNumber']).first()

    if not computer:
        """Create new Computer object"""
        computer = Computer(
            computer_name = data["computerName"],
            ip_address = data["ipAddresses"],
            timestamp = data["timestamp"],
            os = data["os"],
            os_install_date = data["osInstallDate"],
            serial_number = data["serialNumber"],
            computerModel = data["computerModel"],
            cpu = data["cpu"],
            memory = data["memory"],
            hardDisk = data["hardDisk"]
        )

        account = Accounts(
            current_account = data["user"],
            previous_account = None,
            computer = computer
        )

        db.session.add_all([computer, account])
        db.session.commit()
    else:
        computer.timestamp = data['timestamp']
        account = Accounts.query.filter_by(computer_sn=data["serialNumber"]).first()
        account.previous_account = account.current_account
        account.current_account = data["user"]

        db.session.add_all([computer, account])
        db.session.commit()

    json_data = ComputerSchema().dump(computer)
    
    return jsonify({"purchase_details": json_data}), 200


@api.route("/devices", methods=["GET"])
@jwt_required()
def get_devices():
    devices = Computer.query.all()
    json_data = ComputerSchema(many=True).dump(devices)

    if not devices:
        return jsonify({"message": "No devices available"}), 200
    
    return jsonify({"devices": json_data}), 200


@api.route("/edit-device", methods=["PUT"])
@jwt_required()
def put_edit_devices():
    data = request.get_json()

    purchase_details = PurchaseDetails.query.filter_by(computer_sn=data['serial_number']).first()
    json_data = PurchaseDetailsSchema().dump(purchase_details)

    if not purchase_details:
        return jsonify({"message": "No such purchase details found."}), 400
    
    purchase_details.supplier = data['supplier']
    purchase_details.price = data['price']
    purchase_details.purchase_date = data['purchase_date']
    purchase_details.notes = data['notes']

    db.session.add(purchase_details)
    db.session.commit()
    
    return jsonify({"purchase_details": json_data}), 200



@api.route("/login", methods=["POST"])
def login():
    """Retrieve a token"""
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    try:
        hasher = PasswordHasher()
        hasher.verify(user.password, data["password"])
    except (VerifyMismatchError, VerificationError, InvalidHash, AttributeError):
        # This must also return 401 or else the user may learn
        # private information
        return jsonify({"message": "Invalid credentials"}), 401

    # Rehash password if the parameters of the PasswordHasher change.
    # https://argon2-cffi.readthedocs.io/en/stable/api.html
    if hasher.check_needs_rehash(user.password):
        user.password = hasher.hash(data["password"])
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=user.username, fresh=True)
    refresh_token = create_refresh_token(user.username)
    
    return (
        jsonify({"access_token": access_token, "refresh_token": refresh_token}),
        200
    )


@api.route("/check-logged-in", methods=["GET"])
@jwt_required()
def get_check_logged_in():
    return ""


# Blacklist the access token when the user logs out
@api.route("/revoke-access-token", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    """Endpoint for revoking the current users access token."""
    jti = get_jwt()["jti"]
    blacklist.add(jti)

    return dict(message="Successfully revoked access token")


# Blacklist the refresh token when the user logs out
@api.route("/revoke-refresh-token", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    """Endpoint for revoking the current users refresh token."""
    jti = get_jwt()["jti"]
    blacklist.add(jti)

    return dict(message="Successfully revoked refresh token")


@api.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh token endpoint in order to get a new access token.
    A blacklisted refresh token will not be able to access this endpoint."""
    username = get_jwt_identity()
    # Refreshed tokens have the argument fresh=False, because a refresh token
    # is only fresh after the user successfully provided his credentials.
    return dict(access_token=create_access_token(identity=username, fresh=False))