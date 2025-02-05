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

    research_item = request.json

    new_research_id = research_model.create_research(research_item)
    if not new_research_id:
        return # Error code

    new_research_item = dict(research_model.get_research_by_id(new_research_id))

    return new_research_item, 201

if __name__ == "__main__":
    app.run(debug=True)