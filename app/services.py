from app.models import Event, Attendee
from app.utils import from_ist
from app import db

def create_event(data):
    event = Event(
        name=data['name'],
        location=data['location'],
        start_time=from_ist(data['start_time']),
        end_time=from_ist(data['end_time']),
        max_capacity=data['max_capacity']
    )
    db.session.add(event)
    db.session.commit()
    return event.to_dict()

def get_upcoming_events():
    events = Event.query.all()
    return [event.to_dict() for event in events]

def register_attendee(event_id, data):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404

    existing = Attendee.query.filter_by(event_id=event_id, email=data['email']).first()
    if existing:
        return {"error": "Attendee already registered"}, 400

    if len(event.attendees) >= event.max_capacity:
        return {"error": "Event is fully booked"}, 400

    attendee = Attendee(name=data['name'], email=data['email'], event_id=event_id)
    db.session.add(attendee)
    db.session.commit()
    return attendee.to_dict(), 201

def get_attendees(event_id, page=1, limit=10):
    attendees = Attendee.query.filter_by(event_id=event_id).paginate(page=page, per_page=limit, error_out=False)
    return {
        "attendees": [a.to_dict() for a in attendees.items],
        "total": attendees.total,
        "page": attendees.page,
        "pages": attendees.pages
    }
