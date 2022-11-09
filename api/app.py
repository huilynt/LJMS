from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from Courses import *
from Skills import *
from JobRoles import *
from Staffs import *
from Journey import *

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root@localhost:3306/ljps"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
