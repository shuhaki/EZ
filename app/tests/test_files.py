import pytest
from app import create_app
from app.models import mongo

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
    
    with app.test_client() as client:
        with app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.files.delete_many({})
        yield client

def test_ops_upload_valid_file(client):
    # Create ops user
    client.post('/api/login', json={
        'email': 'ops@test.com',
        'password': 'password'
    })
    
    # Upload file
    response = client.post(
        '/api/ops/upload',
        data={'file': (io.BytesIO(b"test"), 'report.pptx')},
        content_type='multipart/form-data'
    )
    assert response.status_code == 201