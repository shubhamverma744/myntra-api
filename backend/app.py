import os
from flask import Flask
from flask_cors import CORS
from db.config import engine, Base
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config['ENV'] = os.getenv("FLASK_ENV", "development")
    app.secret_key = os.getenv("APP_SECRET_KEY")

    # Enable CORS for all domains and routes
    CORS(app, resources={r"/*": {"origins": "*"}})


    # Register routes (blueprints)
    register_routes(app)

    # Initialize database tables
    Base.metadata.create_all(bind=engine)

    return app

if __name__ == "__main__":  
    app = create_app()
    app.run(debug=True)




