# user-service/app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt 
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from .config import settings
from ..db import get_db
from ..models.user import User

# --- 1. CẤU HÌNH ---
password_hash = PasswordHash.recommended()

# Định nghĩa nơi lấy token.
security = HTTPBearer()

# --- 2. CÁC HÀM TIỆN ÍCH CŨ (Giữ nguyên) ---
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# --- 3. HÀM MỚI: Dependency lấy User hiện tại ---
async def get_current_user(
    # Thay đổi dependency ở đây: dùng 'security' thay vì 'oauth2_scheme'
    token_obj: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Lấy chuỗi token từ object credentials (Bearer <token>)
    token = token_obj.credentials 
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user