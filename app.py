from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session

from lib.model.users import Users


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

if __name__ == "__main__":
    app.run(debug=True)