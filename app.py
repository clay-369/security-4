import flask
from flask import Flask, render_template, request
# DB Models
from lib.model.research import Research
from lib.model.enlistments import Enlistment

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('log-in.html')

@app.route('/test')
def test():
    return render_template('api-test.html')

@app.route('/api/onderzoeken', methods=['POST'])
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

@app.route('/api/onderzoeken', methods=['GET'])
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

    all_formatted_research_items = []
    for research_item in all_research_items:
        formatted_research_item = research_model.format_research_item(research_item)
        all_formatted_research_items.append(formatted_research_item)

    return all_formatted_research_items, 200

@app.route('/api/onderzoeken/inschrijvingen', methods=['POST'])
def create_enlistment():
    enlistment_model = Enlistment()

    research_id = request.json['research_id']
    expert_id = request.json['expert_id']

    new_enlistment_id = enlistment_model.create_enlistment(research_id=research_id, expert_id=expert_id)
    new_enlistment = enlistment_model.get_enlistment_by_id(new_enlistment_id)

    return dict(new_enlistment), 201

@app.route('/api/onderzoeken/inschrijvingen', methods=['GET'])
def get_all_enlistments():
    enlistment_model = Enlistment()

    all_enlistments = enlistment_model.get_all_formatted_enlistments()

    return all_enlistments, 200

@app.route('/api/onderzoeken/inschrijvingen', methods=['DELETE'])
def delist():
    expert_id = request.json['expert_id']
    research_id = request.json['research_id']
    enlistment_model = Enlistment()
    deleted_item = enlistment_model.delete_enlistment(expert_id, research_id)

    return dict(deleted_item), 200


@app.route('/deskundige')
def expert_dashboard():
    return render_template('experts-dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)