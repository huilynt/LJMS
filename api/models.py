from app import db

class Role(db.Model):
    __tablename__ = "role"
    Role_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(20), nullable=False)

    staff = db.relationship("Staff", backref="role", lazy=True)

    def __init__(self, Role_ID, Role_Name):
        self.Role_ID = Role_ID
        self.Role_Name = Role_Name

    def json(self):
        return {
            "Role_ID": self.Role_ID, 
            "Role_Name": self.Role_Name
        }


class Course(db.Model):
    __tablename__ = "course"

    Course_ID = db.Column(db.String(20), primary_key=True)
    Course_Name = db.Column(db.String(50), nullable=False)
    Course_Desc = db.Column(db.String(255), nullable=True)
    Course_Status = db.Column(db.String(15), nullable=True)
    Course_Type = db.Column(db.String(10), nullable=True)
    Course_Category = db.Column(db.String(50), nullable=True)

    registrations = db.relationship("Registration", backref="course", lazy=True)

    def __init__(self, Course_ID, Course_Name, Course_Desc, Course_Status, Course_Type, Course_Category):
        self.Course_ID = Course_ID
        self.Course_Name = Course_Name
        self.Course_Desc = Course_Desc
        self.Course_Status = Course_Status
        self.Course_Type = Course_Type
        self.Course_Category = Course_Category

    def json(self):
        return {
            "Course_ID": self.Course_ID, 
            "Course_Name": self.Course_Name, 
            "Course_Desc": self.Course_Desc,
            "Course_Status": self.Course_Status,
            "Course_Type": self.Course_Type,
            "Course_Category": self.Course_Category,
        }


class Staff(db.Model):
    __tablename__ = "staff"

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Role = db.Column(db.Integer, db.ForeignKey(Role.Role_ID), nullable=False)

    registrations = db.relationship("Registration", backref="staff", lazy=True)

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Dept, Email, Role):
        self.Staff_ID = Staff_ID
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Dept = Dept
        self.Email = Email
        self.Role = Role

    def json(self):
        return {
            "Staff_ID": self.Staff_ID, 
            "Staff_FName": self.Staff_FName, 
            "Staff_LName": self.Staff_LName,
            "Dept": self.Dept,
            "Email": self.Email,
            "Role": self.Role,
        }


class Registration(db.Model):
    __tablename__ = "registration"

    Reg_ID = db.Column(db.Integer, primary_key=True)
    Course_ID = db.Column(db.String(20), db.ForeignKey(Course.Course_ID), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey(Staff.Staff_ID), nullable=False)
    Reg_Status = db.Column(db.String(20), nullable=False)
    Completion_Status = db.Column(db.String(20))

    def __init__(self, Reg_ID, Course_ID, Staff_ID, Reg_Status, Completion_Status, Role):
        self.Reg_ID = Reg_ID
        self.Course_ID = Course_ID
        self.Staff_ID = Staff_ID
        self.Reg_Status = Reg_Status
        self.Completion_Status = Completion_Status

    def json(self):
        return {
            "Reg_ID": self.Reg_ID, 
            "Course_ID": self.Course_ID, 
            "Staff_ID": self.Staff_ID,
            "Reg_Status": self.Reg_Status,
            "Completion_Status": self.Completion_Status
        }

Jobrole_skill = db.Table('jobrole_skill',
                        db.Column('JobRole_ID', db.String(20), db.ForeignKey('jobrole.JobRole_ID')),
                        db.Column('Skill_ID', db.String(20), db.ForeignKey('skill.Skill_ID'))
)

Skill_course = db.Table('skill_course',
                        db.Column('Skill_ID', db.String(20), db.ForeignKey('skill.Skill_ID')),
                        db.Column('Course_ID', db.String(20), db.ForeignKey('course.Course_ID'))
)

class Skill(db.Model):
    __tablename__ = "skill"

    Skill_ID = db.Column(db.String(20), primary_key=True)
    Skill_Name = db.Column(db.String(50), nullable=False)
    Skill_Desc = db.Column(db.String(150))
    Skill_Status = db.Column(db.String(20))

    courses = db.relationship(Course, secondary=Skill_course, backref="skill", lazy=True)

    def __init__(self, Skill_ID, Skill_Name, Skill_Desc="", Skill_Status=""):
        self.Skill_ID = Skill_ID
        self.Skill_Name = Skill_Name
        self.Skill_Desc = Skill_Desc
        self.Skill_Status = Skill_Status

    def json(self):
        return {
            "Skill_ID": self.Skill_ID,
            "Skill_Name": self.Skill_Name,
            "Skill_Desc": self.Skill_Desc,
            "Skill_Status": self.Skill_Status
        }


class JobRole(db.Model):
    __tablename__ = "jobrole"

    JobRole_ID = db.Column(db.String(20), primary_key=True)
    JobRole_Name = db.Column(db.String(50), nullable=False)
    JobRole_Desc = db.Column(db.String(150))
    JobRole_Status = db.Column(db.String(20))

    skills = db.relationship(Skill, secondary=Jobrole_skill, backref="jobroles", lazy=True)

    def __init__(self, JobRole_ID, JobRole_Name, JobRole_Desc="", JobRole_Status=""):
        self.JobRole_ID = JobRole_ID
        self.JobRole_Name = JobRole_Name
        self.JobRole_Desc = JobRole_Desc
        self.JobRole_Status = JobRole_Status

    def json(self):
        return {
            "JobRole_ID": self.JobRole_ID,
            "JobRole_Name": self.JobRole_Name,
            "JobRole_Desc": self.JobRole_Desc,
            "JobRole_Status": self.JobRole_Status
        }

# Learning Journey
LearningJourney_SelectedCourse = db.Table("learningjourney_selectedcourse",
                        db.Column('Journey_ID', db.String(20), db.ForeignKey("learningjourney.Journey_ID")),
                        db.Column('Course_ID', db.String(20), db.ForeignKey(Course.Course_ID)),
)

class LearningJourney(db.Model):
    __tablename__ = "learningjourney"

    Journey_ID = db.Column(db.String(20), primary_key=True)
    JobRole_ID = db.Column(db.String(20), db.ForeignKey(JobRole.JobRole_ID), nullable=False)
    Staff_ID = db.Column(db.String(20), db.ForeignKey(Staff.Staff_ID), nullable=False)
    LearningJourney_Status = db.Column(db.String(20))

    courses = db.relationship(Course, secondary=LearningJourney_SelectedCourse, backref="learningjourneys", lazy=True)

    def __init__(self, Journey_ID, JobRole_ID, Staff_ID, LearningJourney_Status="Progress"):
        self.Journey_ID = Journey_ID
        self.JobRole_ID = JobRole_ID
        self.Staff_ID = Staff_ID
        self.LearningJourney_Status = LearningJourney_Status

    def json(self):
        return {
            "Journey_ID": self.Journey_ID,
            "JobRole_ID": self.JobRole_ID,
            "Staff_ID": self.Staff_ID,
            "LearningJourney_Status": self.LearningJourney_Status
        }
