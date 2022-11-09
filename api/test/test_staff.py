import unittest
from app import Staff


class Staffs(unittest.TestCase):
    def test_staff_json(self):
        staff = Staff("130001", "John" , "Sim", "Chairman", "jack.sim@allinone.com.sg", "1")
        self.assertEqual(
            staff.json(),
            {
                "Staff_ID": "130001",
                "Staff_FName":  "John",
                "Staff_LName":  "Sim",
                "Dept": "Chairman",
                "Email": "jack.sim@allinone.com.sg",
                "Role": "1"
            }
        )


if __name__ == "__main__":
    unittest.main()
