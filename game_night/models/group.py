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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


    def json(self):
        return {'id': self.id,'name': self.name, 'description': self.description}
