from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = '12345678nbvfd'
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register routes (Blueprints)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
