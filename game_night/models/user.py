from db import db

user_game = db.Table('user_game',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True)
)

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    collection = db.relationship('GameModel', secondary=user_game, backref=db.backref('users'), lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_game_to_collection(self, game):
        game.users.append(self)
        db.session.commit()

    def remove_game_from_collection(self, game):
        game.users.remove(self)
        db.session.commit()

    def json(self):
        return {'username': self.username, 'collection': [game.json() for game in self.collection.all()]}

    def simple_json(self):
        return {'id': self.id, 'username': self.username}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
