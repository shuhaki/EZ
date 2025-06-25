from flask import current_app
from gridfs import GridFS
from .models import mongo
from werkzeug.utils import secure_filename

def save_file(file):
    fs = GridFS(mongo.db)
    filename = secure_filename(file.filename)
    file_id = fs.put(file, filename=filename)
    return file_id

def get_file(gridfs_id):
    fs = GridFS(mongo.db)
    return fs.get(gridfs_id)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']