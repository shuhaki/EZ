from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_verification_token(user_id):
    serializer = URLSafeTimedSerializer(current_app.config['VERIFICATION_SECRET'])
    return serializer.dumps(str(user_id), salt='email-verify')

def verify_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(current_app.config['VERIFICATION_SECRET'])
    try:
        user_id = serializer.loads(
            token,
            salt='email-verify',
            max_age=expiration
        )
        return user_id
    except:
        return None

# In production: Integrate with SMTP service like SendGrid
def send_verification_email(email, token):
    verification_url = f"https://yourdomain.com/verify-email?token={token}"
    print(f"Verification email sent to {email}: {verification_url}")