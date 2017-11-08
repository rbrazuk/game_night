from db import db

group_user = db.Table('group_user',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class GroupModel(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    members = db.relationship('UserModel', secondary=group_user, backref=db.backref('groups'), lazy='dynamic')


    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def add_member(self, user):
        self.members.append(user)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def json(self):
        return {'id': self.id,
            'name': self.name,
             'description': self.description,
             'members': [user.simple_json() for user in self.members.all()]
             }
