from flask import jsonify, request

from app import app, db
from models import Registration, JobRole, Skill


# retrieve all skills
@app.route("/skill")
def view_skills():
    skills = Skill.query.all()

    return jsonify(
        {
            "code": 200,
            "data": [skill.json() for skill in skills]
        }
    )


# retrieve all active skills
@app.route("/activeskill")
def view_active_skills():
    skills = Skill.query.filter_by(Skill_Status=None)

    return jsonify(
        {
            "code": 200,
            "data": [skill.json() for skill in skills]
        }
    )


# retrieve all skills related to a course
@app.route("/<string:jobroleId>/skills")
def view_skills_for_a_role(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    skill_list = []
    for skill in jobrole.skills:
        if skill.Skill_Status != "Retired":
            skill_list.append(skill)
    if skill_list:
        return (
            {
                "code": 200,
                "data": [skill.json() for skill in skill_list],
                "role": jobrole.JobRole_Name
            }
        )
    return (
            {
                "code": 400,
                "message": "No skills found"
            }
        )


# check if the user completed the skill
@app.route("/skills/complete/<string:jobroleId>", methods=["POST"])
def check_skills_completed(jobroleId):
    userId = request.get_json()["userId"]
    skills_of_role = []
    check_skill = view_skills_for_a_role(jobroleId)
    if check_skill["code"] == 200:
        skills_of_role = check_skill["data"]

    for i in range(len(skills_of_role)):
        course_found = False
        skill_id = skills_of_role[i]['Skill_ID']
        skill = Skill.query.filter_by(Skill_ID=skill_id).first()
        for course in skill.courses:
            registration = Registration.query.filter_by(Staff_ID=userId, Course_ID=course.Course_ID).first()
            if registration is not None:
                status = registration.Completion_Status
                if status == "Completed":
                    course_found = True
        skills_of_role[i]['Completion_Status'] = course_found

    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()

    return jsonify(
        {
            "code": 200,
            "data": skills_of_role,
            "role": jobrole.JobRole_Name
        }
    )


# find by skill
@app.route("/skill/<string:skillId>")
def find_by_skillId(skillId):
    skill = Skill.query.filter_by(Skill_ID=skillId).first()
    if skill:
        return jsonify(
            {
                "code": 200,
                "data": skill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404


# create a skill
@app.route("/skill/create", methods=['POST'])
def create_a_skill():
    data = request.get_json()
    skill = Skill(**data)
    skillId = skill.Skill_ID
    skillname = skill.Skill_Name

    if (Skill.query.filter_by(Skill_ID=skillId).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "skillId": skillId
                },
                "message": "Skill ID already exists."
            }
        ), 400

    if (Skill.query.filter_by(Skill_Name=skillname).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "skillname": skillname
                },
                "message": "Skill Name already exists."
            }
        ), 400

    try:
        db.session.add(skill)
        db.session.commit()
    except Exception:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "skillId": skillId
                },
                "message": "An error occurred creating the skill."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": skill.json()
        }
    ), 200


# update a skill
@app.route("/skill/<string:skillId>", methods=['PUT'])
def update_a_skill(skillId):
    skill = Skill.query.filter_by(Skill_ID=skillId).first()
    if skill:
        data = request.get_json()
        if data['Skill_Name']:
            skill_check = Skill.query.filter_by(Skill_Name=data['Skill_Name']).first()
            if skill_check and skill_check.Skill_ID != data["Skill_ID"]:
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "skillId": skillId
                        },
                        "message": "Skill name is repeated."
                    }
                ), 404
            else:
                skill.Skill_Name = data['Skill_Name']

        if data['Skill_Desc']:
            skill.Skill_Desc = data['Skill_Desc']

        try:
            db.session.commit()
        except Exception:
            return {
                "message": "Unable to commit to database."
            }, 404

        return jsonify(
            {
                "code": 200,
                "data": skill.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "data": {
                "skillId": skillId
            },
            "message": "Skill not found."
        }
    ), 404


# delete a skill
@app.route("/skill/<string:skillId>", methods=['DELETE'])
def delete_a_skill(skillId):
    skill = Skill.query.filter_by(Skill_ID=skillId).first()
    if skill:
        # db.session.delete(skill)
        # db.session.commit()
        skill.Skill_Status = "Retired"
        try:
            db.session.commit()
        except Exception:
            return {
                "message": "Unable to commit to database."
            }, 404

        return jsonify(
            {
                "code": 200,
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "skillId": skillId
            },
            "message": "Skill not found."
        }
    ), 404


# restore a deleted skill
@app.route("/skill/restore/<string:skillId>")
def restore_skill(skillId):
    skill = Skill.query.filter_by(Skill_ID=skillId).first()
    if skill:
        skill.Skill_Status = None
        try:
            db.session.commit()
        except Exception:
            return {
                "message": "Unable to commit to database."
            }, 404

        return jsonify(
            {
                "code": 200,
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "skillId": skillId
            },
            "message": "Skill not found."
        }
    ), 404
