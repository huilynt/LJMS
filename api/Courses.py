from flask import jsonify, request

from app import app, db
from models import Course, Skill, Skill_course


@app.route("/course")
def view_course():
    courselist = Course.query.all()
    return jsonify({
        "code": 200,
        "data": [course.json() for course in courselist]})


# retrieve one course information
@app.route("/course/<string:CourseId>")
def view_course_information(CourseId):
    course_info = Course.query.filter_by(Course_ID=CourseId).first()
    return jsonify({"code": 200, "data": course_info.json()})


# retrieve all courses related to a skill
@app.route("/<string:skillId>/courses")
def view_courses_for_a_skill(skillId):
    skill = Skill.query.filter_by(Skill_ID=skillId).first()

    course_list = []

    for course in skill.courses:
        if course.Course_Status == "Active":
            course_list.append(course)

    return jsonify(
        {
            "code": 200,
            "data": {
                "courses": [course.json() for course in course_list],
                "skill": skill.json(),
            },
        }
    )


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


# Add skills to existing course
@app.route("/hr/courses/edit/<string:courseId>", methods=["POST"])
def update_skills_to_course(courseId):
    course = Course.query.filter_by(Course_ID=courseId).first()
    if course:
        courseId = course.Course_ID
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

        # delete all unassignment of skills to the course
        all_skillcourse = db.session.query(Skill_course).filter_by(Course_ID=courseId).all()
        for skill in all_skillcourse:
            if skill.Skill_ID not in skills_list:
                try:
                    db.session.query(Skill_course).filter_by(Course_ID=courseId, Skill_ID=skill.Skill_ID).delete()
                    db.session.commit()
                    deleted_list.append(skill.Skill_ID)
                except Exception:
                    return {
                        "message": "Unable to commit to database."
                    }, 404

        # add the new assigned skills to courses
        for skillId in skills_list:
            check = db.session.query(Skill_course).filter_by(Course_ID=courseId, Skill_ID=skillId).first()
            if check is None:
                try:
                    course_skill = Skill_course.insert().values(Course_ID=courseId, Skill_ID=skillId)
                    db.engine.execute(course_skill)
                    added_list.append(skillId)
                except Exception:
                    return {
                        "message": "Unable to commit to database."
                    }, 404

        return jsonify(
            {
                "code": 200,
                "data": {
                    "Course": courseId,
                    "added list": added_list,
                    "deleted list": deleted_list
                },
                "message": "Course skills updated successfully."
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Course not found",
        }
    ), 404
