
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.user import User
from ..core.security import verify_password, create_access_token
from ..schemas.user import TokenResponse, UserLogin

router = APIRouter(tags=["Authentication"])

@router.post("/auth/login", response_model=TokenResponse)
def login_for_access_token(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    # 1. Tìm user trong DB bằng EMAIL (lấy từ JSON)
    user = db.query(User).filter(User.email == login_data.email).first()
    
    # 2. Kiểm tra user và mật khẩu
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Tạo Token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token
    }
