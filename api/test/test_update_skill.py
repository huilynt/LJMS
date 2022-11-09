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
            "Skill_Name": "TestingName200",
            "Skill_Desc": "TestingDesc200"
        }

        response = self.client.put("/skill/LE01", data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # test if update skill with existing name will return error
    def test_update_invalid_skill_with_same_name(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            "Skill_Name": "Leadership Skill",
            "Skill_Desc": "Testing Description"
        }

        response = self.client.put("/skill/LE01", data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "data": {
                "skillId": "LE01"
            },
            "message": "Skill name is repeated."
        })

    # test if invalid skillid in url will return an error
    def test_update_invalid_skill_with_invalid_id(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        request_body = {
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
