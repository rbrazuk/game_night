from flask import Flask
from flask_restful import Api

from resources.game import Game
from resources.user import UserRegister, User
from resources.group import Group, GroupList, GroupMember
from resources.event import Event

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(UserRegister, '/register')

api.add_resource(User,'/user/<int:user_id>')

api.add_resource(Group,
    '/group',
    '/group/<int:id>',
    '/group/<int:group_id>/members/<int:user_id>'
    )

api.add_resource(GroupMember, '/groups/<int:group_id>/members/<int:user_id>')

api.add_resource(GroupList, '/groups')

api.add_resource(Game,
    '/game',
    '/game/<int:game_id>',
    '/user/<int:user_id>/collection',
    '/user/<int:user_id>/collection/<int:game_id>'
    )

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
