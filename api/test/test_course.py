# import unittest

# from app import app
# from Courses import Course
# import json

# class TestCourse(unittest.TestCase):
#     def test_course_json(self):
#         course = Course(
#                         'COR001',
#                         'Systems Thinking and Design',
#                         'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking', 
#                         'Active', 
#                         'Internal', 
#                         'Core')
#         self.assertEqual(
#             course.json(),
#             {
#                 "Course_ID": "COR001", 
#                 "Course_Name": "Systems Thinking and Design", 
#                 "Course_Desc": "This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
#                 "Course_Status": "Active",
#                 "Course_Type": "Internal",
#                 "Course_Category": "Core"
#             }
#         )

# if __name__ == '__main__':
#     unittest.main()