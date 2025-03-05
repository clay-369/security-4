from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from lib.model.research import Research

organisation_bp = Blueprint('organisation', __name__)

@organisation_bp.get('/onderzoeken') # Test route
@jwt_required()
def get_research():
    claims = get_jwt()

    if claims.get('account_type') == "organisation":
        research_model = Research()
        result = research_model.get_all_research_items()
        return dict(result), 200

    return {"message": "You are not authorized to access this resource"}, 401