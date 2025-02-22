from flask import Blueprint, request, current_app, make_response

import jwt
import datetime
from functools import wraps

from lib.model.organisatie import Organisatie

public_bp = Blueprint('public', __name__)

# JWT API Authorization
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') # http://127.0.0.1:5000/route?token=dmaoioemf4wnfei

        if not token:
            return {'message': 'Token is missing.'}, 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return {'message': 'Token is invalid.'}, 401

        return f(*args, **kwargs)
    return decorated


# Log in to get JWT
@public_bp.route('/api/organisatie')
def organisation_login():
    organisation_model = Organisatie()

    auth = request.authorization

    if auth:
        is_validated = organisation_model.validate_credentials(auth.username, auth.password)
        if is_validated:
            token = jwt.encode(
                {'organisation': auth.username, 'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)},
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            return {'token': token}

    return make_response('Could not verify.', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})


@public_bp.route('/api/e')
@token_required
def a():
    return 'a'
