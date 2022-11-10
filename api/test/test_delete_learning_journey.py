import unittest
from models import LearningJourney
from app import db, app
import flask_testing


# create a flask app for testing purposes
class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        lj_obj = LearningJourney(
                                    Journey_ID="DA001-140525",
                                    JobRole_ID="DA001",
                                    Staff_ID=140525
                                )
        db.session.add(lj_obj)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestDeleteLearningJourney(TestApp):
    def test_valid(self):
        res = self.client.post('/journey/delete', json={
                "journeyId": "DA001-140525"
            }
        )
        res_data = res.get_json()
        self.assertEqual(res_data["code"], 200)

    def test_invalid(self):
        res = self.client.post('/journey/delete', json={
                "journeyId": "DA002-140525"
            }
        )
        res_data = res.get_json()
        self.assertEqual(res_data["code"], 400)


if __name__ == '__main__':
    unittest.main()