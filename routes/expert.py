from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required

from lib.model.experts import Experts
from lib.model.disabilities import Disabilities
expert_bp = Blueprint('expert', __name__)

@expert_bp.route('/deskundige')
def dashboard():
    return render_template('experts-dashboard.html')


@expert_bp.route('/deskundige/registreer')
def register():
    return render_template('registreer_deskundige.html')


@expert_bp.route('/deskundige/profiel')
def edit():
    return render_template('account_beheer.html')


# API
@expert_bp.route("/api/deskundige", methods=["POST"])
def create_expert():
    expert_model = Experts()
    data = request.get_json()
    success, message = expert_model.create_deskundige(data)

    if success:
        return {"success": True, "message": message}
    else:
        return {"success": False, "message": message}


@expert_bp.route("/api/deskundige", methods=["GET"])
def get_expert():
    expert_model = Experts()
    if request.args.get('id'):
        deskundige_id = request.args.get('id')
        deskundige_info = expert_model.get_single_deskundige(deskundige_id)
        single_deskundige_dict = dict(deskundige_info)

        if deskundige_info:
            return {"success": True, "deskundige": single_deskundige_dict}
        else:
            return {"success": False}

    else:
        deskundige_id = session.get('user_id')
        deskundige_info = expert_model.get_single_deskundige(deskundige_id)
        single_deskundige_dict = dict(deskundige_info)

        if deskundige_info:
            return {"success": True, "deskundige": single_deskundige_dict}
        else:
            return {"success": False}


@expert_bp.route("/api/deskundige", methods=["PUT"])
def update_expert():
    expert_model = Experts()
    if request.args.get('id'):
        expert_id = request.args.get('id')
        data = request.get_json()
        update_deskundige, message = expert_model.update_deskundige(data)

        if update_deskundige:
            return {"success": True, "message": message}
        else:
            return {"success": False, "message": message}
        
@expert_bp.route("/api/disabilities", methods=["GET"])
def disabilities():
    disabilities_model = Disabilities()
    all_disabilities = disabilities_model.get_all_disabilities()
    if all_disabilities:
        return {"success": True, "disabilities": all_disabilities, "message": "Beperkingen gevonden"}
    else:
        return {"success": False, "message": "Geen beperkingen gevonden"}
        
# @expert_bp.route("/api/research", methods=["GET"])
# def research():
#     research_model = Research()
#     all_research = research_model.get_all_research_items()
#     return {"success": True, "research": all_research, "message": "Onderzoeken gevonden"}


