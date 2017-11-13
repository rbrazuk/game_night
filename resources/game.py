import sqlite3
from flask_restful import Resource, reqparse
from models.game import GameModel
from models.user import UserModel

class Game(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name field cannot be blank"
    )

    def get(self, id):
        game = GameModel.find_by_id(id)

        if game:
            return game.json(), 200

        return {'message': 'Game with that ID not found'}, 404

    def post(self, user_id):
        data = Game.parser.parse_args()

        game = GameModel(data['name'])
        user = UserModel.find_by_id(user_id)

        game.save_to_db()

        user.save_game_to_collection(game)

        return game.json(), 201

    def delete(self, user_id, game_id):
        game = GameModel.find_by_id(game_id)
        user = UserModel.find_by_id(user_id)

        if game and user:
            user.remove_game_from_collection(game)
            return {'message': 'Game removed from collection!'}, 200

        return {'message': 'Game with that ID not found.'}, 404
