from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

mongo = PyMongo()

class User:
    @staticmethod
    def create(email, password, role):
        return mongo.db.users.insert_one({
            'email': email,
            'password': password,
            'role': role,
            'is_verified': False if role == 'client' else True,
            'created_at': datetime.utcnow()
        })
    
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def verify_user(user_id):
        return mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'is_verified': True}}
        )

class File:
    @staticmethod
    def create(filename, file_type, uploaded_by, gridfs_id):
        return mongo.db.files.insert_one({
            'filename': filename,
            'file_type': file_type,
            'uploaded_by': ObjectId(uploaded_by),
            'gridfs_id': gridfs_id,
            'uploaded_at': datetime.utcnow()
        })
    
    @staticmethod
    def get_all():
        return list(mongo.db.files.find({}, {'gridfs_id': 0}))
    
    @staticmethod
    def get_by_id(file_id):
        return mongo.db.files.find_one({'_id': ObjectId(file_id)})