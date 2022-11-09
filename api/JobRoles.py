from flask import jsonify, request

from app import app, db
from models import JobRole, Skill, LearningJourney, Jobrole_skill


@app.route("/jobrole")
def view_jobrole():
    jobrolelist = JobRole.query.all()

    return jsonify(
        {
            "code": 200,
            "data": [role.json() for role in jobrolelist]
        }
    )


@app.route("/<string:staffId>/jobrole")
def view_relevant_jobrole(staffId):
    jobrolelist = JobRole.query.all()
    learningjourneylist = LearningJourney.query.filter_by(Staff_ID=staffId)

    currentljrole = []
    relevantrolelist = []

    for learningjourney in learningjourneylist:
        currentljrole.append(learningjourney.JobRole_ID)

    for role in jobrolelist:
        if role.JobRole_ID not in currentljrole and role.JobRole_Status != "Retired":
            relevantrolelist.append(role)

    return jsonify(
        {
            "code": 200,
            "data": [relevantrole.json() for relevantrole in relevantrolelist]
        }
    )


# retrieve a jobrole
@app.route("/jobrole/<string:jobroleId>")
def view_single_jobrole(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()

    return jsonify(
        {
            "code": 200,
            "data": jobrole.json()
        }
    )


# create a jobrole
@app.route("/jobrole/create", methods=['POST'])
def create_a_jobrole():
    data = request.get_json()
    jobrole = JobRole(
        JobRole_ID=data["JobRole_ID"],
        JobRole_Name=data["JobRole_Name"],
        JobRole_Desc=data["JobRole_Desc"]
        )
    jobroleId = jobrole.JobRole_ID
    jobrolename = jobrole.JobRole_Name

    if (JobRole.query.filter_by(JobRole_ID=jobroleId).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "jobroleId": jobroleId
                },
                "message": "Role ID already exists."
            }
        ), 400

    if (JobRole.query.filter_by(JobRole_Name=jobrolename).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "jobrolename": jobrolename
                },
                "message": "Role Name already exists."
            }
        ), 400

    try:
        db.session.add(jobrole)
        db.session.commit()
    except Exception:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "jobroleId": jobroleId
                },
                "message": "An error occurred creating the role."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": jobrole.json()
        }
    ), 200


# update a jobrole
@app.route("/jobrole/<string:jobroleId>", methods=['PUT'])
def update_a_jobrole(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    if jobrole:
        data = request.get_json()
        if data['JobRole_Name']:
            jobrole_check = JobRole.query.filter_by(JobRole_Name=data['JobRole_Name']).first()
            if jobrole_check and jobrole.JobRole_Name != data["JobRole_Name"]:
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "jobroleId": jobroleId
                        },
                        "message": "Role name is repeated."
                    }
                ), 404
            else:
                jobrole.JobRole_Name = data['JobRole_Name']

        if data['JobRole_Desc']:
            jobrole.JobRole_Desc = data['JobRole_Desc']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": jobrole.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "jobroleId": jobroleId
            },
            "message": "Role not found."
        }
    ), 404


# delete a jobrole
@app.route("/jobrole/<string:jobroleId>", methods=['DELETE'])
def delete_a_jobrole(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    if jobrole:
        # db.session.delete(jobrole)
        # db.session.commit()
        jobrole.JobRole_Status = "Retired"
        db.session.commit()


# restore a deleted jobrole
@app.route("/jobrole/restore/<string:jobroleId>")
def restore_jobrole(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    if jobrole:
        jobrole.JobRole_Status = None
        db.session.commit()
        return jsonify(
            {
                "code": 200,
            }
        )


# return the skills assigned to the specific job role
@app.route("/jobrole/assignedskills/<string:jobroleId>")
def get_assigned_skills_to_role(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    skillList = Skill.query.all()
    selected_skills = []

    if jobrole:
        for skill in skillList:
            assigned_skills_list = jobrole.skills
            if skill in assigned_skills_list:
                selected_skills.append(skill.Skill_ID)

        return jsonify(
            {
                "code": 200,
                "data": selected_skills,
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Jobrole not found",
        }
    ), 404


# Add skills to existing job role
@app.route("/hr/jobrole/edit/<string:jobroleId>", methods=["POST"])
def update_skills_to_role(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    if jobrole:
        jobroleId = jobrole.JobRole_ID
        skills_list = request.get_json()
        deleted_list = []
        added_list = []

        # check if there is at least one skill selected
        if (skills_list == []):
            return jsonify(
                {
                    "code": 400,
                    "message": "There must at least be one skill selected"
                }
            ), 400

        # delete all unassignment of skills to the role
        all_skills_role = db.session.query(Jobrole_skill).filter_by(JobRole_ID=jobroleId).all()
        for skill in all_skills_role:
            if skill.Skill_ID not in skills_list:
                try:
                    db.session.query(Jobrole_skill).filter_by(JobRole_ID=jobroleId, Skill_ID=skill.Skill_ID).delete()
                    db.session.commit()
                    deleted_list.append(skill.Skill_ID)
                except Exception:
                    return {
                        "message": "Unable to commit to database."
                    }, 404

        # add the new assigned skills to role
        for skillId in skills_list:
            check = db.session.query(Jobrole_skill).filter_by(JobRole_ID=jobroleId, Skill_ID=skillId).first()
            if check is None:
                try:
                    role_skill = Jobrole_skill.insert().values(JobRole_ID=jobroleId, Skill_ID=skillId)
                    db.engine.execute(role_skill)
                    added_list.append(skillId)
                except Exception:
                    return {
                        "message": "Unable to commit to database."
                    }, 404

        return jsonify(
            {
                "code": 200,
                "data": {
                    "Jobrole": jobroleId,
                    "added list": added_list,
                    "deleted list": deleted_list
                },
                "message": "Jobrole skills updated successfully."
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Jobrole not found",
        }
    ), 404
