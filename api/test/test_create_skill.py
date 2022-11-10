import unittest
import flask_testing
import json
from Skills import Skill
from app import app, db


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


# tests for create_a_skill
class TestCreateSkill(TestApp):
    # test for create a skill work as intended
    def test_create_skill(self):
        request_body = {
            "Skill_ID": "LE01",
            "Skill_Name": "Leadership Skill",
            "Skill_Desc": "How to be a leader"
        }

        response = self.client.post("/skill/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Skill_ID": "LE01",
                "Skill_Name": "Leadership Skill",
                "Skill_Desc": "How to be a leader",
                "Skill_Status": ""
            }
        })

    # test for creating skill with existing id will return error
    def test_create_invalid_skill_with_same_id(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            "Skill_ID": "LE01",
            "Skill_Name": "Testing Name",
            "Skill_Desc": "Testing Desc"
        }

        response = self.client.post("/skill/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "code": 400,
            "data": {
                "skillId": "LE01"
            },
            "message": "Skill ID already exists."
        })

    # test for creating skill with existing name will return error
    def test_create_invalid_skill_with_same_name(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            "Skill_ID": "TT200",
            "Skill_Name": "Leadership Skill",
            "Skill_Desc": "Testing Desc"
        }

        response = self.client.post("/skill/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "code": 400,
            "data": {
                "skillname": "Leadership Skill"
            },
            "message": "Skill Name already exists."
        })


if __name__ == '__main__':
    unittest.main()
