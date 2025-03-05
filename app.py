from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from lib.model.users import hash_password

# Routes
from routes import admin, expert, research

from lib.model.users import Users

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Register routes
app.register_blueprint(admin.admin_bp)
app.register_blueprint(expert.expert_bp)
app.register_blueprint(research.research_bp)


@app.before_request
def before_request():
    open_routes = ['login', '/', 'static', 'api_login', 'api_admin_beheer', 'expert.register', 'expert.deskundige_api', 'expert.disabilities', 'expert.research']
    temp_routes = ['expert.edit', 'expert.deskundige_api']
    admin_routes = ['admin.manage']
    expert_routes = ['expert.dashboard', 'expert.register', 'expert.edit', 'expert.details']
    logged_in = session.get('user_id')

    if logged_in is None and request.endpoint not in open_routes and request.endpoint not in temp_routes:
        return redirect(url_for('login'))

    if logged_in is not None:
        if request.endpoint in admin_routes and session.get('admin') == False:
            return redirect(url_for('index'))
        elif request.endpoint in expert_routes and session.get('admin') == True:
            return redirect(url_for('admin.manage'))   # Needs to redirect to admin dashboard when it's ready


@app.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    # Logged in:
    elif not session.get('admin'):
        return redirect(url_for('admin.manage'))
    elif session.get('admin'):
        return redirect(url_for('expert.dashboard'))


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

        password = hash_password(password)
        login = users_model.login(email)
        if 'user' in login:
            user = login[0]
            if password == user[2]:
                session['user_id'] = user['deskundige_id']
                session['name'] = user['voornaam']
                session['admin'] = False
                return {"success": True, "type": "user"}

        elif 'admin' in login:
            print('Admin found')
            admin = login[0]
            if password == admin[4]:
                print('Password correct')
                session['user_id'] = admin[0]
                session['name'] = admin[1]
                session['admin'] = True
                return {"success": True, "type": "admin"}
        else:
            return {"success": False}


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# API tests
## Create Research
@app.route('/test/maak-onderzoek')
def test():
    return render_template('api-test.html')



@app.route('/beheerder_beheer')
def beheerder():
    return render_template('beheerder-beheer.html')

@app.route('/dashboard_beheer')
def dashboard_beheer():
    return render_template('dashboard-beheer.html')

if __name__ == "__main__":
    app.run(debug=True)