from datetime import datetime, timedelta
from jwt import encode as jwt_encode
from config import SECRET_KEY


def generate_token(user):
    """Generate a JWT token for a user."""
    token_payload = {
        'user_id': str(user['_id']),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt_encode(token_payload, SECRET_KEY, algorithm='HS256')
    return token
