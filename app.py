from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_session import Session

from lib.model.users import Users


app = Flask(__name__)

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

        login = users_model.login(email, password)
        if login == ('user', True):
            return jsonify({"success": True, "type": "user"})

        elif login == ('admin', True):
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

if __name__ == "__main__":
    app.run(debug=True)