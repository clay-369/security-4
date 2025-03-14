from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_jwt_extended import JWTManager

from lib.model.organisation import Organisation
from lib.model.token_blocklist import TokenBlocklist
# Routes
from routes import admin, expert, research, auth, organisation

from lib.model.users import Users
from lib.model.experts import Experts

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

Session(app)

app.config['SECRET_KEY'] = ';)' # For JWT


jwt = JWTManager()
jwt.init_app(app)

# Register blueprints
app.register_blueprint(admin.admin_bp)
app.register_blueprint(expert.expert_bp)
app.register_blueprint(research.research_bp)
app.register_blueprint(organisation.organisation_bp)
app.register_blueprint(auth.auth_bp, url_prefix='/auth')


OPEN_ROUTES = [
    'login_page', 'logout', '/', 'static', 'api_login', 'api_admin_beheer', 'test2', 'auth.login_jwt',
    'expert.register', 'expert.deskundige_api', 'expert.disabilities', 'expert.research', "expert.create_expert"
]
PUBLIC_API_ROUTES = [
    'organisation.edit_research', 'organisation.get_research', 'auth.whoami', 'auth.login_jwt', 'auth.refresh_access_token',
    'auth.logout_jwt', 'organisation.create_research_item', 'organisation.get_research_by_id'
]
ADMIN_ROUTES = ['admin.manage', 'admin.dashboard_beheer', 'admin.organisatie_registratie']
EXPERT_ROUTES = ['expert.dashboard', 'expert.register', 'expert.edit', 'expert.details']

temp_routes = ['expert.edit', 'expert.deskundige_api']

@app.before_request
def before_request():
    if request.endpoint in OPEN_ROUTES:
        return # Let user access route

    if request.endpoint in PUBLIC_API_ROUTES:
        return # Let jwt function handle protection

    # TEMP
    if request.endpoint in temp_routes:
        return

    logged_in = session.get('user_id')

    if logged_in is None:
        return redirect(url_for('login_page'))

    if logged_in:
        if request.endpoint in ADMIN_ROUTES and session.get('admin') == False:
            return redirect(url_for('index'))
        elif request.endpoint in EXPERT_ROUTES and session.get('admin') == True:
            return redirect(url_for('admin.dashboard_beheer'))


@app.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    # Logged in:
    elif session.get('admin'):
        return redirect(url_for('admin.dashboard_beheer'))
    elif not session.get('admin'):
        return redirect(url_for('expert.dashboard'))


@app.route('/login')
def login_page():
    return render_template('log-in.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    users_model = Users()
    login = users_model.login(email, password)
    if not login:
        return {"message": "Incorrect wachtwoord of email.", "success": False}

    if type(login) == str:
        # Error message
        return {"message": login}, 400

    if login['account_type'] == 'expert':
        expert_account = login['user']
        session['user_id'] = expert_account['deskundige_id']
        session['name'] = expert_account['voornaam']
        session['admin'] = False
        return {"success": True, "account_type": "expert"}

    elif login['account_type'] == 'admin':
        admin_account = login['user']
        session['user_id'] = admin_account['beheerder_id']
        session['name'] = admin_account['voornaam']
        session['admin'] = True
        return {"success": True, "account_type": "admin"}



@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


# API tests
## Create Research
@app.route('/test/maak-onderzoek')
def test():
    return render_template('api-test.html')

@app.route('/test/organisatie/login')
def test2():
    return render_template('public-api-test.html')


# JWT

## Load current user
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_headers, jwt_data):
    identity_email = jwt_data['sub']
    account_type = jwt_data['account_type']

    if account_type == 'expert':
        expert_model = Experts()
        expert_account = expert_model.get_expert_by_email(identity_email)
        return expert_account

    elif account_type == 'organisation':
        organisation_model = Organisation()
        organisation_account = organisation_model.get_organisation_by_email(identity_email)
        return organisation_account

    elif account_type == 'admin':
        admin_model = Users()
        admin_account = admin_model.get_admin_by_email(identity_email)
        return admin_account


## Additional claims
@jwt.additional_claims_loader
def make_additional_claims(identity_email):
    # Can be used to block organisations from visiting expert routes and the other way around
    # Check if expert
    expert_model = Experts()
    expert_account = expert_model.get_expert_by_email(identity_email)
    if expert_account:
        return {"account_type": "expert", "expert_id": expert_account['deskundige_id']}

    # Check if admin
    admin_model = Users()
    admin_account = admin_model.get_admin_by_email(identity_email)
    if admin_account:
        return {"account_type": "admin", "admin_id": admin_account['beheerder_id']}

    # Check if organisation
    organisation_model = Organisation()
    organisation_account = organisation_model.get_organisation_by_email(identity_email)
    if organisation_account:
        return {"account_type": "organisation", "organisation_id": organisation_account['organisatie_id']}



## JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(_jwt_header, _jwt_data):
    return {"message": "Token has expired", "error": "token_expired"}, 401


@jwt.invalid_token_loader
def invalid_token_callback(_error):
    return {"message": "Token is invalid", "error": "invalid_token"}, 401


@jwt.unauthorized_loader
def missing_token_callback(_error):
    return {"message": "Request doesn't contain a valid token", "error": "authorization_header"}, 401


@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(_jwt_header, jwt_data):
    jti = jwt_data['jti']
    token_blocklist_model = TokenBlocklist()
    is_blocked = token_blocklist_model.check_jti_in_blocklist(jti)

    return is_blocked


@app.route('/edit/research')
def research_test():
    return render_template('edit_research_test.html')

if __name__ == "__main__":
    app.run(debug=True)