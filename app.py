from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('log-in.html')

@app.route('/organisatie_registratie')
def organisatie_registratie():
    return render_template('organisatie_registratie.html')

if __name__ == "__main__":
    app.run(debug=True)