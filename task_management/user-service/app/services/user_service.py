# user-service/app/services/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..auth.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        # 1. Check trùng email
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # 2. Hash & Tạo object
        hashed_pwd = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_pwd,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        # 3. Lưu DB
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except Exception as e:
            self.db.rollback()
            # Nên dùng logger ở đây thay vì print
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
            
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        try:
            self.db.delete(user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")