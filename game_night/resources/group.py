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

        if GroupModel.find_by_name(data['name']):
            return {'message': 'Group with that name already exists.'}

        group = GroupModel(data['name'], data['description'])

        group.save_to_db()

        return {'message': "Group '{}' created successfully.".format(data['name'])}, 201

class GroupList(Resource):
    def get(self):
        return {'groups': [group.json() for group in GroupModel.query.all()]}
