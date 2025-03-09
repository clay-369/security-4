from flask import Blueprint, request
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required, current_user,
                                get_jwt_identity, get_jwt)

from lib.model.organisation import Organisation
from lib.model.token_blocklist import TokenBlocklist

auth_bp = Blueprint('auth', __name__)



# JWT API Authorization
@auth_bp.route('/organisatie/login', methods=['POST'])
def login_organisation():
    # Accepts {"email": <email>, "password": <password>} in JSON
    data = request.get_json()
    organisations_model = Organisation()

    email = data['email']
    password = data['password']

    is_validated = organisations_model.validate_credentials(email, password)

    if is_validated:
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        return {
            "message": "Login successful",
            "tokens": {
                "access": access_token,
                "refresh": refresh_token,
            }
        }, 200

    return {"error": "Invalid credentials"}, 401


@auth_bp.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    user_details =  dict(current_user)
    user_details.pop('wachtwoord') # Dont show password
    return {"user_details": user_details}, 200


@auth_bp.route('/refresh', methods=['GET'])
@jwt_required(refresh=True) # Accepts refresh token, not access token
def refresh_access_token():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return {"access_token": new_access_token}, 200


@auth_bp.route('/organisatie/logout', methods=['GET'])
@jwt_required(verify_type=False)
def logout_organisation():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_blocklist_model = TokenBlocklist()
    token_blocklist_model.add_token(jti)

    return {"message": f"Successfully revoked {token_type} token"}, 200