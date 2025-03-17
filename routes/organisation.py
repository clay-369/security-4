from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from lib.model.enlistments import Enlistment
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
        research_item = dict(research_model.get_research_by_id(research_id))

        enlistment_model = Enlistment()
        enlistments = enlistment_model.get_enlistments_for_organisation(research_id)

        research_item['inschrijvingen'] = enlistments
        all_research_items.append(research_item)

    return all_research_items, 200


@organisation_bp.route('/onderzoeken/<research_id>', methods=['GET'])
@jwt_required()
def get_research_by_id(research_id):
    claims = get_jwt()
    if claims.get('account_type') != "organisation":
        return {"message": "You are not authorized to access this resource"}, 401

    research_model = Research()
    research_item = research_model.get_research_by_id(research_id)

    if not research_item:
        return {"message": "Onderzoek niet gevonden"}, 404

    organisation_id = claims['organisation_id']
    if research_item['organisatie_id'] != organisation_id:
        return {"message": "You don't have access to this item"}, 401

    research_item = dict(research_item)

    enlistment_model = Enlistment()
    enlistments = enlistment_model.get_enlistments_for_organisation(research_id)

    research_item['inschrijvingen'] = enlistments

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

    new_research_item = research_model.create_research(research_item, organisation_id)
    try:
        if new_research_item['error']:
            return new_research_item, 422

    except KeyError:
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
        return {"message": "Onderzoek succesvol bewerkt.", "success": True}, 200
    else:
        return {"error": "Onderzoek bewerken mislukt."}, 400
