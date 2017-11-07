import sqlite3
from flask_restful import Resource, reqparse
from models.game import GameModel

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
            return game.json()

        return {'message': 'Game with that ID not found'}

    def post(self):
        data = Game.parser.parse_args()

        game = GameModel(data['name'])

        game.save_to_db()

        return game.json()

    def delete(self, id):
        game = GameModel.find_by_id(id)

        if game:
            game.delete_from_db()
            return {'message': 'Game deleted!'}

        return {'message': 'Game with that ID not found.'}
