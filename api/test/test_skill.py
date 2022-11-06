import unittest

from app import app
from Skills import Skill
import json

class TestSkills(unittest.TestCase):
    def test_skills_json(self):
        skill = Skill('CM01','Change Management','For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.')
        self.assertEqual(
            skill.json(),
            {
                "Skill_ID": 'CM01',
                "Skill_Name": 'Change Management',
                "Skill_Desc": 'For all approaches to prepare, support, and help individuals, teams, and organizations in making organizational change.',
                "Skill_Status": ''
            }
        )

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_view_course(self):
        response = self.client.get("/course")
        assert response.status_code == 200

    def test_view_skills_for_a_role(self):
        response = self.client.get("/DA001/skills")
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))

        # self.assertEqual(data['data2'], ["DM01"])
        self.assertEqual(data['role'], "Data Analyst")

    # def test_check_skills_completed(self):
    #     response = self.client.post("/skills/complete/DA001", data=json.dumps(dict(userId=140001)), content_type='application/json')
    #     assert response.status_code == 200
    #     data = json.loads(response.get_data(as_text=True))

    #     self.assertEqual(data['role'], "Data Analyst")


    # def test_home(self): #example from internet
    #     response = self.client.post("/", data={"content": "hello world"})
    #     assert response.status_code == 200
    #     assert "POST method called" == response.get_data(as_text=True)

if __name__ == "__main__":
    unittest.main()

