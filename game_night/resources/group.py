import sqlite3
from flask_restful import Resource, reqparse
from models.group import GroupModel

class Group(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name field cannot be blank"
    )
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help="Name field cannot be blank"
    )

    def post(self):

        #TODO: check if group with name exists already
        data = Group.parser.parse_args()

        group = GroupModel(data['name'], data['description'])

        return group.json(), 201
