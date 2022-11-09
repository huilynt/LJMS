from flask import jsonify, request

from app import app, db
from models import Role, JobRole, Skill, LearningJourney, Jobrole_skill

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
    jobrole = JobRole.query.filter_by(JobRole_ID= jobroleId).first()

    return jsonify(
        {
            "code":200,
            "data": jobrole.json()
        }
    )

# create a jobrole 
@app.route("/jobrole/create", methods=['POST'])
def create_a_jobrole():
    data = request.get_json()
    jobrole = JobRole(
        JobRole_ID = data["JobRole_ID"], 
        JobRole_Name  = data["JobRole_Name"], 
        JobRole_Desc  = data["JobRole_Desc"]
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
    except:
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
    ), 201

#update a jobrole
@app.route("/jobrole/<string:jobroleId>", methods=['PUT'])
def update_a_jobrole(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID= jobroleId).first()
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

#return the skills assigned to the specific job role
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
                "data": selected_skills
            }
        ), 200

    return jsonify(
        { 
            "code": 404,
            "message": "JobRole not found",
        }
    ), 404

#Add skills to existing job role
@app.route("/hr/jobrole/edit/<string:jobroleId>", methods=["POST"]) 
def update_skills_to_role(jobroleId):
    jobroleid = JobRole.query.filter_by(JobRole_ID = jobroleId).first().JobRole_ID
    skillid_list = request.get_json() #get from the part when the specific skill is added
    deleted_list=[]

    if (db.session.query(Jobrole_skill).filter_by(JobRole_ID=jobroleid).all()): #find all skills of job role and delete
        existing_jobrole_skills_list = db.session.query(Jobrole_skill).filter_by(JobRole_ID=jobroleid).all()
        for existing_jobrole_skills in existing_jobrole_skills_list:
            deleted_list.append(existing_jobrole_skills.Skill_ID)              
            db.session.query(Jobrole_skill).filter_by(JobRole_ID=jobroleid, Skill_ID=existing_jobrole_skills.Skill_ID).delete()
            db.session.commit()

    if (skillid_list == []): #check if there is at least one skill selected
        return jsonify(
            {
                "code": 400,
                "message": "There must at least be one skill selected"
            }
        ), 400
        
    for skillid in skillid_list: #add skills to job role
        jobrole_skill = Jobrole_skill.insert().values(JobRole_ID=jobroleid, Skill_ID=skillid)
        db.engine.execute(jobrole_skill)

    return jsonify(
        {
            "code": 200,
            "data": {
                "job role": jobroleid,
                "added list": skillid_list,
                "deleted list": deleted_list
            },
            "message": "Jobrole skills updated successfully."
        }
    ), 200

