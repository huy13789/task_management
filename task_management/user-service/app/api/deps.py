# user-service/app/api/deps.py

from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

# Import cấu hình và models
from ..core.config import settings
from ..db import get_db
from ..models.user import User

# Import hàm decode từ file jwt mới
from ..auth.jwt import decode_access_token 

# 1. Cấu hình
security = HTTPBearer()
SessionDep = Annotated[Session, Depends(get_db)]

# 2. Dependency: Lấy User hiện tại
async def get_current_user(
    token_obj: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    db: SessionDep
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Lấy chuỗi token
    token = token_obj.credentials 
    
    # Dùng hàm decode đã tách ra file jwt.py
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    # Truy vấn DB
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user

# Type Alias (Để dùng trong Router và RoleChecker)
CurrentUser = Annotated[User, Depends(get_current_user)]

# 3. Class: Kiểm tra quyền (Role Checker)
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    # Dùng CurrentUser ở đây cho gọn
    def __call__(self, user: CurrentUser): 
        if getattr(user, "role", None) not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return user