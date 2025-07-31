import os
from flask import Flask
from db.config import engine, Base
from models import *  # Make sure models/__init__.py imports everything
from routes import register_routes  # New route registration method

def create_app():
    app = Flask(__name__)
    app.config['ENV'] = os.getenv("FLASK_ENV", "development")
    app.secret_key = os.getenv("APP_SECRET_KEY")

    # Register routes (blueprints)
    register_routes(app)

    # Initialize database tables
    Base.metadata.create_all(bind=engine)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


