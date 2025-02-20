from flask import Blueprint, render_template, request

from lib.model.research import Research
from lib.model.enlistments import Enlistment

research_bp = Blueprint('research', __name__)

# API's
## Research Items
@research_bp.route('/api/onderzoeken', methods=['GET'])
def get_research_items():
    research_model = Research()

    # Single research item
    if request.args.get('research_id'):
        research_id = request.args.get('research_id')
        research_item = research_model.get_research_by_id(int(research_id))
        formatted_research_item = research_model.format_research_item(research_item)
        return formatted_research_item

    # All research items
    all_research_items = research_model.get_all_research_items()

    formatted_research_items = []
    for research_item in all_research_items:
        formatted_research_item = research_model.format_research_item(research_item)
        formatted_research_items.append(formatted_research_item)

    # Filter for available research items
    if request.args.get('available') == 'true':
        formatted_research_items = list(filter(lambda item: item['beschikbaar'], formatted_research_items))

    # Filter for status: NIEUW, GOEDGEKEURD, AFGEKEURD, GESLOTEN
    if request.args.get('status'):
        status = request.args.get('status').upper()
        formatted_research_items = list(filter(lambda item: item['status'] == status, formatted_research_items))

    return formatted_research_items, 200


@research_bp.route('/api/onderzoeken', methods=['POST'])
def create_research_item():
    research_model = Research()

    auth_token = request.headers.get('Authorization')
    print(auth_token)
    # TODO: Authorization

    research_item = request.json

    new_research_id = research_model.create_research(research_item)
    if not new_research_id:
        return 500

    new_research_item = research_model.get_research_by_id(new_research_id)

    return dict(new_research_item), 201


## Enlistments
@research_bp.route('/api/onderzoeken/inschrijvingen', methods=['GET'])
def get_all_enlistments():
    enlistment_model = Enlistment()

    # Return all enlistments by one expert
    if request.args.get('expert_id'):
        expert_id = int(request.args.get('expert_id'))
        all_enlistments = enlistment_model.get_formatted_enlistments_by_expert(expert_id)
        return all_enlistments, 200


@research_bp.route('/api/onderzoeken/inschrijvingen', methods=['POST'])
def create_enlistment():
    enlistment_model = Enlistment()

    research_id = request.json['research_id']
    expert_id = request.json['expert_id']

    new_enlistment_id = enlistment_model.create_enlistment(research_id=research_id, expert_id=expert_id)
    new_enlistment = enlistment_model.get_enlistment_by_id(new_enlistment_id)

    return dict(new_enlistment), 201


@research_bp.route('/api/onderzoeken/inschrijvingen', methods=['DELETE'])
def delete_enlistment():
    expert_id = request.json['expert_id']
    research_id = request.json['research_id']
    enlistment_model = Enlistment()
    deleted_item = enlistment_model.delete_enlistment(expert_id, research_id)

    return dict(deleted_item), 200
