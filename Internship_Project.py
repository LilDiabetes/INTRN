from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "monkeh"

db = SQLAlchemy(app)
jwt = JWTManager(app)

resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
}

resource_posts = {
    'id': fields.Integer,
    'account_name': fields.String,
    'amount': fields.Integer,
    'profit': fields.Integer
}

registerParser = reqparse.RequestParser()
registerParser.add_argument("email", type=str, required=True, help="email should be string")
registerParser.add_argument("password", type=str, required=True, help="password should be string")
registerParser.add_argument("username", type=str, help="username should be string")

class UserModel(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class PostModel(db.Model):
    __tablename__ = 'Bank Accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    profit = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.account_name




userParser = reqparse.RequestParser()
userParser.add_argument("username", type=str, help="username should be string")
userParser.add_argument("email", type=str, help="email should be string")

postParser = reqparse.RequestParser()
postParser.add_argument("id", type=int, help="ID must be integer ")
postParser.add_argument("account_name", type=str, help="acc name must be str ")
postParser.add_argument("amount", type=int, help="amount must be integer ")
postParser.add_argument("profit", type=int, help="profit must be integer ")


class Post(Resource):
    @marshal_with(resource_posts)
    def get(self, post_id):
        if post_id == 000:
            return PostModel.query.all()
        args = postParser.parse_args()
        post = PostModel.query.filter_by(id=post_id).first()
        return post

    # @marshal_with(resource_posts)
    def post(self, post_id):
        args = postParser.parse_args()
        post = PostModel(account_name=args["account_name"], amount=args["amount"], profit=args["profit"])
        db.session.add(post)
        db.session.commit()
        return "Account has been inserted"

    # @marshal_with(resource_posts)
    def put(self, post_id):
        args = postParser.parse_args()
        post = PostModel.query.filter_by(id=post_id).first()
        if post is None:
            post = PostModel(account_name=args["account_name"], amount=args["amount"], profit=args["profit"])
        else:
            post.account_name = args["account_name"]
            post.amount = args["amount"]
            post.profit = args["profit"]
        db.session.add(post)
        db.session.commit()
        return "Successfully Withdrawn/Deposited"

    # @marshal_with(resource_posts)
    def delete(self, post_id):
        post = PostModel.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return f"Account with id {post_id} has been deleted"


class Auth(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = UserModel.query.filter_by(email=email).first()
        if user is None or check_password_hash(user.password, password) is False:
            return {"msg": "Wrong username or password"}, 401

        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token)


class Register(Resource):
    def post(self):
        args = registerParser.parse_args()
        user = UserModel(username=args['username'], email=args['email'],password=generate_password_hash(args["password"]))
        db.session.add(user)
        db.session.commit()
        return {"msg": "Account was succesfully created"}, 201


class User(Resource):
    @marshal_with(resource_fields)
    @jwt_required()
    def get(self, user_id):
        if user_id == 000:
            return UserModel.query.all()
        user = UserModel.query.filter_by(id=user_id).first()
        return user

    # @marshal_with(resource_fields)
    @jwt_required()
    def post(self, user_id):
        args = userParser.parse_args()
        # password = generate_password_hash(args["password"])
        user = UserModel(email=args["email"], password=args["password"])
        db.session.add(user)
        db.session.commit()
        return "new user added"

    def put(self, user_id):
        args = userParser.parse_args()

        user = UserModel.query.filter_by(id=user_id).first()
        if user is None:
            user = UserModel(username=args["username"], email=args["email"])
        else:
            user.username = args["username"]
            user.email = args["email"]

        db.session.add(user)
        db.session.commit()
        return "user edited"

    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()

        db.session.delete(user)
        db.session.commit()

        return f"Deleted user with id {user_id}"


api.add_resource(User, '/user/<int:user_id>')
api.add_resource(Post, '/post/<int:post_id>')
api.add_resource(Auth, '/login')
api.add_resource(Register, '/register')

if __name__ == '__Internship Project__':
    app.run(debug=True)


