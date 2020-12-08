"""
jwt.py
- creates the JWT manager and processes each request before being consumed by the endpoints
in the api.py file.
"""
from flask import jsonify
from flask_jwt_extended import JWTManager
from src.blacklist import BLACKLIST


jwt = JWTManager()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Checks if a token has been blacklisted and will be called automatically when
    JWT_BLACKLIST_ENABLED is true. We add the token's unique identifier (jti) to the blacklist."""
    return decrypted_token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token():
    """Checks if a token has been revoked."""
    return (
        jsonify({"message": "The token has been revoked.", "error": "token_revoked"}),
        401,
    )


# The following callbacks are used for customizing jwt response/error messages.
@jwt.expired_token_loader
def expired_token():
    """Checks if a token has expired."""
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token(_):
    """Checks if a token is invalid."""
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token(_):
    """Checks if a token is missing."""
    return (
        jsonify(
            {
                "message": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh():
    """Checks if a token is not fresh."""
    return (
        jsonify(
            {"message": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )
