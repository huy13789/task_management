# task-service/app/core/jwt.py

import jwt
from ..core.config import settings

# This function allows deps.py to avoid importing the jwt library directly
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return Exception("Token has expired")
    except jwt.InvalidTokenError:
        return Exception("Invalid token")