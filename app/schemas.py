from datetime import datetime

def validate_event(data):
    required_fields = ['name', 'location', 'start_time', 'end_time', 'max_capacity']
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}", False
    try:
        datetime.fromisoformat(data['start_time'])
        datetime.fromisoformat(data['end_time'])
        if data['max_capacity'] <= 0:
            return "Max capacity must be positive.", False
    except Exception as e:
        return str(e), False
    return "", True

def validate_attendee(data):
    if not data.get("name"):
        return "Attendee name is required", False
    if not data.get("email"):
        return "Attendee email is required", False
    return "", True