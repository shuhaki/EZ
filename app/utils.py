from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import json

def generate_download_token(user_id, file_id, expiration_minutes=5):
    payload = {
        'user_id': user_id,
        'file_id': file_id,
        'exp': (datetime.utcnow() + timedelta(minutes=expiration_minutes)).isoformat()
    }
    cipher_suite = Fernet(current_app.config['FERNET_KEY'])
    return cipher_suite.encrypt(json.dumps(payload).encode()).decode()

def decrypt_download_token(token):
    cipher_suite = Fernet(current_app.config['FERNET_KEY'])
    try:
        payload = json.loads(cipher_suite.decrypt(token.encode()).decode())
        return payload
    except:
        return None