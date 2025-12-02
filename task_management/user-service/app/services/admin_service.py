# user-service/app/services/admin_service.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from ..models.user import User

class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).filter(User.role == "user").offset(skip).limit(limit).all()

    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def delete_user_by_admin(self, user_id: int):
        user = self.get_user_by_id(user_id) 
        try:
            self.db.delete(user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete: {str(e)}")
        
    def search_users(self, keyword: str, skip: int = 0, limit: int = 100):
        search_pattern = f"%{keyword}%"
        
        users = self.db.query(User).filter(
            or_(
                User.email.ilike(search_pattern),      # Tìm trong Email
                User.first_name.ilike(search_pattern), # Tìm trong Tên
                User.last_name.ilike(search_pattern)   # Tìm trong Họ
            )
        ).offset(skip).limit(limit).all()
        
        return users