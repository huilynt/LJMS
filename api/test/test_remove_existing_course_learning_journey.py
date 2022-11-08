import unittest
import flask_testing
from app import app, db
from models import LearningJourney, Course, LearningJourney_SelectedCourse
from Journey import remove_existing_course_learning_journey



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


class RemoveExistingCourse(TestApp):

    def test_existing_course_not_found(self):
        lj_obj = LearningJourney("EN002-140525","EN002",'140525','Progress')
        
        db.session.add(lj_obj)
        db.session.commit()
        response = self.client.delete("/journey/EN001-130001/COR001")
        self.assertEqual(response.json,  {
            "code": 404,
            "data": {
                "journeyId": 'EN002-140525',
                "courseId": 'COR002'
            },
            "message": "Course in selected Learning Journey not found"
        })
        self.assertEqual(response.status_code, 404)

    def test_at_least_one_course(self):
        lj_obj = LearningJourney("EN001-130001","EN001",'130001','Progress')
        lj_course = Course('COR001',
                            'Systems Thinking and Design',
                            'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking',
                            'Active','Internal','Core')
        db.session.add(lj_obj)
        db.session(lj_course)
        LearningJourney_SelectedCourse.insert(Journey_ID='EN001-130001', Course_ID='COR001')
        db.session.commit()

        response = self.client.delete("/journey/EN001-130001/COR001")
        self.assertEqual(response.json, {
                                        "code": 200,
                                        "message": "Only one course left"
                                    })
        self.assertEqual(response.status_code, 200)


    def test_remove_existing_course(self):
        lj_obj = LearningJourney("EN002-140525","EN002",'140525','Progress')
        lj_course1 = Course('COR002',
                            'Lean Six Sigma Green Belt Certification',
                            'Apply Lean Six Sigma methodology and statistical tools such as Minitab to be used in process analytics',
                            'Active','Internal','Core')
        lj_course1 = Course('COR006',
                            'Manage Change',
                            'Identify risks associated with change and develop risk mitigation plans.',
                            'Active','External','Core')

        db.session.add(lj_obj)
        db.session.add(lj_course1)
        db.session.add(lj_course2)
        LearningJourney_SelectedCourse.insert(Journey_ID='EN002-140525', Course_ID='COR002')
        LearningJourney_SelectedCourse.insert(Journey_ID='EN002-140525', Course_ID='COR006')
        db.session.commit()

        response = self.client.delete("/journey/EN002-140525/COR002")
        self.assertEqual(response.json, {
                                        "code": 200,
                                        "message": "Delete success"
                                    })
        self.assertEqual(response.status_code, 200)

    


if __name__ == '__main__':
    unittest.main()