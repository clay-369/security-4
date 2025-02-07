import flask
from flask import Flask, render_template, request
# DB Models
from lib.model.research import Research

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

    new_research_item = dict(research_model.get_research_by_id(new_research_id))

    return new_research_item, 201

@app.route('/api/onderzoeken', methods=['GET'])
def get_research_items():
    research_model = Research()
    all_research_items = research_model.get_all_research_items()

    all_formatted_research_items = []
    for research_item in all_research_items:
        formatted_research_item = research_model.format_research_item(research_item)
        all_formatted_research_items.append(formatted_research_item)

    return all_formatted_research_items

@app.route('/deskundige')
def expert_dashboard():
    return render_template('experts-dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)