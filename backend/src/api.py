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
    PurchaseDetails,
    Accounts, 
)
from src.schemas import (
    ComputerSchema, 
    PurchaseDetailsSchema,
)
from src.jwt import blacklist
from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHash,
    VerificationError,
    VerifyMismatchError,
)

from pprint import pprint

api = Blueprint("api", __name__)


@api.route("/script-device", methods=["POST"])
#@jwt_required()
def post_script_device():
    data = request.get_json()
    print(str(type(data['hard_disk'])), flush=True)

    computer = Computer.query.filter_by(serial_number=data['serial_number']).first()

    if not computer:
        """Virtualbox serial number is 0 => take computer name as serial number instead."""
        if data['serial_number'] == "0":
            data['serial_number'] = data['computer_name']

        """Create computer object."""
        computer = Computer(
            computer_name = data["computer_name"],
            ip_address = data["ip_addresses"],
            os = data["os"],
            os_install_date = data["os_install_date"],
            serial_number = data["serial_number"],
            computer_model = data["computer_model"],
            cpu = data["cpu"],
            memory = data["memory"],
            hard_disk = data["hard_disk"]
        )

        """Create account information."""
        account = Accounts(
            current_account = data["user"],
            previous_account = None,
            last_seen = data["last_seen"],
            computer = computer
        )
    else:
        """Update computer object."""
        computer.computer_name = data["computer_name"],
        computer.ip_address = data["ip_addresses"],
        computer.os = data["os"],
        computer.os_install_date = data["os_install_date"],
        computer.serial_number = data["serial_number"],
        computer.computer_model = data["computer_model"],
        computer.cpu = data["cpu"],
        computer.memory = data["memory"],
        computer.hard_disk = data["hard_disk"]
        
        """Update account information."""
        account = Accounts.query.filter_by(computer_sn=data["serial_number"]).first()

        if account.current_account != data['user']:
            account.previous_account = account.current_account
            
        account.current_account = data["user"]
        account.last_seen = data['last_seen']
    
    db.session.add_all([computer, account])
    db.session.commit()

    return jsonify({"message": "Computer successfully created."}), 201


@api.route("/devices", methods=["GET"])
@jwt_required()
def get_devices():
    devices = Computer.query.all()
    json_data = ComputerSchema(many=True).dump(devices)

    if not devices:
        return jsonify({"message": "No devices available."}), 200
    
    return jsonify({"devices": json_data}), 200


@api.route("/purchase-details", methods=["POST"])
@jwt_required()
def post_purchase_details():
    data = request.get_json()
    data_load = PurchaseDetailsSchema().load(data)
    print(str(data_load), flush=True)

    computer = Computer.query.filter_by(serial_number=data_load['serial_number']).first()

    if not computer:
        return jsonify({"message": "Computer does not exist."}), 400

    purchase_details = PurchaseDetails(
        supplier = data_load['supplier'],
        price = data_load['price'],
        purchase_date = data_load['purchase_date'],
        notes = data_load['notes'],
        computer = computer
    )
    db.session.add(purchase_details)
    db.session.commit()

    return jsonify({"message": "Purchase details successfully created."}), 201


@api.route("/purchase-details", methods=["PUT"])
@jwt_required()
def put_purchase_details():
    data = request.get_json()
    data_load = PurchaseDetailsSchema().load(data)
    print(str(data_load), flush=True)
    purchase_details = PurchaseDetails.query.filter_by(id=data_load['id']).first()
    

    if not purchase_details:
        return jsonify({"message": "Purchase details do not exist."}), 400

       
    purchase_details.supplier = data_load['supplier']
    purchase_details.price = data_load['price']
    purchase_details.purchase_date = data_load['purchase_date']
    purchase_details.notes = data_load['notes']
    
    db.session.add(purchase_details)
    db.session.commit()

    return jsonify({"message": "Purchase details successfully updated."}), 200



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