import sqlite3

from flask import Blueprint, render_template, request

from lib.model.users import Users
from lib.model.organisation import Organisation

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def dashboard_beheer():
    return render_template('dashboard-beheer.html')

@admin_bp.route('/admin/beheer')
def manage():
    return render_template('beheerder-beheer.html')


@admin_bp.route('/admin/organisatie', methods=['GET'])
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
    try:
        new_organisation_id = organisation_model.create_organisation(data)
        return {"message": "Organisatie succesvol geregistreerd!", "success": True, "id": new_organisation_id}, 201
    except sqlite3.IntegrityError:
        return {"message": "Dit e-mailadres bestaat al.", "success": False}, 400


