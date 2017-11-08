import sqlite3
from flask_restful import Resource, reqparse
from models.group import GroupModel
from models.user import UserModel

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
        help="Description field cannot be blank"
    )

    def get(self, id):
        group = GroupModel.find_by_id(id)

        if group:
            return group.json()

        return {'message': 'Item with that id not found.'}

    def post(self):
        data = Group.parser.parse_args()

        if GroupModel.find_by_name(data['name']):
            return {'message': 'Group with that name already exists.'}

        group = GroupModel(data['name'], data['description'])

        group.save_to_db()

        return {'message': "Group '{}' created successfully.".format(data['name'])}, 201

    def put(self, id):
        data = Group.parser.parse_args()

        group = GroupModel.find_by_id(id)

        group.name = data['name']

        if data['description'] is not None:
            group.description = data['description']

        group.save_to_db()

        return group.json()

    def delete(self, id):
        group = GroupModel.find_by_id(id)

        if group:
            group.delete_from_db()
            return {'message': 'Group deleted!'}
        return {'message': 'Group with that id not found.'}

class GroupList(Resource):
    def get(self):
        return {'groups': [group.json() for group in GroupModel.query.all()]}


class GroupMember(Resource):
    def post(self, group_id, user_id):
        group = GroupModel.find_by_id(group_id)
        user = UserModel.find_by_id(user_id)

        if group:
             if user:
                 group.add_member(user)
             else:
                 return {'message': 'User with that ID not found.'}


        return {'message': 'Group with that ID not found.'}

    def delete(self):
        # Remove a user from a group
        pass
