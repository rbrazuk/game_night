from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required, current_identity
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
    parser.add_argument(
        'bio',
        type=str
    )
    parser.add_argument(
        'location',
        type=str
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User with that name already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User '{}' created successfully".format(data['username'])}, 201

class User(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found!'}, 404

    def put(self, user_id):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_id(user_id)

        if user is None:
            user = UserModel(**data)
        else:
            user.username = data['username']
            user.email = data['email']
            user.password = data['password']
            user.bio = data['bio']
            user.location = data['location']

        user.save_to_db()

        return user.json(), 200

class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        print(current_identity.id)
        return {'user_id': current_identity.id}
        #return dict(current_identity)
