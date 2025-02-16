from flask import Flask, render_template, request, jsonify
from lib.model.organisatie import Organisatie

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('log-in.html')


@app.route('/organisatie_registratie', methods=['GET', 'POST'])
def organisatie_registratie():
    if request.method == 'POST':
        naam = request.form['naam']
        organisatie_type = request.form['type']
        website = request.form['website']
        contactpersoon = request.form['contactpersoon']
        beschrijving = request.form['beschrijving']
        email = request.form['email']
        telefoonnummer = request.form['telefoonnummer']
        details = request.form['details']

        organisatie = Organisatie()
        organisatie.create_organisatie(naam, organisatie_type, website, beschrijving, contactpersoon, email,
                                       telefoonnummer, details)

        return jsonify({"message": "Organisatie succesvol geregistreerd!", "success": True})

    return render_template('organisatie_registratie.html')

if __name__ == "__main__":
    app.run(debug=True)