from flask import Flask
from flask_restful import Resource, Api
# import sqlite3
from flask_sqlalchemy import SQLAlchemy

# con = sqlite3.connect("students.sqlite", check_same_thread=False)
# cur = con.cursor()

db_name = 'students.sqlite'
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True)
    age = db.Column(db.Integer, nullable=True)

    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def _repr_(self):
        return f'Student {self.name} - {self.age}'


# from student_app import db
# db.create_all()


john = Students('John', 'john@john.com', 35)
db.session.add(john)
db.session.commit()

quit()