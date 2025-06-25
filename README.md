# POSTMAN 
## API Testing
Import the [Postman Collection](https://schema.postman.com/json/collection/v2.1.0/collection.json) to test all endpoints.

# Secure File Sharing System

A REST API for secure file sharing between Ops Users (upload) and Client Users (download), built with Flask and MongoDB.

## Features

- **Role-based access control**:
  - Ops Users: Upload files (PPTX, DOCX, XLSX only)
  - Client Users: Sign up, verify email, download files
- **Security**:
  - JWT authentication
  - Encrypted download URLs
  - File type validation
- **Email verification** for client users

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB (with GridFS for file storage)
- **Authentication**: JWT
- **Security**: Fernet encryption for download URLs

## API Endpoints

### Ops User
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/login` | POST | Ops user login |
| `/api/ops/upload` | POST | Upload files (PPTX/DOCX/XLSX) |

### Client User
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/client/signup` | POST | Client registration |
| `/api/client/verify` | POST | Email verification |
| `/api/client/files` | GET | List all available files |
| `/api/client/download/<file_id>` | POST | Generate secure download URL |

### Common
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/download/<token>` | GET | Download file via encrypted URL |

## Setup Instructions

### Prerequisites
- Python 3.9+
- MongoDB
- Pipenv (recommended)

1.Running the Application

python run.py
The API will be available at http://localhost:5000

2. Project Structure
   secure-file-share/
├── app/                  # Application code
│   ├── __init__.py       # Flask app factory
│   ├── auth.py           # Authentication utils
│   ├── file_handler.py   # File operations
│   ├── models.py         # Database models
│   ├── routes.py         # API endpoints
│   └── utils.py          # Helper functions
├── tests/                # Test cases
├── postman/              # Postman collection
├── init_db.py            # Database initialization
├── create_ops_user.py    # Ops user creation
├── run.py                # Application entry point
├── config.py             # Configuration
├── .env                  # Environment variables
└── requirements.txt      # Dependencies
