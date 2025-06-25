import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    FERNET_KEY = os.getenv('FERNET_KEY')
    VERIFICATION_SECRET = os.getenv('VERIFICATION_SECRET')
    ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}