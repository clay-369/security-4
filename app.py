from flask import Flask, render_template, request, jsonify

from lib.model.users import Users


app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def login():
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

    else:
        return render_template('log-in.html')

@app.route('/admin/beheer', methods=['GET','POST'])
def beheer():
    users_model = Users()

    if request.method == 'POST':
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        create_admin = users_model.admin_create(first_name, last_name, email, password)
        if create_admin:
            return jsonify({"success": True})

    elif request.method == 'GET' and request.args.get('fetch') == 'adminData':
        admin_data = users_model.get_admins()
        return jsonify(admin_data)

    else:
        return render_template('beheerder-beheer.html')

@app.route('/user')
def user():
    return render_template('experts-dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)