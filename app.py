from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session

# DB Models
from lib.model.research import Research
from lib.model.enlistments import Enlistment
from lib.model.organisatie import Organisatie

from lib.model.users import Users
from lib.model.deskundige import Deskundige

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def before_request():
    open_routes = ['login', '/', 'static', 'api_login', 'api_admin_beheer']
    admin_routes = ['admin_beheer']
    user_routes = ['user']
    logged_in = session.get('user_id')

    if logged_in is None and request.endpoint not in open_routes:
        return redirect(url_for('login'))

    if logged_in is not None:
        if request.endpoint in admin_routes and session.get('admin') == False:
            return redirect(url_for('index'))
        elif request.endpoint in user_routes and session.get('admin') == True:
            return redirect(url_for('admin_beheer'))   # Needs to redirect to admin dashboard when it's ready

@app.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('user'))
@app.route('/login')
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

@app.route('/api/login', methods=['GET','POST'])
def api_login():
    users_model = Users()

    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        login = users_model.login(email)
        if 'user' in login:
            user = login[0]
            if password == user[2]:
                session['user_id'] = user['deskundige_id']
                session['name'] = user['voornaam']
                session['admin'] = False
                return jsonify({"success": True, "type": "user"})

        elif 'admin' in login:
            admin = login[0]
            session['user_id'] = admin[0]
            session['name'] = admin[1]
            session['admin'] = True
            return jsonify({"success": True, "type": "admin"})

        else:
            return jsonify({"success": False})

@app.route('/admin/beheer')
def admin_beheer():
    return render_template('beheerder-beheer.html')

@app.route('/account_beheer')
def account_beheer():
    return render_template('account_beheer.html')


@app.route('/api/admin/beheer', methods=['GET','POST'])
def api_admin_beheer():
    users_model = Users()

    if request.method == 'POST':
        data = request.get_json()
        request_type = data.get('request')

        if request_type == 'create':
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')

            create_admin = users_model.admin_create(first_name, last_name, email, password)
            if create_admin:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

        elif request_type == 'update':
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            admin_id = data.get('admin_id')

            edit_admin = users_model.admin_edit(admin_id, first_name, last_name, email, password)
            if edit_admin:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

        elif request_type == 'delete':
            admin_id = data.get('admin_id')

            delete_admin = users_model.admin_delete(admin_id)
            if delete_admin:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

    elif request.method == 'GET' and request.args.get('fetch') == 'adminData':
        admin_data = users_model.get_admins()
        admin_dict = [dict(row) for row in admin_data]
        return jsonify(admin_dict)

    elif request.method == 'GET' and request.args.get('id') is not None:
        admin_id = request.args.get('id')
        admin_info = users_model.get_single_admin(admin_id)
        single_admin_dict = dict(admin_info)

        return jsonify(single_admin_dict)

@app.route('/user')
def user():
    return render_template('experts-dashboard.html')

@app.route('/logout')
def logout():
    session['user_id'] = None
    session['name'] = None
    session['admin'] = None
    return redirect('/')

# Registreer deskundige
@app.route('/registreer_deskundige')
def registreer_deskundige():
    return render_template('registreer_deskundige.html')

@app.route('/deskundige_details')
def deskundige_details():
    return render_template('deskundige_details.html')

# Api voor registreer deskundige
@app.route("/api/deskundige", methods=["GET", "POST", "PUT"])
def deskundige_api():
    deskundige = Deskundige()
    if request.method == 'POST':
        data = request.get_json()
        create_admin = deskundige.create_deskundige(data)

        if create_admin:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})

    if request.method == 'GET' and request.args.get('id'):
        print("test")
        deskundige_id = request.args.get('id')
        deskundige_info = deskundige.get_single_deskundige(deskundige_id)
        single_deskundige_dict = dict(deskundige_info)

        if deskundige_info:
            return jsonify({"success": True, "deskundige": single_deskundige_dict})
        else:
            return jsonify({"success": False})

    if request.method == 'PUT' and request.args.get('id'):
        deskundige_id = request.args.get('id')
        data = request.get_json()
        update_deskundige = deskundige.update_deskundige(data)

        if update_deskundige:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})


@app.route('/test')
def test():
    return render_template('api-test.html')


@app.route('/deskundige')
def expert_dashboard():
    return render_template('experts-dashboard.html')


# API's
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

    # Return all enlistments by one expert
    if request.args.get('expert_id'):
        expert_id = int(request.args.get('expert_id'))
        all_enlistments = enlistment_model.get_formatted_enlistments_by_expert(expert_id)
        return all_enlistments, 200


@app.route('/api/onderzoeken/inschrijvingen', methods=['DELETE'])
def delist():
    expert_id = request.json['expert_id']
    research_id = request.json['research_id']
    enlistment_model = Enlistment()
    deleted_item = enlistment_model.delete_enlistment(expert_id, research_id)

    return dict(deleted_item), 200





if __name__ == "__main__":
    app.run(debug=True)