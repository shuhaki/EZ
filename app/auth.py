from flask_jwt_extended import create_access_token
from .models import User
import bcrypt

def authenticate_user(email, password):
    user = User.find_by_email(email)
    if not user:
        return None
    
    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return user
    return None

def create_jwt_token(user):
    return create_access_token(identity={
        'id': str(user['_id']),
        'email': user['email'],
        'role': user['role'],
        'is_verified': user['is_verified']
    })