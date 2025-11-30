# user-service/app/schemas/user.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Schema Cơ bản (Base)
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# Schema Tạo Người dùng (Input)
class UserCreate(UserBase):
    password: str

# Schema Đăng nhập (Input)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema Phản hồi (Output)
# Đây là cấu trúc dữ liệu trả về cho client (KHÔNG BAO GỒM MẬT KHẨU)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True 

# Schema Phản hồi Token (Output)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"