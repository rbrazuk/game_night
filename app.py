import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.game import Game
from resources.user import UserRegister, User, CurrentUser
from resources.group import Group, GroupList, GroupMember
from resources.event import Event, GroupEvent, GroupEventList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/register')

api.add_resource(CurrentUser, '/current_user')

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

api.add_resource(GroupEvent,
    '/events/<int:event_id>',
    '/groups/<int:group_id>/event/<int:event_id>',
    '/groups/<int:group_id>/event',
    )

api.add_resource(GroupEventList, '/groups/<int:group_id>/events')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
