from flask import jsonify, request

from app import app, db
from models import Course, Skill, Skill_course

@app.route("/course")
def view_course():
    courselist = Course.query.all()
    return jsonify(
        {
            "code": 200, 
            "data": [course.json() for course in courselist]
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

# return the skills assigned to the specific course
@app.route("/courses/<string:courseId>")
def get_assgined_skills_to_course(courseId):
    skillList = Skill.query.all()
    course = Course.query.filter_by(Course_ID=courseId).first()
    selected_skills = []

    if course:
        for skill in skillList:
            courseList = skill.courses
            if course in courseList:
                selected_skills.append(skill.Skill_ID)

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
            "message": "Course not found",
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