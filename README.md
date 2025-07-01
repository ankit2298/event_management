#  Mini Event Management API

A backend system built using **Flask + SQLAlchemy** that allows:

- Creating Events
- Registering Attendees
- Viewing Attendees with Pagination
- Timezone (IST) aware scheduling

---

## 🚀 Tech Stack

- Python 3.8+
- Flask
- SQLAlchemy (ORM)
- SQLite (can easily swap with PostgreSQL)
- Pytz for timezone support

---

## 🧪 Features

- RESTful API endpoints
- Clean Architecture: routes / services / models
- No duplicate attendees per event
- Max capacity restriction
- Pagination on attendee lists
- Timezone-safe datetime handling
- Ready for extension with async, tests, and docs

---


## 🛠️ Setup Instructions

### 1. Clone or Download the Project
```bash
git clone <your-repo-url>
cd event_management_system


2. Create Virtual Environment
python -m venv venv
source venv/bin/activate 


3. Install Dependencies
pip install -r requirements.txt

4.Run the App
python main.py

