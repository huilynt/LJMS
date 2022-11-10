import unittest
from app import Role


class Roles(unittest.TestCase):
    def test_role_json(self):
        role = Role("1", "Admin")
        self.assertEqual(
            role.json(),
            {
                "Role_ID": "1",
                "Role_Name": "Admin"
            }
        )


if __name__ == "__main__":
    unittest.main()
