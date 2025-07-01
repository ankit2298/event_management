import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

def test_create_event(client):
    response = client.post('/events', json={
        "name": "Test Event",
        "location": "Mumbai",
        "start_time": "2025-07-10T10:00:00",
        "end_time": "2025-07-10T12:00:00",
        "max_capacity": 2
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Event"

def test_register_attendee(client):
    client.post('/events', json={
        "name": "Test",
        "location": "Delhi",
        "start_time": "2025-07-11T10:00:00",
        "end_time": "2025-07-11T12:00:00",
        "max_capacity": 5
    })

    response = client.post('/events/1/register', json={
        "name": "Ankit",
        "email": "ankit_unique_test@example.com"
    })

    print("REGISTER RESPONSE:", response.status_code, response.get_json())

    assert response.status_code == 201

def test_prevent_duplicate_registration(client):
    client.post('/events', json={
        "name": "Dup Test",
        "location": "Bangalore",
        "start_time": "2025-07-12T10:00:00",
        "end_time": "2025-07-12T12:00:00",
        "max_capacity": 5  # ✅ increase capacity to prevent full booking
    })

    # First registration
    client.post('/events/1/register', json={
        "name": "Ankit",
        "email": "ankit@example.com"
    })

    # Duplicate registration
    response = client.post('/events/1/register', json={
        "name": "Ankit",
        "email": "ankit@example.com"
    })

    assert response.status_code == 400
    assert "already registered" in response.get_json().get("error", "")


def test_prevent_overbooking(client):
    client.post('/events', json={
        "name": "Capacity Test",
        "location": "Chennai",
        "start_time": "2025-07-13T10:00:00",
        "end_time": "2025-07-13T12:00:00",
        "max_capacity": 1
    })

    client.post('/events/1/register', json={
        "name": "First",
        "email": "first@example.com"
    })

    response = client.post('/events/1/register', json={
        "name": "Second",
        "email": "second@example.com"
    })

    assert response.status_code == 400
    assert "fully booked" in response.get_json().get("error", "")

def test_get_attendees_with_pagination(client):
    client.post('/events', json={
        "name": "Pagination Test",
        "location": "Hyd",
        "start_time": "2025-07-14T10:00:00",
        "end_time": "2025-07-14T12:00:00",
        "max_capacity": 3
    })

    client.post('/events/1/register', json={"name": "A", "email": "a@test.com"})
    client.post('/events/1/register', json={"name": "B", "email": "b@test.com"})
    client.post('/events/1/register', json={"name": "C", "email": "c@test.com"})

    response = client.get('/events/1/attendees?page=1&limit=2')
    assert response.status_code == 200
    data = response.get_json()
    assert "attendees" in data
    assert len(data["attendees"]) == 2
