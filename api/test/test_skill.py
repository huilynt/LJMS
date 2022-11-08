import unittest

from app import app
from Skills import Skill
import json

class TestSkills(unittest.TestCase):
    def test_skills_json(self):
        skill = Skill('CM01','Change Management','For all approaches to prepare, support, and help organizations in making change.')
        self.assertEqual(
            skill.json(),
            {
                "Skill_ID": 'CM01',
                "Skill_Name": 'Change Management',
                "Skill_Desc": 'For all approaches to prepare, support, and help organizations in making change.',
                "Skill_Status": ''
            }
        )


if __name__ == "__main__":
    unittest.main()

