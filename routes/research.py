from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from lib.model.experts import Experts
from lib.model.research import Research
from lib.model.enlistments import Enlistment
research_bp = Blueprint('research', __name__)

# API's
## Research Items
@research_bp.route('/api/onderzoeken', methods=['GET'])
@jwt_required()
def get_research_items():
    # This route is for experts, so it only gets research items that are available and are accepted by admin
    claims = get_jwt()
    if claims.get('account_type') != "expert":
        return {"message": "You are not authorized to access this resource"}, 401

    research_model = Research()

    expert_model = Experts()
    expert = expert_model.get_expert_by_email(get_jwt_identity())
    date_of_birth = expert['geboortedatum']
    age = expert_model.calculate_age(date_of_birth)


    disability_ids = expert_model.get_disabilities(expert['deskundige_id'])

    all_research_items = research_model.get_all_available_research_items(age, disability_ids)

    formatted_research_items = []
    for research_item in all_research_items:
        formatted_research_item = research_model.format_research_item(research_item)
        formatted_research_items.append(formatted_research_item)

    return formatted_research_items, 200


@research_bp.get('/api/onderzoeken/<research_id>')
@jwt_required()
def get_research_item(research_id):
    claims = get_jwt()
    if claims.get('account_type') != "expert":
        return {"message": "You are not authorized to access this resource"}, 401

    research_model = Research()
    research_item = dict(research_model.get_research_by_id(int(research_id)))
    formatted_research_item = research_model.format_research_item(research_item)
    return formatted_research_item


## Enlistments
@research_bp.route('/api/onderzoeken/inschrijvingen', methods=['POST'])
@jwt_required()
def create_enlistment():
    claims = get_jwt()
    if claims.get('account_type') != "expert":
        return {"message": "You are not authorized to access this resource"}, 401

    expert_id = claims.get('expert_id')
    research_id = request.json['research_id']

    enlistment_model = Enlistment()

    new_enlistment_id = enlistment_model.create_enlistment(research_id=research_id, expert_id=expert_id)
    new_enlistment = enlistment_model.get_enlistment_by_id(new_enlistment_id)

    return new_enlistment, 201


@research_bp.route('/api/onderzoeken/inschrijvingen', methods=['DELETE'])
@jwt_required()
def delete_enlistment():
    claims = get_jwt()
    if claims.get('account_type') != "expert":
        return {"message": "You are not authorized to access this resource"}, 401

    expert_id = claims.get('expert_id')

    research_id = request.json['research_id']
    enlistment_model = Enlistment()
    deleted_item = enlistment_model.delete_enlistment(expert_id, research_id)

    return deleted_item, 200


@research_bp.route('/api/onderzoeken/inschrijvingen/deskundige', methods=['GET'])
@jwt_required()
def get_all_enlistments_by_expert():
    claims = get_jwt()
    if claims.get('account_type') != "expert":
        return {"message": "You are not authorized to access this resource"}, 401

    expert_id = claims.get('expert_id')

    search_words = ""
    if request.args.get('search'):
        search_words = request.args.get('search')

    enlistment_model = Enlistment()
    all_enlistments = enlistment_model.get_formatted_enlistments_by_expert(expert_id, search_words)
    return all_enlistments, 200

