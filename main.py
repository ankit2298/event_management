from flask import Flask
from config import Config
from app import db
from app.routes import event_routes
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Swagger(app)

    db.init_app(app)

    from app import models

    with app.app_context():
        db.create_all()

    app.register_blueprint(event_routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
