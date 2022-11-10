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


# tests for update_a_skill
class TestUpdateSkill(TestApp):
    # test if update a skill work as intended
    def test_update_a_skill(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            "Skill_ID": "LE01",
            "Skill_Name": "TestingName200",
            "Skill_Desc": "TestingDesc200"
        }

        response = self.client.put("/skill/LE01", data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Skill_ID": "LE01",
                "Skill_Name": "TestingName200",
                "Skill_Desc": "TestingDesc200",
                "Skill_Status": None
            }
        })

    # test if update skill with existing name will return error
    def test_update_invalid_skill_with_same_name(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        s2 = Skill("CM01", "Change Management", "For all approaches to prepare, support, and help organizations in making change.")
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        request_body = {
            "Skill_ID": "CM01",
            "Skill_Name": "Leadership Skill",
            "Skill_Desc": "Testing Description"
        }

        response = self.client.put("/skill/CM01", data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "data": {
                "skillId": "CM01"
            },
            "message": "Skill name is repeated."
        })

    # test if invalid skillid in url will return an error
    def test_update_invalid_skill_with_invalid_id(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            "Skill_ID": "TT200",
            "Skill_Name": "Testing Name",
            "Skill_Desc": "Testing Description"
        }

        response = self.client.put("/skill/TT200", data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "data": {
                "skillId": "TT200"
            },
            'message': 'Skill not found.'
        })


if __name__ == '__main__':
    unittest.main()
