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

class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(), nullable=True)

    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
    
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

@app.route('/')
def hello_world():

    return 'Hello, World!'

@app.route('/test')
def test():
    courselist = Course.query.all()

    return 'Testing! Course table row count: ' + str(len(courselist))