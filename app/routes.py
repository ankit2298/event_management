from flask import Blueprint, request, jsonify
from app.schemas import validate_event, validate_attendee
from app.services import create_event, get_upcoming_events, register_attendee, get_attendees

event_routes = Blueprint('event_routes', __name__)


@event_routes.route('/events', methods=['POST'])
def create_event_route():
    """
    Create a new event
    ---
    tags:
      - Events
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              location:
                type: string
              start_time:
                type: string
                format: date-time
              end_time:
                type: string
                format: date-time
              max_capacity:
                type: integer
    responses:
      201:
        description: Event created successfully
    """
    data = request.get_json()
    msg, ok = validate_event(data)
    if not ok:
        return jsonify({"error": msg}), 400
    result = create_event(data)
    return jsonify(result), 201


@event_routes.route('/events', methods=['GET'])
def list_events():
    """
    List all upcoming events
    ---
    tags:
      - Events
    responses:
      200:
        description: List of events
    """
    return jsonify(get_upcoming_events())


@event_routes.route('/events/<int:event_id>/register', methods=['POST'])
def register_attendee_route(event_id):
    """
    Register an attendee to an event
    ---
    tags:
      - Attendees
    parameters:
      - in: path
        name: event_id
        schema:
          type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
    responses:
      201:
        description: Attendee registered successfully
    """
    data = request.get_json()
    msg, ok = validate_attendee(data)
    if not ok:
        return jsonify({"error": msg}), 400
    result, status = register_attendee(event_id, data)
    return jsonify(result), status


@event_routes.route('/events/<int:event_id>/attendees', methods=['GET'])
def get_attendees_route(event_id):
    """
    Get attendees for an event
    ---
    tags:
      - Attendees
    parameters:
      - in: path
        name: event_id
        schema:
          type: integer
        required: true
      - in: query
        name: page
        schema:
          type: integer
        required: false
        description: Page number (default=1)
      - in: query
        name: limit
        schema:
          type: integer
        required: false
        description: Number of results per page (default=10)
    responses:
      200:
        description: List of attendees with pagination
    """
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    result = get_attendees(event_id, page, limit)
    return jsonify(result)
