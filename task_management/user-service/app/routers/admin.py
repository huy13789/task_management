from fastapi import APIRouter, Depends
from typing import List

from ..schemas.user import UserResponse
from ..api.deps import SessionDep, AdminOnly
from ..services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"], dependencies=[Depends(AdminOnly)])

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: SessionDep, skip: int = 0, limit: int = 100, ):
    return AdminService(db).get_all_users(skip=skip, limit=limit)

@router.get("/users/info/{user_id}", response_model=UserResponse)
def get_user_by_id(db: SessionDep, user_id: int):
    return AdminService(db).get_user_by_id(user_id)

@router.get("/users/search", response_model=List[UserResponse])
def search_users(db: SessionDep, keyword: str, skip: int = 0, limit: int = 100):
    return AdminService(db).search_users(keyword=keyword, skip=skip, limit=limit)

@router.delete("/users/{user_id}")
def delete_user_by_id(db: SessionDep, user_id: int):
    AdminService(db).delete_user_by_admin(user_id)
    return {"message": "User deleted by admin"}


