from flask import Flask
import unittest
from app import LearningJourney, LearningJourney_SelectedCourse, db, app, delete_learning_journey

lj_obj = LearningJourney(
    Journey_ID="DA001-140525",
    JobRole_ID="DA001",
    Staff_ID=140525
)
def _init_db():
    db.session.add(lj_obj)
    db.session.commit()

class TestDeleteLearningJourney(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.app.config = app.config
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/ljps_test"
        db.create_all()
        _init_db()
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()

    def test_index(self):
        res = self.app.post('/journey/delete',
            json={
                "journeyId": "DA001-140525"
            }
        )
        res_data = res.get_json()
        self.assertEqual(res_data["code"], 200)


if __name__ == '__main__':
    unittest.main()