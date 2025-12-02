from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    role = Column(String, default="user")
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        # Index cho tìm kiếm tên: Giúp query: WHERE first_name LIKE '...' OR last_name LIKE '...'
        Index('idx_user_full_name', 'first_name', 'last_name'),
        # Index cho lọc user active: Giúp query: WHERE is_active = true AND role = 'admin'
        Index('idx_user_active_role', 'is_active', 'role'),
        # Index cho tìm kiếm email nhanh hơn
        Index('idx_user_email', 'email'),
    )