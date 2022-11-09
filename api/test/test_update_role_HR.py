import unittest
from JobRoles import JobRole
import flask_testing
from app import app, db


# create a flask app for testing purposes
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


class TestUpdateRoleHr(TestApp):
    def test_jobrole_is_repeated(self):
        jobrole1 = JobRole('DA001', 'Data Analyst', 'The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.', 'Active')
        jobrole2 = JobRole('EN001', 'Software Engineer', 'The role focus on applying the principles of engineering to software development.', 'Active')

        db.session.add(jobrole1)
        db.session.add(jobrole2)
        db.session.commit()

        request_body = {
                "JobRole_Name": "Software Engineer",
                "JobRole_Desc": "The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems."
            }
        response = self.client.put("/jobrole/DA001", json=request_body)
        self.assertEqual(response.json, {
            "code": 404,
            "data": {
                "jobroleId": "DA001",
                "existing job role": "Data Analyst",
                "updated job role": "Software Engineer"
            },
            "message": "Role name is repeated."
        })
        self.assertEqual(response.status_code, 404)

    def test_jobrole_is_found(self):
        jobrole1 = JobRole('DA001', 'Data Analyst', 'The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.', 'Active')
        jobrole2 = JobRole('EN001', 'Software Engineer', 'The role focus on applying the principles of engineering to software development.', 'Active')
        
        db.session.add(jobrole1)
        db.session.add(jobrole2)
        db.session.commit()

        response = self.client.put("/jobrole/DA001", json={
            "JobRole_Name": "Data Scientist",
            "JobRole_Desc": "The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems."
            })

        self.assertEqual(response.json,  {
            "code": 200,
            "data": {
                "JobRole_ID": 'DA001',
                "JobRole_Name": 'Data Scientist',
                "JobRole_Desc": 'The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.',
                "JobRole_Status": "Active"
                }
        })

    def test_jobrole_not_found(self):
        jobrole = JobRole('DA001', 'Data Analyst', 'The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.', 'Active')

        db.session.add(jobrole)
        db.session.commit()

        response = self.client.put("/jobrole/DA002", json={
            "JobRole_Name": "Data Analyst",
            "JobRole_Desc": "The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems."
            })

        self.assertEqual(response.json, {
            "code": 404,
            "data": {
                "jobroleId": "DA002"
            },
            "message": "Role not found."
        })


if __name__ == '__main__':
    unittest.main()
