from db import db
import datetime

class EventModel(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date_time = db.Column(db.DateTime(timezone=False))
    is_private = db.Column(db.Boolean)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    def __init__(self, name, description, location, date_time, is_private):
        self.name = name
        self.description = description
        self.location = location
        self.date_time = date_time
        self.is_private = is_private

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id =_id).first()

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'location': self.location,
                'date_time': self.date_time,
                'is_private': self.is_private
                }
