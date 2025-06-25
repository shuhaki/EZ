from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, File
from .auth import authenticate_user, create_jwt_token
from .file_handler import save_file, get_file, allowed_file
from .email_service import generate_verification_token, send_verification_email, verify_token
from .utils import generate_download_token, decrypt_download_token
from bson import ObjectId

bp = Blueprint('api', __name__)

# Common login
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if user['role'] == 'client' and not user['is_verified']:
        return jsonify({"error": "Email not verified"}), 403
    
    token = create_jwt_token(user)
    return jsonify(access_token=token), 200

# Ops User - File Upload
@bp.route('/ops/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()
    if current_user['role'] != 'ops':
        return jsonify({"error": "Unauthorized"}), 403
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        file_id = save_file(file)
        File.create(
            filename=file.filename,
            file_type=file.filename.rsplit('.', 1)[1].lower(),
            uploaded_by=current_user['id'],
            gridfs_id=file_id
        )
        return jsonify({"message": "File uploaded successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Client User - Signup
@bp.route('/client/signup', methods=['POST'])
def client_signup():
    data = request.get_json()
    if User.find_by_email(data['email']):
        return jsonify({"error": "Email already exists"}), 400
    
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    result = User.create(data['email'], hashed_pw.decode('utf-8'), 'client')
    
    token = generate_verification_token(result.inserted_id)
    send_verification_email(data['email'], token)
    
    return jsonify({
        "message": "Verification email sent",
        "verification_url": f"/verify-email?token={token}"  # For demo only
    }), 201

# Client User - Email Verification
@bp.route('/client/verify', methods=['POST'])
def verify_email():
    token = request.json.get('token')
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 400
    
    if User.verify_user(user_id):
        return jsonify({"message": "Email verified successfully"}), 200
    return jsonify({"error": "Verification failed"}), 400

# Client User - List Files
@bp.route('/client/files', methods=['GET'])
@jwt_required()
def list_files():
    current_user = get_jwt_identity()
    if current_user['role'] != 'client' or not current_user['is_verified']:
        return jsonify({"error": "Unauthorized"}), 403
    
    files = File.get_all()
    for file in files:
        file['_id'] = str(file['_id'])
        file['uploaded_by'] = str(file['uploaded_by'])
    
    return jsonify(files), 200

# Client User - Generate Download URL
@bp.route('/client/download/<file_id>', methods=['POST'])
@jwt_required()
def generate_download(file_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'client' or not current_user['is_verified']:
        return jsonify({"error": "Unauthorized"}), 403
    
    if not File.get_by_id(file_id):
        return jsonify({"error": "File not found"}), 404
    
    token = generate_download_token(current_user['id'], file_id)
    return jsonify({
        "download-link": f"/download/{token}",
        "message": "success"
    }), 200

# Secure File Download
@bp.route('/download/<token>', methods=['GET'])
@jwt_required()
def download_file(token):
    current_user = get_jwt_identity()
    payload = decrypt_download_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 400
    
    if datetime.utcnow() > datetime.fromisoformat(payload['exp']):
        return jsonify({"error": "Link expired"}), 410
    
    if current_user['id'] != payload['user_id']:
        return jsonify({"error": "Unauthorized access"}), 403
    
    file_meta = File.get_by_id(payload['file_id'])
    if not file_meta:
        return jsonify({"error": "File not found"}), 404
    
    file = get_file(file_meta['gridfs_id'])
    return send_file(
        io.BytesIO(file.read()),
        as_attachment=True,
        download_name=file_meta['filename']
    )