from db import db

class GroupModel(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))

    #members = db.relationship('UserModel', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def json(self):
        return {'name': self.name, 'description': self.description}
