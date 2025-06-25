from app import create_app
from app.models import mongo
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create application instance
app = create_app()

with app.app_context():
    # Get MongoDB URI from environment
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/file_share')
    
    # Initialize PyMongo
    mongo.init_app(app, uri=mongo_uri)
    
    # Create collections if they don't exist
    collections = mongo.db.list_collection_names()
    
    if 'users' not in collections:
        mongo.db.create_collection('users')
        print("Created 'users' collection")
    
    if 'files' not in collections:
        mongo.db.create_collection('files')
        print("Created 'files' collection")
    
    # Create indexes
    mongo.db.users.create_index('email', unique=True)
    
    print("Database initialization complete")