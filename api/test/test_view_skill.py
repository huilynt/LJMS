import unittest
import flask_testing
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


# tests for view_skills, view_active_skills and view_skills_for_a_role
class TestViewSkill(TestApp):
    # test for able to view skill
    def test_view_all_skill(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/skill", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": [{
                "Skill_Desc": "How to be a leader",
                "Skill_ID": "LE01",
                "Skill_Name": "Leadership Skill",
                "Skill_Status": None
            }]
        })

    # test for able to view all active skills
    def test_view_all_active_skill(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        s2 = Skill("LE02", "Leadership Skills 2", "How to be a leader 2", "Retired")
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        response = self.client.get("/activeskill", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": [{
                "Skill_ID": "LE01",
                "Skill_Name": "Leadership Skill",
                "Skill_Desc": "How to be a leader",
                "Skill_Status": None
            }]
        })

    # test for able to find skills by skillid
    def test_find_by_skillid(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/skill/LE01", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": {
                "Skill_ID": "LE01",
                "Skill_Name": "Leadership Skill",
                "Skill_Desc": "How to be a leader",
                "Skill_Status": None
            }
        })

    # test if invalid skillid will cause an error
    def test_find_by_skillid_with_invalid_id(self):
        s1 = Skill("LE01", "Leadership Skill", "How to be a leader")
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/skill/TT200", content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "code": 404,
            "message": "Skill not found."
        })


if __name__ == '__main__':
    unittest.main()
