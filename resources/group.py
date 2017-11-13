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
            return group.json(), 200

        return {'message': 'Item with that id not found.'}, 404

    def post(self):
        data = Group.parser.parse_args()

        if GroupModel.find_by_name(data['name']):
            return {'message': 'Group with that name already exists.'}, 400

        group = GroupModel(data['name'], data['description'])

        group.save_to_db()

        return group.json(), 201

    def put(self, id):
        data = Group.parser.parse_args()

        group = GroupModel.find_by_id(id)

        group.name = data['name']

        if data['description'] is not None:
            group.description = data['description']

        group.save_to_db()

        return group.json(), 200

    def delete(self, id):
        group = GroupModel.find_by_id(id)

        if group:
            group.delete_from_db()
            return {'message': 'Group deleted!'}, 200
        return {'message': 'Group with that id not found.'}, 404

class GroupList(Resource):
    def get(self):
        return {'groups': [group.json() for group in GroupModel.query.all()]}, 200


class GroupMember(Resource):
    def post(self, group_id, user_id):
        group = GroupModel.find_by_id(group_id)
        user = UserModel.find_by_id(user_id)

        if group:
             if user:
                 group.add_member(user)
                 return {'message': "User '{}' added to '{}'".format(user.username, group.name)}, 201
             else:
                 return {'message': 'User with that ID not found.'}, 404

        return {'message': 'Group with that ID not found.'}, 404

    def delete(self, group_id, user_id):
        group = GroupModel.find_by_id(group_id)
        user = UserModel.find_by_id(user_id)

        if group:
            if user:
                group.remove_member(user)
                return {'message': "User '{}' removed from '{}'".format(user.username, group.name)}, 200
            else:
                return {'message': 'User with that ID not found.'}, 404

        return {'message': 'Group with that ID not found.'}, 404
