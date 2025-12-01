import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..core.security import get_password_hash, get_current_user, RoleChecker

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra email
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash mật khẩu
    hashed_pwd = get_password_hash(user.password)
    
    # 3. Tạo User mới
    new_user = User(
        email=user.email,
        hashed_password=hashed_pwd,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()         
        print(f"Error creating user: {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    return new_user

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.patch("/me/update", response_model=UserResponse)
def update_users_me(
        user_update: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Lấy thông tin user hiện tại từ DB
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Chuyển đổi object sang Dictionary
    update_data = user_update.model_dump(exclude_unset=True) # Chỉ lấy những trường thực sự gửi lên

    for key, value in update_data.items():
        setattr(db_user, key, value) # db_user.key = value

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

    return db_user

@router.delete("/")
def delete_user(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == current_user.email).first()

    print(f"user: {user}")

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )

    return {"message": "User deleted"}