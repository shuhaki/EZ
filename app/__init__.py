from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from .models import mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    mongo.init_app(app)
    
    # Import and register blueprints
    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app