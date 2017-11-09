from flask_restful import Resource, reqparse
from models.event import EventModel

class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name field cannot be blank"
    )
    parser.add_argument(
        'description',
        type=str
    )
    parser.add_argument(
        'location',
        type=str,
        required=True,
        help="Location field cannot be blank"
    )
    parser.add_argument(
        'date_time',
        type=str,
        required=True,
        help="date_time field cannot be blank"
    )
    parser.add_argument(
        'is_private',
        type=bool,
        required=True,
        help="is_private field cannot be blank"
    )

    def post(self):
        data = Event.parser.parse_args()

        event = EventModel(data['name'], data['description'], data['location'], data['date_time'], data['is_private'])

        event.save_to_db()

        return event.json()

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class GroupEvent(Resource):
    def post(self, group_id):
        data = Event.parser.parse_args()

        event = EventModel(
            data['name'],
            data['description'],
            data['location'],
            data['date_time'],
            data['is_private'],
            group_id
            )

        event.save_to_db()

        return event.json()
