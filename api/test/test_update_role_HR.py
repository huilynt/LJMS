import unittest
from unittest.mock import patch
from api.models import JobRole
import flask_testing
import json
from Skills import Skill
from JobRoles import JobRole
from models import Jobrole_skill
from app import app,db 

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

class TestUpdateRoleHr(TestApp):
     def test_jobrole_not_found(self):
        jobrole= JobRole('DA001','Data Analyst','The role requires you to make recommendations about the methods and ways in which a company obtains and analyses data to improve quality and the efficiency of data systems.')
        
        db.session.add(jobrole)
        db.session.commit()

        response = self.client.put("/jobrole/DA001", 
        json={"JobRole_Name": "Data Analyst"})
        self.assertEqual(response.json,  {
            "code": 404,
            "data": {
                "jobroleId": jobroleId
            },
            "message": "Role name is repeated."
        })


if __name__ == '__main__':
    unittest.main()