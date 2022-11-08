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

#tests for delete_a_skill
class TestDeleteSkill(TestApp):
    #test if delete a skill work as intended
    def test_delete_a_skill(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.delete("/skill/LE01",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #test if invalid skillid in url will return an error
    def test_delete_invalid_skill_with_invalid_id(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.delete("/skill/TT200",
                                    content_type='application/json')
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
