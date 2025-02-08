from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('log-in.html')

@app.route('dashboard_beheer')
def dashboard_beheer():
    return render_template('dashboard-beheer.html')

if __name__ == "__main__":
    app.run(debug=True)