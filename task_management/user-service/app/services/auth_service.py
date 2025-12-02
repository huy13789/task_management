# user-service/app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..auth.security import verify_password
from ..auth.jwt import create_access_token
from ..schemas.user import UserLogin, TokenResponse

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login_user(self, login_data: UserLogin) -> TokenResponse:
        # 1. Tìm user
        user = self.db.query(User).filter(User.email == login_data.email).first()
        
        # 2. Verify mật khẩu
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 3. Tạo Token
        access_token = create_access_token(data={"sub": user.email})
        
        return TokenResponse(access_token=access_token, token_type="bearer")