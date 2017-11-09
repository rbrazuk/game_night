from datetime import datetime
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


class GroupEvent(Resource):
    def get(self, event_id):
        return EventModel.find_by_id(event_id).json()

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

    def put(self, event_id):
        data = Event.parser.parse_args()

        event = EventModel.find_by_id(event_id)

        if event is None:
            event = EventModel(
                data['name'],
                data['description'],
                data['location'],
                data['date_time'],
                data['is_private'],
                group_id
            )
        else:
            event.name = data['name']
            event.description = data['description']
            event.location = data['location']
            event.date_time = datetime.strptime(data['date_time'], '%Y/%m/%d %H:%M')
            event.is_private = data['is_private']

        event.save_to_db()

        return event.json()

    def delete(self, event_id):
        event = EventModel.find_by_id(event_id)

        if event:
            event.delete_from_db()
            return {'message': 'Event deleted!'}

        return {'message': 'Event with that ID not found.'}


class GroupEventList(Resource):
    def get(self, group_id):
        return {'events': [event.json() for event in EventModel.query.filter_by(group_id=group_id)]}
