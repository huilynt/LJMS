from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root@localhost:3306/ljms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


class Role(db.Model):
    __tablename__ = "role"
    Role_ID = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(20), nullable=False)

    Staff = db.relationship('Staff', backref='role', lazy=True)

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

    Registrations = db.relationship("Registrations", backref="course", lazy=True)

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
            "title": self.title, 
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
    Role = db.Column(db.Integer, db.ForeignKey("Role.Role_ID"), nullable=False)

    Registrations = db.relationship("Registrations", backref="staff", lazy=True)

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
    Course_ID = db.Column(db.String(20), db.ForeignKey("Course.Course_ID"), nullable=False)
    Staff_ID = db.Column(db.Integer, db.ForeignKey("Staff.Staff_ID"), nullable=False)
    Reg_Status = db.Column(db.String(20), nullable=False)
    Completion_Status = db.Column(db.String(20), nullable=False)

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

@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/test")
def test():
    courselist = Course.query.all()

    return "Testing! Course table row count: " + str(len(courselist))

# @app.route("/member")
# def member():
#     return {"members": ["M1","M2","M3"]}

# @app.route("/roles")
# def role():
#     rolelist= Role.query.all()
#     return rolelist    

    # Running app
if __name__ == '__main__':
    app.run(debug=True, port=5000)