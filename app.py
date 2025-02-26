from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_jwt_extended import JWTManager

# Routes
from routes import admin, expert, research, auth, organisation

from lib.model.users import Users

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SECRET_KEY'] = ';)' # For JWT


jwt = JWTManager()
jwt.init_app(app)

# Register blueprints
app.register_blueprint(admin.admin_bp)
app.register_blueprint(expert.expert_bp)
app.register_blueprint(research.research_bp)
app.register_blueprint(auth.auth_bp)
app.register_blueprint(organisation.organisation_bp)


OPEN_ROUTES = ['login', '/', 'static', 'api_login', 'api_admin_beheer', 'test2', 'auth.login_organisation']
PROTECTED_ROUTES = ['organisation.get_research', 'auth.whoami']
ADMIN_ROUTES = ['admin.manage']
EXPERT_ROUTES = ['expert.dashboard', 'expert.register', 'expert.edit', 'expert.details']


@app.before_request
def before_request():
    logged_in = session.get('user_id')

    if request.endpoint in OPEN_ROUTES:
        return # Let user access route

    if request.endpoint in PROTECTED_ROUTES:
        return # Let jwt function handle protection

    if logged_in is None:
        return redirect(url_for('login')), 401

    if logged_in is not None:
        if request.endpoint in ADMIN_ROUTES and session.get('admin') == False:
            return redirect(url_for('index')), 403
        elif request.endpoint in EXPERT_ROUTES and session.get('admin') == True:
            return redirect(url_for('admin.manage')), 403   # Needs to redirect to admin dashboard when it's ready


@app.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    # Logged in:
    elif session.get('admin'):
        return redirect(url_for('admin.manage'))
    elif not session.get('admin'):
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

        login = users_model.login(email)
        if 'user' in login:
            user = login[0]
            if password == user[2]:
                session['user_id'] = user['deskundige_id']
                session['name'] = user['voornaam']
                session['admin'] = False
                return {"success": True, "type": "user"}

        elif 'admin' in login:
            admin = login[0]
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

@app.route('/test/organisatie/login')
def test2():
    return render_template('public-api-test.html')


@app.route('/beheerder_beheer')
def beheerder():
    return render_template('beheerder-beheer.html')

@app.route('/dashboard_beheer')
def dashboard_beheer():
    return render_template('dashboard-beheer.html')

# JWT
## Additional claims
@jwt.additional_claims_loader
def make_additional_claims(identity):
    # Can be used to block organisations from visiting expert routes and the other way around
    if identity == 'Stichting accessibility':
        return {"account_type": "organisation"}
    else:
        return {"account_type": "expert"}

## JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return {"message": "Token has expired", "error": "token_expired"}, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"message": "Token is invalid", "error": "invalid_token"}, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"message": "Request doesn't contain a valid token", "error": "authorization_header"}, 401


if __name__ == "__main__":
    app.run(debug=True)