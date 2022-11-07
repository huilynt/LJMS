import unittest
from app import LearningJourney, db, app

lj_obj = LearningJourney(Journey_ID="DA001-140525", JobRole_ID="DA001", Staff_ID=140525)


def _init_db():
    for obj in db.session:
        print(obj, "init")
    db.session.add(lj_obj)
    db.session.commit()


def _exit_db():

    db.session.close()


class TestDeleteLearningJourney(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.app.config = app.config
        self.app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql+mysqlconnector://root@localhost:3306/ljps_test"

        db.create_all()
        _init_db()
        return super().setUp()

    def tearDown(self) -> None:
        _exit_db()
        self.app_context.pop()
        return super().tearDown()

    def test_valid(self):
        res = self.app.post("/journey/delete", json={"journeyId": "DA001-140525"})
        res_data = res.get_json()
        self.assertEqual(res_data["code"], 200)

    def test_invalid(self):
        res = self.app.post("/journey/delete", json={"journeyId": "DA002-140525"})
        res_data = res.get_json()
        self.assertEqual(res_data["code"], 400)


if __name__ == "__main__":
    unittest.main()
