import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Username field cannot be blank"
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email field cannot be blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password field cannot be blank"
    )

    def post(self):
        return {'message': "User created successfully"}, 201
