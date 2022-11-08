import unittest
import flask_testing
import json
from Skills import Skill
from app import app, db


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

# tests for view_skills, view_active_skills and view_skills_for_a_role
class TestViewSkill(TestApp):
    #test for able to view skill
    def test_view_all_skill(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/skill",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #test for able to view all active skills
    def test_view_all_active_skill(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/activeskill",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #test for able to find skills by skillid
    def test_find_by_skillid(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/skill/LE01",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #test if invalid skillid will cause an error
    def test_find_by_skillid_with_invalid_id(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/skill/TT200",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            'message': 'Skill not found.'
        })

    #test for no skill in db will cause an error
    def test_find_by_skillid_with_invalid_id(self):
        response = self.client.get("/skill/TT200",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
