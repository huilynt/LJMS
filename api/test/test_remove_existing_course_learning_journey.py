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
        lj_obj = LearningJourney("EN001-130001","EN001",'130001','Progress')
        
        db.session.add(lj_course)
        db.session.commit()
        response = self.client.delete("/journey/EN001-130001/COR001")
        self.assertEqual(response.json,  {
            "code": 404,
            "data": {
                "journeyId": 'EN001-130001',
                "courseId": 'COR001'
            },
            "message": "Course in selected Learning Journey not found"
        })
        self.assertEqual(response.status_code, 404)

    def test_remove_existing_course(self):
        lj_obj = LearningJourney("EN001-130001","EN001",'130001','Progress')
        lj_course = Course('COR001',
                            'Systems Thinking and Design',
                            'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,',
                            'Active','Internal','Core')
        db.session.add(lj_obj)
        db.session.add(lj_course)
        lj_courses = LearningJourney_SelectedCourse.insert(Journey_ID='EN001-130001', Course_ID='COR001')
        db.session.commit()

        response = self.client.delete("/journey/EN001-130001/COR001")
        self.assertEqual(response.json, {
                                        "code": 200,
                                        "message": "Delete success"
                                    })
        self.assertEqual(response.status_code, 200)

    


if __name__ == '__main__':
    unittest.main()