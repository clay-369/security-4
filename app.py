from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('log-in.html')

@app.route('/api/onderzoeken', methods=['POST'])
def create_research():
    research_item = request.json
    return #created_research, 201

if __name__ == "__main__":
    app.run(debug=True)