import unittest
from unittest.mock import patch
import flask_testing
from Skills import Skill
from Courses import Course
from models import Skill_course
from app import app,db 

# create a flask app for testing purposes
class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

# tests for get_skills_assigned_to_course
class TestAssignSkillsToCourses(TestApp):
    # test if the course is not found
    def test_no_course_found(self):
        response = self.client.get("/courses/COR001")
        self.assertEqual(response.json, 
            {
                "code": 404,
                "message": "Course not found"
            }
        )

    # test if no skills, it return 200 response but with an empty selected_skill list
    def test_no_skills(self):
        course1 = Course('COR001','Systems Thinking and Design','This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking', 'Active', 'Internal', 'Core')
        db.session.add(course1)
        db.session.commit()
        response = self.client.get("/courses/COR001")
        self.assertEqual(response.json, 
            {
                "code": 200,
                "data": [],
                "name": "Systems Thinking and Design"
            }
        )
    
    # test if no skill assigned to course, it return 200 response but with an empty selected_skill list too
    def test_no_skills_assigned_to_course(self):
        skill1 = Skill('BM01','Brand Management','Analysis on how to manage the brand')
        skill2 = Skill('CM01','Change Management','For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.')
        course1 = Course('COR001','Systems Thinking and Design','This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking', 'Active', 'Internal', 'Core')
        db.session.add(skill1)
        db.session.add(skill1)
        db.session.add(course1)
        db.session.commit()
        response = self.client.get("/courses/COR001")
        self.assertEqual(response.json, 
            {
                "code": 200,
                "data": [],
                "name": "Systems Thinking and Design"
            }
        )

    # test if 1 skill assign to the course, it return 200 response with the skill inside selected_skill list
    def test_get_assigned_courses(self):
        skill1 = Skill('BM01','Brand Management','Analysis on how to manage the brand')
        skill2 = Skill('CM01','Change Management','For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.')
        course1 = Course('COR001','Systems Thinking and Design','This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking', 'Active', 'Internal', 'Core')
        db.session.add(skill1)
        db.session.add(skill2)
        db.session.add(course1)
        course_skill = Skill_course.insert().values(Skill_ID='BM01',Course_ID='COR001')
        db.session.commit()
        db.engine.execute(course_skill)
        response = self.client.get("/courses/COR001")
        self.assertEqual(response.json, 
            {
                "code": 200,
                "data": ['BM01'],
                "name": "Systems Thinking and Design"
            }
        )

if __name__ == '__main__':
    unittest.main()