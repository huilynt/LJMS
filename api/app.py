from audioop import add
from re import L
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import delete
import requests
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/ljps"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


class Role(db.Model):
    __tablename__ = "role"
    Role_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(20), nullable=False)

    staff = db.relationship("Staff", backref="role", lazy=True)

    def __init__(self, Role_ID, Role_Name):
        self.Role_ID = Role_ID
        self.Role_Name = Role_Name

    def json(self):
        return {
            "Role_ID": self.Role_ID, 
            "Role_Name": self.Role_Name
        }


class Course(db.Model):
    __tablename__ = "course"

    Course_ID = db.Column(db.String(20), primary_key=True)
    Course_Name = db.Column(db.String(50), nullable=False)
    Course_Desc = db.Column(db.String(255), nullable=True)
    Course_Status = db.Column(db.String(15), nullable=True)
    Course_Type = db.Column(db.String(10), nullable=True)
    Course_Category = db.Column(db.String(50), nullable=True)

    registrations = db.relationship("Registration", backref="course", lazy=True)

    def __init__(self, Course_ID, Course_Name, Course_Desc, Course_Status, Course_Type, Course_Category):
        self.Course_ID = Course_ID
        self.Course_Name = Course_Name
        self.Course_Desc = Course_Desc
        self.Course_Status = Course_Status
        self.Course_Type = Course_Type
        self.Course_Category = Course_Category

    def json(self):
        return {
            "Course_ID": self.Course_ID, 
            "Course_Name": self.Course_Name, 
            "Course_Desc": self.Course_Desc,
            "Course_Status": self.Course_Status,
            "Course_Type": self.Course_Type,
            "Course_Category": self.Course_Category,
        }


class Staff(db.Model):
    __tablename__ = "staff"

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Role = db.Column(db.Integer, db.ForeignKey(Role.Role_ID), nullable=False)

    registrations = db.relationship("Registration", backref="staff", lazy=True)

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Dept, Email, Role):
        self.Staff_ID = Staff_ID
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Dept = Dept
        self.Email = Email
        self.Role = Role

    def json(self):
        return {
            "Staff_ID": self.Staff_ID, 
            "Staff_FName": self.Staff_FName, 
            "Staff_LName": self.Staff_LName,
            "Dept": self.Dept,
            "Email": self.Email,
            "Role": self.Role,
        }


class Registration(db.Model):
    __tablename__ = "registration"

    Reg_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.String(20), db.ForeignKey(Course.Course_ID), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey(Staff.Staff_ID), nullable=False)
    Reg_Status = db.Column(db.String(20), nullable=False)
    Completion_Status = db.Column(db.String(20))

    def __init__(self, Reg_ID, Course_ID, Staff_ID, Reg_Status, Completion_Status, Role):
        self.Reg_ID = Reg_ID
        self.Course_ID = Course_ID
        self.Staff_ID = Staff_ID
        self.Reg_Status = Reg_Status
        self.Completion_Status = Completion_Status

    def json(self):
        return {
            "Reg_ID": self.Reg_ID, 
            "Course_ID": self.Course_ID, 
            "Staff_ID": self.Staff_ID,
            "Reg_Status": self.Reg_Status,
            "Completion_Status": self.Completion_Status
        }

Jobrole_skill = db.Table('jobrole_skill',
                        db.Column('JobRole_ID', db.String, db.ForeignKey('jobrole.JobRole_ID')),
                        db.Column('Skill_ID', db.String, db.ForeignKey('skill.Skill_ID'))
)

Skill_course = db.Table('skill_course',
                        db.Column('Skill_ID', db.String, db.ForeignKey('skill.Skill_ID')),
                        db.Column('Course_ID', db.String, db.ForeignKey('course.Course_ID'))
)

class Skill(db.Model):
    __tablename__ = "skill"

    Skill_ID = db.Column(db.String, primary_key=True)
    Skill_Name = db.Column(db.String, nullable=False)
    Skill_Desc = db.Column(db.String)
    Skill_Status = db.Column(db.String)

    courses = db.relationship(Course, secondary=Skill_course, backref="skill", lazy=True)

    def __init__(self, Skill_ID, Skill_Name, Skill_Desc="", Skill_Status=""):
        self.Skill_ID = Skill_ID
        self.Skill_Name = Skill_Name
        self.Skill_Desc = Skill_Desc
        self.Skill_Status = Skill_Status

    def json(self):
        return {
            "Skill_ID": self.Skill_ID,
            "Skill_Name": self.Skill_Name,
            "Skill_Desc": self.Skill_Desc,
            "Skill_Status": self.Skill_Status
        }


class JobRole(db.Model):
    __tablename__ = "jobrole"

    JobRole_ID = db.Column(db.String, primary_key=True)
    JobRole_Name = db.Column(db.String, nullable=False)
    JobRole_Desc = db.Column(db.String)
    JobRole_Status = db.Column(db.String)

    skills = db.relationship(Skill, secondary=Jobrole_skill, backref="jobroles", lazy=True)

    def __init__(self, JobRole_ID, JobRole_Name, JobRole_Desc="", JobRole_Status=""):
        self.JobRole_ID = JobRole_ID
        self.JobRole_Name = JobRole_Name
        self.JobRole_Desc = JobRole_Desc
        self.JobRole_Status = JobRole_Status

    def json(self):
        return {
            "JobRole_ID": self.JobRole_ID,
            "JobRole_Name": self.JobRole_Name,
            "JobRole_Desc": self.JobRole_Desc,
            "JobRole_Status": self.JobRole_Status
        }

# Learning Journey
LearningJourney_SelectedCourse = db.Table("learningjourney_selectedcourse",
                        db.Column('Journey_ID', db.String, db.ForeignKey("learningjourney.Journey_ID")),
                        db.Column('Course_ID', db.String, db.ForeignKey(Course.Course_ID)),
)

class LearningJourney(db.Model):
    __tablename__ = "learningjourney"

    Journey_ID = db.Column(db.String, primary_key=True)
    JobRole_ID = db.Column(db.String, db.ForeignKey(JobRole.JobRole_ID), nullable=False)
    Staff_ID = db.Column(db.String, db.ForeignKey(Staff.Staff_ID), nullable=False)
    LearningJourney_Status = db.Column(db.String)

    courses = db.relationship(Course, secondary=LearningJourney_SelectedCourse, backref="learningjourneys", lazy=True)

    def __init__(self, Journey_ID, JobRole_ID, Staff_ID, LearningJourney_Status="Progress"):
        self.Journey_ID = Journey_ID
        self.JobRole_ID = JobRole_ID
        self.Staff_ID = Staff_ID
        self.LearningJourney_Status = LearningJourney_Status

    def json(self):
        return {
            "Journey_ID": self.Journey_ID,
            "JobRole_ID": self.JobRole_ID,
            "Staff_ID": self.Staff_ID,
            "LearningJourney_Status": self.LearningJourney_Status
        }


@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/role")
def view_role():
    rolelist = Role.query.all()
    return "Testing! Role table row count: " + str(len(rolelist))

@app.route("/course")
def view_course():
    courselist = Course.query.all()
    return jsonify(
        {
            "code": 200, 
            "data": [course.json() for course in courselist]
        }
    )

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
        if role.JobRole_ID not in currentljrole:
            relevantrolelist.append(role)
    
    return jsonify(
        {
            "code": 200, 
            "data": [relevantrole.json() for relevantrole in relevantrolelist]
        }
    )

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
    skills = Skill.query.filter_by(Skill_Status = None)

    return jsonify(
        {
            "code": 200, 
            "data": [skill.json() for skill in skills]
        }
    )

# retrieve all skills related to a course
@app.route("/<string:jobroleId>/skills")
def view_skills_for_a_role(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID= jobroleId).first()
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
            registration = Registration.query.filter_by(Staff_ID = userId, Course_ID = course.Course_ID).first()
            if registration is not None:
                status = registration.Completion_Status
                if status == "Completed":
                    course_found = True
        skills_of_role[i]['Completion_Status'] = course_found

    jobrole = JobRole.query.filter_by(JobRole_ID= jobroleId).first()
        
    return jsonify(
        {
            "code": 200,
            "data": skills_of_role,
            "role": jobrole.JobRole_Name
        }
    )
    


# retrieve one course information
@app.route("/course/<string:CourseId>")
def view_course_information(CourseId):
    course_info = Course.query.filter_by(Course_ID = CourseId).first()
    return jsonify(
        {
            "code":200,
            "data": course_info.json()
        }
    )

# retrieve all courses related to a skill
@app.route("/<string:skillId>/courses")
def view_courses_for_a_skill(skillId):
    skill = Skill.query.filter_by(Skill_ID= skillId).first()

    course_list = []
    for course in skill.courses:
        if course.Course_Status == 'Active':
            course_list.append(course)

    return jsonify(
        {
            "code": 200,
            "data": {
                "courses": [course.json() for course in course_list],
                "skill": skill.json()
            }
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
    except:
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
    ), 201

#update a skill
@app.route("/skill/<string:skillId>", methods=['PUT'])
def update_a_skill(skillId):
    skill = Skill.query.filter_by(Skill_ID= skillId).first()
    if skill:
        data = request.get_json()
        if data['Skill_Name']:
            skill_check = Skill.query.filter_by(Skill_Name=data['Skill_Name']).first()
            if skill_check and skill.Skill_Name != data["Skill_Name"]:
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
        db.session.commit()
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
        db.session.commit()
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

# delete a jobrole
@app.route("/jobrole/<string:jobroleId>", methods=['DELETE'])
def delete_a_jobrole(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    if jobrole:
        # db.session.delete(jobrole)
        # db.session.commit()
        jobrole.JobRole_Status = "Retired"
        db.session.commit()

# restore a deleted skill
@app.route("/skill/restore/<string:skillId>")
def restore_skill(skillId):
    skill = Skill.query.filter_by(Skill_ID=skillId).first()
    if skill:
        skill.Skill_Status = None
        db.session.commit()
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

# get all courses a staff has added (registered/waitlist)
@app.route("/staff/courses/added", methods=['POST'])
def staff_courses_completed():
    userId = request.get_json()["userId"]
    roleId = request.get_json()["roleId"]
    journeyId = roleId + "-" + userId
    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    
    return jsonify(
        {
            "code": 200,
            "data": [course.Course_ID for course in journey.courses]
        }
    ), 200

# retrieve all user learning journey
@app.route("/learningjourney", methods=["POST"])
def view_leaningjourney():
    userId = request.get_json()["userId"]
    registration = Staff.query.filter_by(Staff_ID = userId).first()

    if registration:
        learningjourneylist = LearningJourney.query.filter_by(Staff_ID = userId).all()
        
        for journey in learningjourneylist:
            if journey.LearningJourney_Status == "Progress":
                url = "http://127.0.0.1:5000/journey/progress/" + journey.Journey_ID
                x = requests.post(url, json={"userId": userId})
                code = json.loads(x.text)["code"]
                if code == "200":
                    update_journey_completion(journey.Journey_ID, json.loads(x.text)["data"] )

        if learningjourneylist:
            return jsonify(
                    {
                        "code": 200, 
                        "data": [learningjourney.json() for learningjourney in learningjourneylist]
                    }
                )
                
    return jsonify(
        { 
            "code": 404,
            "message": "Staff has no existing learning journey."
        }
    ), 404

def update_journey_completion(journeyId, skill_list):    
    completed_cnt = 0
    for skill in skill_list:
        if skill['Completion_Status'] == True:
            completed_cnt += 1

    journey = LearningJourney.query.filter_by(Journey_ID = journeyId).first()
    role = JobRole.query.filter_by(JobRole_ID = journey.JobRole_ID).first()

    if len(role.skills) == completed_cnt:
        if journey:
            journey.LearningJourney_Status = 'Completed'
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": journey.json()
                }
            )

    return jsonify(
        { 
            "code": 404,
            "message": "Staff has no existing learning journey."
        }
    ), 404


@app.route("/journey/progress/<string:journeyId>", methods=["POST"])
def get_skills_progress(journeyId):
    userId = request.get_json()["userId"]
    journey = LearningJourney.query.filter_by(Journey_ID = journeyId).first()
    skill_list = []
    check_skill_list = view_skills_for_a_role(journey.JobRole_ID)
    if check_skill_list["code"] == 200:
        skill_list = check_skill_list["data"]
    courses_added = journey.courses
    if journey and skill_list:
        for i in range(len(skill_list)):
            course_found = False
            skill_id = skill_list[i]['Skill_ID']
            skill = Skill.query.filter_by(Skill_ID=skill_id).first()
            for course in courses_added:
                if course in skill.courses:
                    course_regi = Registration.query.filter_by(Staff_ID=userId, Course_ID=course.Course_ID).first()
                    if course_regi:
                        if course_regi.Completion_Status == "Completed":
                            course_found = True
            skill_list[i]['Completion_Status'] = course_found

        jobrole = JobRole.query.filter_by(JobRole_ID= journey.JobRole_ID).first()

        return jsonify(
            {
                "code": 200,
                "data": skill_list,
                "role": jobrole.JobRole_Name
            }
        ), 201

    return jsonify(
        { 
            "code": 404,
            "message": "Journey not found"
        }
    ), 404

@app.route("/journey/<string:journeyId>", methods=["POST"])
def get_courses_in_journey(journeyId):
    userId = request.get_json()["userId"]
    journey = LearningJourney.query.filter_by(Journey_ID = journeyId).first()
    course_list = [course.json() for course in journey.courses]
    skill_list = JobRole.query.filter_by(JobRole_ID= journey.JobRole_ID).first().skills

    for i in range(len(course_list)):
        course_found = False
        course = course_list[i]
        registration = Registration.query.filter_by(Staff_ID = userId, Course_ID = course['Course_ID']).first()
        if registration is not None:
            status = registration.Completion_Status
            if status == "Completed":
                course_found = True
        
        course_list[i]["Completion_Status"] = course_found

    for j in range(len(journey.courses)):
        course = journey.courses[j]
        for skill in skill_list:
            if course in skill.courses:
                if "skills" in course_list[j]:
                    course_list[j]['skills'].append(skill.json())
                else:
                    course_list[j]["skills"] = [skill.json()]

    return jsonify(
        {
            "code": 200,
            "data": course_list
        }
    ), 201


@app.route("/courses/<string:courseId>")
def get_assgined_courses(courseId):
    skillList = Skill.query.all()
    selected_skills = []

    for skill in skillList:
        courseList = skill.courses
        course = Course.query.filter_by(Course_ID=courseId).first()
        if course in courseList:
            selected_skills.append(skill.Skill_ID)

    if selected_skills:
        return jsonify(
            {
                "code": 200,
                "data": selected_skills,
                "name": course.Course_Name
            }
        ), 201

    return jsonify(
        { 
            "code": 404,
            "message": "skills not found",
            "name": course.Course_Name
        }
    ), 404

#Add skills to existing course
@app.route("/hr/courses/edit/<string:courseId>", methods=["POST"]) 
def update_skills_to_course(courseId):
    courseid = Course.query.filter_by(Course_ID = courseId).first().Course_ID
    skillid_list = request.get_json() #get from the part when the specific skill is added
    deleted_list=[]

    if (db.session.query(Skill_course).filter_by(Course_ID=courseId).all()): #find all skills of courses and delete
        existing_course_skills_list = db.session.query(Skill_course).filter_by(Course_ID=courseId).all()
        for existing_course_skills in existing_course_skills_list:
            deleted_list.append(existing_course_skills.Skill_ID)              
            db.session.query(Skill_course).filter_by(Course_ID=courseId, Skill_ID=existing_course_skills.Skill_ID).delete()
            db.session.commit()

    if (skillid_list == []): #check if there is at least one skill selected
        return jsonify(
            {
                "code": 400,
                "message": "There must at least be one skill selected"
            }
        ), 400
        
    for skillid in skillid_list: #add skills to courses
        course_skill = Skill_course.insert().values(Course_ID=courseId, Skill_ID=skillid)
        db.engine.execute(course_skill)

    return jsonify(
        {
            "code": 200,
            "data": {
                "Course": courseId,
                "added list": skillid_list,
                "deleted list": deleted_list
            },
            "message": "Course skills updated successfully."
        }
    ), 200

#return the skills assigned to the specific job role
@app.route("/jobrole/assignedskills/<string:jobroleId>")
def get_assigned_skills(jobroleId):
    jobrole = JobRole.query.filter_by(JobRole_ID=jobroleId).first()
    skillList = Skill.query.all()
    selected_skills = []
    
    for skill in skillList:
        assigned_skills_list = jobrole.skills
        if skill in assigned_skills_list:
            selected_skills.append(skill.Skill_ID)

    if selected_skills:
        return jsonify(
            {
                "code": 200,
                "data": selected_skills,
            }
        ), 200

    return jsonify(
        { 
            "code": 404,
            "message": "skills not found",
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

@app.route("/journey/<string:journeyId>/<string:courseId>", methods=['DELETE'])
def remove_existing_course_learning_journey(journeyId, courseId):   
    learningjourney = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    print(learningjourney)
    for course in learningjourney.courses:
        if(course.Course_ID==courseId):       
            try:
                db.session.query(LearningJourney_SelectedCourse).filter_by(Course_ID=courseId, Journey_ID=journeyId).delete()
                db.session.commit()
                return jsonify(
                            {
                                "code": 200,
                                "message": "Delete success"
                            }
                        ), 201
            except:
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "journeyId": journeyId,
                            "courseId": courseId
                        },
                        "message": "Course in selected Learning Journey not found"
                    }
                ), 404
    return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "journeyId": journeyId,
                            "courseId": courseId
                        },
                        "message": "Course in selected Learning Journey not found"
                    }
                ), 404
    
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

# save learning journey with added courses
@app.route("/journey/<string:staffId>/<string:jobRoleId>", methods=['POST'])
def save_learning_journey(staffId, jobRoleId):
    journeyId = jobRoleId + '-' + staffId
    print(journeyId)
    addedCourses = request.get_json()["addedCourses"]
    
    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    if journey == None:
        journey = LearningJourney(Journey_ID = journeyId, 
                                    Staff_ID = staffId, 
                                    JobRole_ID = jobRoleId, 
                                    LearningJourney_Status = 'Progress',
                                )
        try:
            db.session.add(journey)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "journeyId": journeyId
                    },
                    "message": "An error occurred creating the learning journey."
                }
            ), 500    
    

    # convert str to json
    addedCourses = json.loads(addedCourses)
    for course in addedCourses:
        # get course object from db
        tobeadded = Course.query.filter_by(Course_ID=course).first()
        try:
            # add into new journey & commit to db
            journey.courses.append(tobeadded)
            db.session.commit()
        except:
            return jsonify(
            {
                "code": 400,
                "data": {
                    "journeyId": journeyId,
                    "course_id": course
                },
                "message": "An error occurred creating the learning journey."
            }
        ), 400

    return jsonify(
        {
            "code": 200,
            "data": journey.json()
        }
    ), 200

# hard delete learning journey and its courses
@app.route("/journey/delete", methods=['POST'])
def delete_learning_journey():
    journeyId = request.get_json()["journeyId"]

    try:
        journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
        db.session.delete(journey)
        db.session.commit()
    except:
        return jsonify(
            {
            "code": 400,
            "data": journeyId
        }
    ), 400

    return jsonify(
        {
            "code": 200,
            "data": journeyId
        }
    ), 200
    
if __name__ == '__main__':
    app.run(debug=True)
