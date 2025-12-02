# user-service/app/services/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from loguru import logger # Import logger
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..auth.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:

        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_pwd = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_pwd,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            logger.info(f"Created user: {new_user.email}")
            return new_user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user {user_data.email}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            password = update_data.pop("password")
            user.hashed_password = get_password_hash(password)

        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        try:
            self.db.delete(user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")