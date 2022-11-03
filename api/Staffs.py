from flask import jsonify, request

from app import app, db
from models import Staff, Registration, Role

@app.route("/staff")
def view_staff():
    stafflist = Staff.query.all()
    
    return jsonify(
        {
            "code": 200, 
            "data": [staff.json() for staff in stafflist]
        }
    )

@app.route("/registration")
def view_registration():
    registrationlist = Registration.query.all()

    return jsonify(
        {
            "code": 200, 
            "data": [regi.json() for regi in registrationlist]
        }
    )

#create a role 
@app.route("/roles/create", methods=['POST'])
def create_a_role():
    data = request.get_json()
    role = Role(**data)
    roleId = role.Role_ID
    rolename = role.Role_Name
    
    if (Role.query.filter_by(Role_ID=roleId).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "roleId": roleId
                },
                "message": "Role ID already exists."
            }
        ), 400

    if (Role.query.filter_by(Role_Name=rolename).first()):
        return jsonify(
            {
                "code": 200,
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "roleId": roleId
            },
            "message": "Role not found."
        }
    ), 404
