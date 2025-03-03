from flask import Blueprint, render_template, request

from lib.model.deskundige import Deskundige
from lib.model.disabilities import Disabilities

expert_bp = Blueprint('expert', __name__)

@expert_bp.route('/deskundige')
def dashboard():
    return render_template('experts-dashboard.html')


@expert_bp.route('/deskundige/registreer')
def register():
    return render_template('registreer_deskundige.html')


@expert_bp.route('/deskundige/profiel')
def details():
    return render_template('deskundige_details.html')


@expert_bp.route('/deskundige/profiel/bewerk')
def edit():
    return render_template('account_beheer.html')


# API
@expert_bp.route("/api/deskundige", methods=["GET", "POST", "PUT"])
def deskundige_api():
    deskundige = Deskundige()
    if request.method == 'POST':
        data = request.get_json()
        success, message = deskundige.create_deskundige(data)

        if success:
            return {"success": True, "message": message}
        else: 
            return {"success": False, "message": message}

    if request.method == 'GET' and request.args.get('id'):
        deskundige_id = request.args.get('id')
        deskundige_info = deskundige.get_single_deskundige(deskundige_id)
        single_deskundige_dict = dict(deskundige_info)

        if deskundige_info:
            return {"success": True, "deskundige": single_deskundige_dict}
        else:
            return {"success": False}

    if request.method == 'PUT' and request.args.get('id'):
        deskundige_id = request.args.get('id')
        data = request.get_json()
        update_deskundige = deskundige.update_deskundige(data)

        if update_deskundige:
            return {"success": True}
        else:
            return {"success": False}
        
@expert_bp.route("/api/disabilities", methods=["GET"])
def disabilities():
    disabilities = Disabilities()
    if request.method == 'GET':
        all_disabilities = disabilities.get_all_disabilities()
        if all_disabilities:
            return {"success": True, "disabilities": all_disabilities, "message": "Beperkingen gevonden"}
        else:
            return {"success": False, "message": "Geen beperkingen gevonden"}

