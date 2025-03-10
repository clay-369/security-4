from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from lib.model.organisation import Organisation
from lib.model.research import Research

organisation_bp = Blueprint('organisation', __name__)

# All routes for external organisation use

@organisation_bp.get('/onderzoeken') # Test route
@jwt_required()
def get_research():
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    research_model = Research()
    result = research_model.get_all_research_items()
    return dict(result), 200




@organisation_bp.post('/onderzoeken')
@jwt_required()
def create_research_item():
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    organisation_model = Organisation()


    research_item = request.json
    research_model = Research()

    new_research_item = research_model.create_research(research_item, 1)
    if not new_research_item:
        return {"message": "Could not create item", "success": False}, 500 # Server error

    return new_research_item, 201 # Created

