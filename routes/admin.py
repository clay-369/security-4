import sqlite3

from flask import Blueprint, render_template, request, session

from lib.model.research import Research
from lib.model.users import Users
from lib.model.organisation import Organisation
from lib.model.experts import Experts
from lib.model.enlistments import Enlistment


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def dashboard_beheer():
    return render_template('dashboard-beheer.html')

@admin_bp.route('/admin/beheer')
def manage():
    return render_template('beheerder-beheer.html')


@admin_bp.route('/admin/e', methods=['GET'])
def organisatie_registratie():
    return render_template('organisatie_registratie.html')

# API's
## Create admin account
@admin_bp.route('/api/admin/beheer', methods=['POST'])
def api_create_admin():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    users_model = Users()
    create_admin = users_model.admin_create(first_name, last_name, email, password)
    if create_admin:
        return {"success": True}
    else:
        return {"success": False}


@admin_bp.route('/api/admin/beheer', methods=['GET'])
def api_get_admin():
    users_model = Users()
    # Get all admins
    if request.args.get('fetch') == 'adminData':
        admin_data = users_model.get_admins()
        admin_dict = [dict(row) for row in admin_data]

        return admin_dict
    # Get one admin
    elif request.args.get('id') is not None:
        admin_id = request.args.get('id')
        admin_info = users_model.get_single_admin(admin_id)
        single_admin_dict = dict(admin_info)

        return single_admin_dict

# Edit admin
@admin_bp.route('/api/admin/beheer', methods=['PATCH'])
def api_edit_admin():
    data = request.get_json()
    admin_id = data.get('admin_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    users_model = Users()
    edit_admin = users_model.admin_edit(admin_id, first_name, last_name, email, password)
    if edit_admin:
        return {"success": True}
    else:
        return {"success": False}

# Delete admin account
@admin_bp.route('/api/admin/beheer', methods=['DELETE'])
def api_delete_admin():
    data = request.get_json()
    admin_id = data.get('admin_id')

    users_model = Users()
    delete_admin = users_model.admin_delete(admin_id)
    if delete_admin:
        return {"success": True}
    else:
        return {"success": False}

@admin_bp.route('/api/organisatie', methods=['POST'])
def create_organisation():
    data = request.get_json()

    organisation_model = Organisation()
    new_organisation_id = organisation_model.create_organisation(data)
    if new_organisation_id:
        return {"message": "Organisatie succesvol geregistreerd!", "success": True, "id": new_organisation_id}, 201

    return {"message": "Dit e-mailadres bestaat al.", "success": False}, 400

@admin_bp.route('/api/admin', methods=['GET'])
def api_get_data():
    experts_model = Experts()
    enlistment_model = Enlistment()
    research_model = Research()

    expert_data = experts_model.get_deskundigen()
    expert_dict = [dict(row) for row in expert_data]

    research_data = research_model.get_all_research_items_for_admins()

    # Inschrijving details
    enlistment_data = enlistment_model.get_enlistments_details()
    enlistment_dict = [dict(row) for row in enlistment_data]
    print(enlistment_dict)


    return {
        "experts": expert_dict,
        "enlistments": enlistment_dict,
        "researches": research_data,
        "admin_id": session.get('user_id')
    }

@admin_bp.route('/api/admin', methods=['PATCH'])
def api_status_update():
    data = request.get_json()
    status = data.get('status')
    data_type = data.get('data_type')
    data_id = data.get('data_id')
    admin_id = data.get('admin_id')
    if data_type == 'expert':
        experts_model = Experts()
        experts_model.status_update(status, data_id, admin_id)
        return {"message" : "Registratie succesvol geaccepteerd!"}
    elif data_type == 'enlistment':
        enlistment_model = Enlistment()
        enlistment_model.status_update(status, data_id, admin_id)
        return {"message" : "Inschrijving succesvol geaccepteerd!"}
    elif data_type == 'research':
        research_model = Research()
        research_model.status_update(status, data_id, admin_id)
        return {"message" : "Onderzoek succesvol geaccepteerd!"}
    else:
        return {"message": "Er is iets fout gegaan tijdens het accepteren van het verzoek."}

