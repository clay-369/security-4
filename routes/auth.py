from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_current_user

from lib.model.organisatie import Organisatie

auth_bp = Blueprint('auth', __name__)


# JWT API Authorization
@auth_bp.route('/api/organisaties/login', methods=['POST'])
def login_organisation():
    # Accepts {"naam": <name>, "wachtwoord": <password>} in JSON
    data = request.get_json()
    organisations_model = Organisatie()

    organisation_name = data['naam']
    password = data['wachtwoord']

    is_validated = organisations_model.validate_credentials(organisation_name, password)
    # Maybe set identity to email, so this can also be used for the experts
    # emails have to be unique in the db then
    # That would be good for sensitive information protection
    if is_validated:
        access_token = create_access_token(identity=organisation_name)
        refresh_token = create_refresh_token(identity=organisation_name)

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
    claims = get_jwt()
    return {"claims": claims}, 200