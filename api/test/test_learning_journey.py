import unittest
from app import LearningJourney


class LearningJourneys(unittest.TestCase):
    def test_learning_journey_json(self):
        lj = LearningJourney("EN001-160212", "EN001", "160212", "Progress")
        self.assertEqual(
            lj.json(),
            {
                "Journey_ID": "EN001-160212",
                "Staff_ID":  "160212",
                "JobRole_ID": "EN001",
                "LearningJourney_Status": "Progress"
            }
        )


if __name__ == "__main__":
    unittest.main()
