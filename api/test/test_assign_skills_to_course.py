import unittest
import flask_testing
import json
from Skills import Skill
from Courses import Course
from models import Skill_course
from app import app, db


# create a flask app for testing purposes
class TestApp(flask_testing.TestCase):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["TESTING"] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


# tests for get_skills_assigned_to_course
class TestGetAssignSkillsToCourses(TestApp):
    # test if the course is not found
    def test_no_course_found(self):
        response = self.client.get("/courses/COR001")
        self.assertEqual(response.json, {"code": 404,
                                         "message": "Course not found"})

    # test if no skills, it return 200 response but with an empty
    # selected_skill list
    def test_no_skills(self):
        course1 = Course(
            "COR001",
            "Systems Thinking and Design",
            "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "Active",
            "Internal",
            "Core",
        )
        db.session.add(course1)
        db.session.commit()
        response = self.client.get("/courses/COR001")
        self.assertEqual(
            response.json,
            {"code": 200, "data": [], "name": "Systems Thinking and Design"},
        )

    # test if no skill assigned to course, it return 200 response but with an
    # empty selected_skill list too
    def test_no_skills_assigned_to_course(self):
        skill1 = Skill(
            "BM01", "Brand Management", "Analysis on how to manage the brand"
        )
        course1 = Course(
            "COR001",
            "Systems Thinking and Design",
            "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "Active",
            "Internal",
            "Core",
        )
        db.session.add(skill1)
        db.session.add(course1)
        db.session.commit()
        response = self.client.get("/courses/COR001")
        self.assertEqual(
            response.json,
            {"code": 200, "data": [], "name": "Systems Thinking and Design"},
        )

    # test if 1 skill assign to the course, it return 200 response with the 
    # skill inside selected_skill list
    def test_get_assigned_courses(self):
        skill1 = Skill(
            "BM01", "Brand Management", "Analysis on how to manage the brand"
        )
        skill2 = Skill(
            "CM01",
            "Change Management",
            "For all approaches to prepare, support, and help organizations in making change.",
        )
        course1 = Course(
            "COR001",
            "Systems Thinking and Design",
            "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "Active",
            "Internal",
            "Core",
        )
        db.session.add(skill1)
        db.session.add(skill2)
        db.session.add(course1)
        course_skill = Skill_course.insert().values(Skill_ID="BM01",
                                                    Course_ID="COR001")
        db.session.commit()
        db.engine.execute(course_skill)

        response = self.client.get("/courses/COR001")
        self.assertEqual(
            response.json,
            {"code": 200, "data": ["BM01"],
                "name": "Systems Thinking and Design"},
        )


class TestUpdateAssignedSkillsToCourses(TestApp):
    # test if the course is not found
    def test_no_course_found(self):
        response = self.client.post("/hr/courses/edit/COR001")
        self.assertEqual(response.json, {"code": 404,
                                         "message": "Course not found"})

    # test if the json parsed in the post is correct format
    def test_data_sent_by_post_request(self):
        course1 = Course(
            "COR001",
            "Systems Thinking and Design",
            "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "Active",
            "Internal",
            "Core",
        )
        db.session.add(course1)
        db.session.commit()

        request_body = []
        response = self.client.post(
            "/hr/courses/edit/COR001",
            data=json.dumps(request_body),
            content_type="application/json",
        )
        self.assertEqual(
            response.json,
            {"code": 400,
             "message": "There must at least be one skill selected"},
        )
        self.assertEqual(response.status_code, 400)

    # test if the deleting of skills work
    def test_delete_of_skills_to_course(self):
        skill1 = Skill(
            "BM01", "Brand Management", "Analysis on how to manage the brand"
        )
        skill2 = Skill(
            "CM01",
            "Change Management",
            "For all approaches to prepare, support, and help organizations in making change.",
        )
        course1 = Course(
            "COR001",
            "Systems Thinking and Design",
            "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "Active",
            "Internal",
            "Core",
        )
        db.session.add(skill1)
        db.session.add(skill2)
        db.session.add(course1)
        db.session.commit()
        course_skill = Skill_course.insert().values(Skill_ID="BM01", 
                                                    Course_ID="COR001")
        course_skill2 = Skill_course.insert().values(
            Skill_ID="CM01", Course_ID="COR001"
        )
        db.engine.execute(course_skill)
        db.engine.execute(course_skill2)

        request_body = ["BM01"]
        response = self.client.post(
            "/hr/courses/edit/COR001",
            data=json.dumps(request_body),
            content_type="application/json",
        )

        self.assertEqual(
            response.json,
            {
                "code": 200,
                "data": {
                    "Course": "COR001",
                    "added list": [],
                    "deleted list": ["CM01"],
                },
                "message": "Course skills updated successfully.",
            },
        )
        self.assertEqual(response.status_code, 200)

    # test if the insert of skills to course work
    def test_insert_skills_to_course(self):
        skill1 = Skill(
            "BM01", "Brand Management", "Analysis on how to manage the brand"
        )
        skill2 = Skill(
            "CM01",
            "Change Management",
            "For all approaches to prepare, support, and help organizations in making change.",
        )
        course1 = Course(
            "COR001",
            "Systems Thinking and Design",
            "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "Active",
            "Internal",
            "Core",
        )
        db.session.add(skill1)
        db.session.add(skill2)
        db.session.add(course1)
        course_skill = Skill_course.insert().values(Skill_ID="BM01", Course_ID="COR001")
        db.session.commit()
        db.engine.execute(course_skill)

        request_body = ["BM01", "CM01"]
        response = self.client.post(
            "/hr/courses/edit/COR001",
            data=json.dumps(request_body),
            content_type="application/json",
        )

        self.assertEqual(
            response.json,
            {
                "code": 200,
                "data": {
                    "Course": "COR001",
                    "added list": ["CM01"],
                    "deleted list": [],
                },
                "message": "Course skills updated successfully.",
            },
        )
        self.assertEqual(response.status_code, 200)

    # test if both insert and delete of skills work together
    def test_delete_and_insert_skills_to_course(self):
        skill1 = Skill(
            "BM01", "Brand Management", "Analysis on how to manage the brand"
        )
        skill2 = Skill(
            "CM01",
            "Change Management",
            "For all approaches to prepare, support, and help in making change.",
        )
        skill3 = Skill(
            "LE02",
            "Leadership Management",
            "The process of planning, directing, and controlling the activities of employees to accomplish objectives.",
        )
        course1 = Course(
            "COR001",
            "Systems Thinking and Design",
            "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "Active",
            "Internal",
            "Core",
        )
        db.session.add(skill1)
        db.session.add(skill2)
        db.session.add(skill3)
        db.session.add(course1)
        course_skill = Skill_course.insert().values(Skill_ID="BM01", Course_ID="COR001")
        db.session.commit()
        db.engine.execute(course_skill)

        request_body = ["CM01", "LE02"]
        response = self.client.post(
            "/hr/courses/edit/COR001",
            data=json.dumps(request_body),
            content_type="application/json",
        )

        self.assertEqual(
            response.json,
            {
                "code": 200,
                "data": {
                    "Course": "COR001",
                    "added list": ["CM01", "LE02"],
                    "deleted list": ["BM01"],
                },
                "message": "Course skills updated successfully.",
            },
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
