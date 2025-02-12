from flask import Flask, render_template, request, jsonify

from lib.model.users import Users


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        users_model = Users()
        login = users_model.login(email, password)
        if login == ('user', True):
            return jsonify({"success": True, "type": "user"})
        elif login == ('admin', True):
            return jsonify({"success": True, "type": "admin"})
        else:
            return jsonify({"success": False})
    else:
        return render_template('log-in.html')

@app.route('/user')
def user():
    return render_template('experts-dashboard.html')

@app.route('/admin')
def admin():
    return render_template('beheerder-beheer.html')

if __name__ == "__main__":
    app.run(debug=True)