import unittest
from unittest.mock import patch
from api.models import JobRole
import flask_testing
import json
from Skills import Skill
from JobRoles import JobRole
from models import Jobrole_skill
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

class TestUpdateRoleHr(TestApp):
    # test if the jobrole is not found
    def test_no_jobrole_found(self):
        response = self.client.post("/hr/roles/edit/DA001")
        self.assertEqual(response.json, 
            {
                "code": 404,
                "message": "Role not found"
            }
        )

    # # test if the json parsed in the post is correct format
    # def test_data_sent_by_post_request(self):
    #     jobrole1 = JobRole('DA001',
    #                     'Data Analyst',
    #                     'The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.', 
    #                     'NULL')
    #     db.session.add(jobrole1)
    #     db.session.commit()

    #     request_body = []
    #     response = self.client.post("/hr/roles/edit/DA001", 
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')
    #     self.assertEqual(response.json, 
    #         {
    #             "code": 400,
    #             "message": "There must at least be one skill selected"
    #         }
    #     )
    #     self.assertEqual(response.status_code, 400)

    # # test if the deleting of skills work
    # def test_delete_of_skills_to_course(self):
    #     skill1 = Skill('BM01','Brand Management','Analysis on how to manage the brand')
    #     skill2 = Skill('CM01','Change Management','For all approaches to prepare, support, and help organizations in making change.')
    #     jobrole1 = JobRole('DA001',
    #                     'Data Analyst',
    #                     'The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.', 
    #                     'NULL')
    #     db.session.add(skill1)
    #     db.session.add(skill2)
    #     db.session.add(course1)
    #     db.session.commit()
    #     course_skill = Skill_course.insert().values(Skill_ID='BM01',Course_ID='COR001')
    #     course_skill2 = Skill_course.insert().values(Skill_ID='CM01',Course_ID='COR001')
    #     db.engine.execute(course_skill)
    #     db.engine.execute(course_skill2)

    #     request_body = ['BM01']
    #     response = self.client.post("/hr/courses/edit/COR001", 
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')

    #     self.assertEqual(response.json, 
    #         {
    #             "code": 200,
    #             "data": {
    #                 "Course": "COR001",
    #                 "added list": [],
    #                 "deleted list": ["CM01"]
    #             },
    #             "message": "Course skills updated successfully."
    #         }
    #     )
    #     self.assertEqual(response.status_code, 200)

    # # test if the insert of skills to course work
    # def test_insert_skills_to_course(self):
    #     skill1 = Skill('BM01','Brand Management','Analysis on how to manage the brand')
    #     skill2 = Skill('CM01','Change Management','For all approaches to prepare, support, and help organizations in making change.')
    #     course1 = Course('COR001',
    #                     'Systems Thinking and Design',
    #                     'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking', 
    #                     'Active', 
    #                     'Internal', 
    #                     'Core')
    #     db.session.add(skill1)
    #     db.session.add(skill2)
    #     db.session.add(course1)
    #     course_skill = Skill_course.insert().values(Skill_ID='BM01',Course_ID='COR001')
    #     db.session.commit()
    #     db.engine.execute(course_skill)

    #     request_body = ['BM01','CM01']
    #     response = self.client.post("/hr/courses/edit/COR001", 
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')

    #     self.assertEqual(response.json, 
    #         {
    #             "code": 200,
    #             "data": {
    #                 "Course": "COR001",
    #                 "added list": ["CM01"],
    #                 "deleted list": []
    #             },
    #             "message": "Course skills updated successfully."
    #         }
    #     )
    #     self.assertEqual(response.status_code, 200)

    # # test if both insert and delete of skills work together
    # def test_delete_and_insert_skills_to_course(self):
    #     skill1 = Skill('BM01','Brand Management','Analysis on how to manage the brand')
    #     skill2 = Skill('CM01','Change Management','For all approaches to prepare, support, and help in making change.')
    #     skill3 = Skill('LE02','Leadership Management','The process of planning, directing, and controlling the activities of employees to accomplish objectives.')
    #     course1 = Course('COR001',
    #             'Systems Thinking and Design',
    #             'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking', 
    #             'Active', 'Internal', 'Core')
    #     db.session.add(skill1)
    #     db.session.add(skill2)
    #     db.session.add(skill3)
    #     db.session.add(course1)
    #     course_skill = Skill_course.insert().values(Skill_ID='BM01',Course_ID='COR001')
    #     db.session.commit()
    #     db.engine.execute(course_skill)

    #     request_body = ['CM01','LE02']
    #     response = self.client.post("/hr/courses/edit/COR001", 
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')

    #     self.assertEqual(response.json, 
    #         {
    #             "code": 200,
    #             "data": {
    #                 "Course": "COR001",
    #                 "added list": ['CM01','LE02'],
    #                 "deleted list": ['BM01']
    #             },
    #             "message": "Course skills updated successfully."
    #         }
    #     )
    #     self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()