from flask import Blueprint, render_template, request

from lib.model.organisatie import Organisatie
from lib.model.research import Research
from lib.model.enlistments import Enlistment

research_bp = Blueprint('research', __name__)

# API's
## Research Items
@research_bp.route('/api/onderzoeken', methods=['GET'])
def get_research_items():
    # This route is for experts, so it only gets research items that are available and are accepted by admin
    research_model = Research()

    search_words = ""
    if request.args.get('search'):
        search_words = request.args.get('search')

    all_research_items = research_model.get_all_available_research_items()

    formatted_research_items = []
    for research_item in all_research_items:
        formatted_research_item = research_model.format_research_item(research_item)
        formatted_research_items.append(formatted_research_item)

    return formatted_research_items, 200


@research_bp.route('/api/onderzoeken', methods=['POST'])
def create_research_item():
    organisation_model = Organisatie()

    research_item = request.json
    token = request.authorization
    print(token)
    # Authorization
    is_authorized = organisation_model.validate_api_token(token, research_item['organisatie_id'])
    if is_authorized:
        research_model = Research()

        new_research_id = research_model.create_research(research_item)
        if not new_research_id:
            return {"message": "Could not create item", "success": False}, 500 # Server error

        new_research_item = research_model.get_research_by_id(new_research_id)

        return dict(new_research_item), 201 # Created

    return {"message": "Invalid API key", "success": False}, 401 # Unauthorized


@research_bp.get('/api/onderzoeken/<research_id>')
def get_research_item(research_id):
    research_model = Research()
    research_item = research_model.get_research_by_id(int(research_id))
    formatted_research_item = research_model.format_research_item(research_item)
    return formatted_research_item


## Enlistments

@research_bp.route('/api/onderzoeken/inschrijvingen', methods=['POST'])
def create_enlistment():
    enlistment_model = Enlistment()

    research_id = request.json['research_id']
    expert_id = request.json['expert_id']

    new_enlistment_id = enlistment_model.create_enlistment(research_id=research_id, expert_id=expert_id)
    new_enlistment = enlistment_model.get_enlistment_by_id(new_enlistment_id)

    return new_enlistment, 201


@research_bp.route('/api/onderzoeken/inschrijvingen', methods=['DELETE'])
def delete_enlistment():
    expert_id = request.json['expert_id']
    research_id = request.json['research_id']
    enlistment_model = Enlistment()
    deleted_item = enlistment_model.delete_enlistment(expert_id, research_id)

    return deleted_item, 200


@research_bp.route('/api/onderzoeken/inschrijvingen/<expert_id>', methods=['GET'])
def get_all_enlistments_by_expert(expert_id):
    enlistment_model = Enlistment()
    search_words = ""
    if request.args.get('search'):
        search_words = request.args.get('search')

    all_enlistments = enlistment_model.get_formatted_enlistments_by_expert(int(expert_id), search_words)
    return all_enlistments, 200
