import unittest
import flask_testing
import json
from Skills import Skill
from JobRoles import JobRole
from models import Jobrole_skill
from app import app, db


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


# tests for get_skills_assigned_to_role
class TestGetAssignSkillsToRole(TestApp):
    # test if the course is not found
    def test_no_course_found(self):
        response = self.client.get("/jobrole/assignedskills/CO001")
        self.assertEqual(response.json, {
                "code": 404,
                "message": "Jobrole not found"
            }
        )

    # test if no skills, it return 200 response but with an empty selected_skill list
    def test_no_skills(self):
        j1 = JobRole("CO001", "C-level Executive", "Play a strategic role within an organization; they hold senior positions and impact company-wide decisions")
        db.session.add(j1)
        db.session.commit()
        response = self.client.get("/jobrole/assignedskills/CO001")
        self.assertEqual(response.json, {
                "code": 200,
                "data": [],
            }
        )

    # test if no skill assigned to role, it return 200 response but with an empty selected_skill list too
    def test_no_skills_assigned_to_course(self):
        s1 = Skill('BM01','Brand Management', 'Analysis on how to manage the brand')
        j1 = JobRole("CO001", "C-level Executive", "Play a strategic role within an organization; they hold senior positions and impact company-wide decisions")
        db.session.add(s1)
        db.session.add(j1)
        db.session.commit()
        response = self.client.get("/jobrole/assignedskills/CO001")
        self.assertEqual(response.json, {
                "code": 200,
                "data": [],
            }
        )

    # test if 1 skill assign to the role, it return 200 response with the skill inside selected_skill list
    def test_get_assigned_skills(self):
        s1 = Skill('BM01','Brand Management','Analysis on how to manage the brand')
        j1 = JobRole("CO001", "C-level Executive", "Play a strategic role within an organization; they hold senior positions and impact company-wide decisions")
        db.session.add(s1)
        db.session.add(j1)
        db.session.commit()
        role_skill = Jobrole_skill.insert().values(JobRole_ID='CO001', Skill_ID='BM01')
        db.engine.execute(role_skill)

        s2 = Skill('CM01', 'Change Management','For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.')
        db.session.add(s2)
        db.session.commit()

        response = self.client.get("/jobrole/assignedskills/CO001")
        self.assertEqual(response.json, {
                "code": 200,
                "data": ['BM01'],
            }
        )


class TestUpdateAssignedSkillsToRoles(TestApp):
    # test if the role is not found
    def test_no_role_found(self):
        response = self.client.post("/hr/jobrole/edit/CO001")
        self.assertEqual(response.json, {
                "code": 404,
                "message": "Jobrole not found"
            }
        )

    # test if the json parsed in the post is correct format
    def test_data_sent_by_post_request(self):
        j1 = JobRole("CO001", "C-level Executive", "Play a strategic role within an organization; they hold senior positions and impact company-wide decisions")
        db.session.add(j1)
        db.session.commit()

        request_body = []
        response = self.client.post("/hr/jobrole/edit/CO001",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
                "code": 400,
                "message": "There must at least be one skill selected"
            }
        )
        self.assertEqual(response.status_code, 400)

    # test if the deleting of skills work
    def test_delete_all_skills_of_role(self):
        s1 = Skill('BM01', 'Brand Management', 'Analysis on how to manage the brand')
        s2 = Skill('CM01', 'Change Management', 'For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.')
        s3 = Skill('LE01', 'Leadership Skill', 'How to be a leader')
        j1 = JobRole("CO001", "C-level Executive", "Play a strategic role within an organization; they hold senior positions and impact company-wide decisions")
        db.session.add(s1)
        db.session.add(j1)
        role_skill1 = Jobrole_skill.insert().values(JobRole_ID='CO001', Skill_ID='BM01')
        db.session.commit()
        db.engine.execute(role_skill1)

        db.session.add(s2)
        role_skill2 = Jobrole_skill.insert().values(JobRole_ID='CO001', Skill_ID='CM01')
        db.session.commit()
        db.engine.execute(role_skill2)

        db.session.add(s3)
        db.session.commit()

        request_body = ['LE01']
        response = self.client.post("/hr/jobrole/edit/CO001",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
                "code": 200,
                "data": {
                    "Jobrole": "CO001",
                    "added list": ['LE01'],
                    "deleted list": ["BM01", "CM01"]
                },
                "message": "Jobrole skills updated successfully."
            }
        )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
