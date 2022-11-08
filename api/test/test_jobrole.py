import unittest
from app import JobRole

class JobRoles(unittest.TestCase):
    def test_jobrole_json(self):
        jobRole = JobRole(
            "DA001", 
            "Data Analyst" , 
            "The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.", 
            "")
        self.assertEqual(
            jobRole.json(),
            {
                "JobRole_ID": "DA001",
                "JobRole_Name":  "Data Analyst",
                "JobRole_Desc":"The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.", 
                "JobRole_Status":""
            }
        )

if __name__ == "__main__":
    unittest.main()