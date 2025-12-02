# app/db/init_db.py

from sqlalchemy.orm import Session
from ..core.config import settings
from ..auth.security import get_password_hash
from ..models.user import User
from ..schemas.user import UserCreate # Hoặc dùng model trực tiếp

def init_db(db: Session) -> None:
    # 1. Kiểm tra xem Admin đã tồn tại chưa
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    
    if not user:
        print(f"Creating superuser: {settings.FIRST_SUPERUSER}")
        
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            first_name="Super",
            last_name="Admin",
            is_active=True,
            role="admin"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Superuser created successfully!")
    else:
        print("Superuser already exists. Skipping creation.")