from flask import jsonify, request

from app import app, db
from models import (
    Course,
    Staff,
    Registration,
    JobRole,
    Skill,
    LearningJourney,
    LearningJourney_SelectedCourse,
)
import Skills
import requests
import json


# get all courses a staff has added in Learning Journey
@app.route("/staff/courses/added", methods=["POST"])
def staff_courses_completed():
    userId = request.get_json()["userId"]
    roleId = request.get_json()["roleId"]
    journeyId = roleId + "-" + userId
    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()

    if journey:
        return (
            jsonify(
                {"code": 200, "data": [course.Course_ID for course in journey.courses]}
            ),
            200,
        )

    return jsonify({"code": 404, "message": "No Learning Journey"}), 404


# retrieve all user learning journey
@app.route("/learningjourney", methods=["POST"])
def view_leaningjourney():
    userId = request.get_json()["userId"]
    registration = Staff.query.filter_by(Staff_ID=userId).first()

    if registration:
        learningjourneylist = LearningJourney.query.filter_by(Staff_ID=userId).all()

        for journey in learningjourneylist:
            if journey.LearningJourney_Status == "Progress":
                url = "http://127.0.0.1:5000/journey/progress/" + journey.Journey_ID
                x = requests.post(url, json={"userId": userId})
                code = json.loads(x.text)["code"]
                if code == 200:
                    update_journey_completion(
                        journey.Journey_ID, json.loads(x.text)["data"]
                    )

        if learningjourneylist:
            return jsonify(
                {
                    "code": 200,
                    "data": [
                        learningjourney.json()
                        for learningjourney in learningjourneylist
                    ],
                }
            )

    return (
        jsonify({"code": 404, "message": "Staff has no existing learning journey."}),
        404,
    )


def update_journey_completion(journeyId, skill_list):
    completed_cnt = 0
    for skill in skill_list:
        if skill["Completion_Status"] is True:
            completed_cnt += 1

    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    role = JobRole.query.filter_by(JobRole_ID=journey.JobRole_ID).first()

    if len(role.skills) == completed_cnt:
        if journey:
            journey.LearningJourney_Status = "Completed"
            db.session.commit()
            return jsonify({"code": 200, "data": journey.json()})

    return (
        jsonify({"code": 404, "message": "Staff has no existing learning journey."}),
        404,
    )


@app.route("/journey/progress/<string:journeyId>", methods=["POST"])
def get_skills_progress(journeyId):
    userId = request.get_json()["userId"]
    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()

    skill_list = []
    check_skill_list = Skills.view_skills_for_a_role(journey.JobRole_ID)
    if check_skill_list["code"] == 200:
        skill_list = check_skill_list["data"]

    courses_added = journey.courses
    if journey and skill_list:
        for i in range(len(skill_list)):
            course_found = False
            skill_id = skill_list[i]["Skill_ID"]
            skill = Skill.query.filter_by(Skill_ID=skill_id).first()
            for course in courses_added:
                if course in skill.courses:
                    course_regi = Registration.query.filter_by(
                        Staff_ID=userId, Course_ID=course.Course_ID
                    ).first()
                    if course_regi:
                        if course_regi.Completion_Status == "Completed":
                            course_found = True
            skill_list[i]["Completion_Status"] = course_found

        jobrole = JobRole.query.filter_by(JobRole_ID=journey.JobRole_ID).first()

        return (
            jsonify({"code": 200, "data": skill_list, "role": jobrole.JobRole_Name}),
            201,
        )

    return jsonify({"code": 404, "message": "Journey not found"}), 404


@app.route("/journey/<string:journeyId>", methods=["POST"])
def get_courses_in_journey(journeyId):
    userId = request.get_json()["userId"]
    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    course_list = [course.json() for course in journey.courses]
    skill_list = JobRole.query.filter_by(JobRole_ID=journey.JobRole_ID).first().skills

    for i in range(len(course_list)):
        course_found = False
        course = course_list[i]
        registration = Registration.query.filter_by(
            Staff_ID=userId, Course_ID=course["Course_ID"]
        ).first()
        if registration is not None:
            status = registration.Completion_Status
            if status == "Completed":
                course_found = True

        course_list[i]["Completion_Status"] = course_found

    for j in range(len(journey.courses)):
        course = journey.courses[j]
        course_list[j]["skills"] = []
        if course.Course_Status != "Retired":
            for skill in skill_list:
                if course in skill.courses and skill.Skill_Status != "Retired":
                    if "skills" in course_list[j]:
                        course_list[j]["skills"].append(skill.json())
                    else:
                        course_list[j]["skills"] = [skill.json()]

    return jsonify({"code": 200, "data": course_list}), 201


@app.route("/journey/<string:journeyId>/<string:courseId>", methods=["DELETE"])
def remove_existing_course_learning_journey(journeyId, courseId):
    learningjourney = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    if len(learningjourney.courses) > 1:
        for course in learningjourney.courses:
            if course.Course_ID == courseId:
                try:
                    db.session.query(LearningJourney_SelectedCourse).filter_by(
                        Course_ID=courseId, Journey_ID=journeyId
                    ).delete()
                    db.session.commit()
                    return jsonify({"code": 200, "message": "Delete success"}), 201
                except:
                    return (
                        jsonify(
                            {
                                "code": 404,
                                "data": {"journeyId": journeyId, "courseId": courseId},
                                "message": "Course in selected Learning Journey not found",
                            }
                        ),
                        404,
                    )
    else:
        return jsonify({"code": 200, "message": "Only one course left"}), 201
    return (
        jsonify(
            {
                "code": 404,
                "data": {"journeyId": journeyId, "courseId": courseId},
                "message": "Course in selected Learning Journey not found",
            }
        ),
        404,
    )


# save learning journey with added courses
@app.route("/journey/<string:staffId>/<string:jobRoleId>", methods=["POST"])
def save_learning_journey(staffId, jobRoleId):
    journeyId = jobRoleId + "-" + staffId
    print(journeyId)
    addedCourses = request.get_json()["addedCourses"]

    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    if journey is None:
        journey = LearningJourney(
            Journey_ID=journeyId,
            Staff_ID=staffId,
            JobRole_ID=jobRoleId,
            LearningJourney_Status="Progress",
        )
        try:
            db.session.add(journey)
            db.session.commit()
        except:
            return (
                jsonify(
                    {
                        "code": 500,
                        "data": {"journeyId": journeyId},
                        "message": "An error occurred creating the learning journey.",
                    }
                ),
                500,
            )

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
            return (
                jsonify(
                    {
                        "code": 400,
                        "data": {"journeyId": journeyId, "course_id": course},
                        "message": "An error occurred creating the learning journey.",
                    }
                ),
                400,
            )

    return jsonify({"code": 200, "data": journey.json()}), 200


# hard delete learning journey and its courses
@app.route("/journey/delete", methods=["POST"])
def delete_learning_journey():
    journeyId = request.get_json()["journeyId"]

    try:
        journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
        db.session.delete(journey)
        db.session.commit()
    except:
        return jsonify({"code": 400, "data": journeyId}), 400

    return jsonify({"code": 200, "data": journeyId}), 200


@app.route("/journey/add/course/<string:jobRoleId>/<string:courseId>", methods=["POST"])
def add_course_in_learning_journey(jobRoleId, courseId):
    staffId = request.get_json()["staffId"]
    journeyId = jobRoleId + "-" + staffId
    journey = LearningJourney.query.filter_by(Journey_ID=journeyId).first()
    tobeadded = Course.query.filter_by(Course_ID=courseId).first()
    try:
        # add into new journey & commit to db
        journey.courses.append(tobeadded)
        db.session.commit()
    except:
        return (
            jsonify(
                {
                    "code": 400,
                    "data": {"journeyId": journeyId, "course_id": courseId},
                    "message": "An error occurred creating the learning journey.",
                }
            ),
            400,
        )

    return jsonify({"code": 200, "data": journey.json()}), 200
