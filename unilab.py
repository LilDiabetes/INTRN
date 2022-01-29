from flask import Flask
from flask_restful import Resource, Api
# import sqlite3
from flask_sqlalchemy import SQLAlchemy

db_name = 'mydb.sqlite'
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
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

    def __repr__(self):
        return f'<Student {self.name} - {self.email}>'



class StudentsR(Resource):
    def get(self, student_id):
        fltr = Students.query.filter_by(id=student_id).first()
        return f"Student '{fltr.name} - {fltr.email}' "

    def post(self, name, age):
        email = f"{name}{age}@{name}.com"
        fltr = Students(name, email, age)
        db.session.add(fltr)
        db.session.commit()
        return f"Student '{name} - {email}' was added to database"

    def put(self,student_id, name, age):
        fltr = Students.query.filter_by(id=student_id).first()
        fltr.name = name
        fltr.age = age
        db.session.add(fltr)
        db.session.commit()
        return f"Student '{name}' was modified to database"

    def delete(self, student_id):
        fltr = Students.query.filter_by(id=student_id).first()
        db.session.delete(fltr)
        db.session.commit()
        return f"Student '{fltr.name}' was deleted from database"


api.add_resource(StudentsR, '/read/<int:student_id>', endpoint="get")
api.add_resource(StudentsR, '/create/<string:name>/<int:age>', endpoint="post")
api.add_resource(StudentsR, '/edit/<int:student_id>/<string:name>/<int:age>', endpoint="put")
api.add_resource(StudentsR, '/remove/<int:student_id>', endpoint="delete")

#
if __name__ == '__unilab__':
    app.run(debug=True)




# db.create_all()

# entry = Students('Baron', 'barontrump@yahoo.com', 18)
# db.session.add(entry)
# db.session.commit()
# print(entry)

# fltr = Students.query.filter_by(name='Baron').first()
# fltr.age = 12
# db.session.add(fltr)
# db.session.commit()
# print(fltr)

# db.session.delete(fltr)
# db.session.commit()

# con = sqlite3.connect('mydb.sqlite', check_same_thread=False)
# cur = con.cursor()

# con = sqlite3.connect("")
# cur = con.cursor()
#
# for s in [(7, 'grapefruit', 7, 2), (8, 'apricot', 3, 8)]:
#     cur.execute("""INSERT INTO grocery_list (id, name, price, quantity)
#         values (?, ?, ?, ?)""", (s[0], s[1], s[2], s[3]))
#     con.commit()

# from flask import Flask
# from flask_restful import Resource, Api
# import sqlite3
# from flask_sqlalchemy import SQLAlchemy
#
# con = sqlite3.connect("")
# cur = con.cursor()
#
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)
#
#
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     age = db.Column(db.)
#
#
# class Students(Resource):
#     def get(self, student_id):
#         print(type(student_id))
#         cur.execute("SELECT * FROM students where id = ?", student_id)
#         print(cur.fetchall())
#         return "fetched"
#
#
# def __repr__(self):
#     return '<User %r>' % self.username
#
#
# api.add_resource(Students, '/', '/read/<int:student_id>')
#
# if __name__ == '__app__':
#     app.run(debug=True)
