from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from lib.model.organisation import Organisation
from lib.model.research import Research

organisation_bp = Blueprint('organisation', __name__)


# All routes for external organisation use

@organisation_bp.route('/onderzoeken', methods=['GET'])  # Test route
@jwt_required()
def get_research():
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    organisation_id = claims['organisation_id']

    research_model = Research()
    all_ids = research_model.get_all_research_ids_by_organisation_id(organisation_id)
    if not all_ids:
        return {"message": "Geen onderzoeken gevonden voor deze organisatie"}, 404

    all_research_ids = [row['onderzoek_id'] for row in all_ids]

    all_research_items = []

    for research_id in all_research_ids:
        research_item = research_model.get_all_information(research_id)
        all_research_items.append(research_item)

    return all_research_items, 200


@organisation_bp.route('/onderzoeken/<research_id>', methods=['GET'])
@jwt_required()
def get_research_by_id(research_id):
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    organisation_id = claims['organisation_id']

    research_model = Research()

    valid_id = research_model.get_organisation_by_id(research_id)
    if not valid_id:
        return {"message": "Dit onderzoek bestaat niet"}, 404

    valid_id = dict(valid_id)['organisatie_id']

    is_validated = (valid_id == organisation_id)
    if not is_validated:
        return {"message": "U heeft geen toegang tot dit onderzoek"}, 401

    research_item = research_model.get_all_information(research_id)

    return research_item, 200


@organisation_bp.route('/onderzoeken', methods=['POST'])
@jwt_required()
def create_research_item():
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    organisation_id = claims['organisation_id']

    research_item = request.json
    research_model = Research()

    new_research_id = research_model.create_research(research_item, organisation_id)
    try:
        return new_research_id['error'], 422

    except TypeError:
        new_research_item = research_model.get_all_information(new_research_id)
        return new_research_item, 201  # Created


@organisation_bp.route('/onderzoeken/<research_id>', methods=['PUT'])
@jwt_required()
def edit_research(research_id):
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    organisation_id = claims['organisation_id']

    research = request.get_json()

    research_model = Research()

    # Check if research item belongs to this organisation
    if organisation_id != research_model.get_organisation_id(research_id):
        return {"message": "You are not authorized to access this resource"}, 401

    is_edited = research_model.edit_research(research, research_id)
    if is_edited:
        edited_research = research_model.get_all_information(research_id)
        return {"message": "Onderzoek succesvol bewerkt.", "success": True, "onderzoek": edited_research}, 200
    else:
        return {"error": "Onderzoek bewerken mislukt."}, 400


@organisation_bp.route('/organisatie', methods=['PUT'])
@jwt_required()
def edit_organisation():
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    organisation_id = claims['organisation_id']
    data = request.get_json()

    organisation_model = Organisation()
    is_edited = organisation_model.edit_organisation(organisation_id, data)
    if not is_edited:
        return {"message": "Organisatie kon niet bewerkt worden."}, 400

    edited_organisation = dict(organisation_model.get_organisation_by_email(data['email']))
    edited_organisation.pop('wachtwoord')

    return {"message": "Organisatie succesvol bewerkt.", "organisatie": edited_organisation}, 200

