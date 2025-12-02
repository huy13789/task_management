# user-service/app/routers/users.py

from fastapi import APIRouter, status
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..api.deps import SessionDep, CurrentUser
from ..services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users Dashboard"])

@router.post("/", response_model=UserResponse)
def sign_up(user_data: UserCreate, db: SessionDep):
    return UserService(db).create_user(user_data)

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def get_me(current_user: CurrentUser):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_account_me(
    user_update: UserUpdate, 
    current_user: CurrentUser, 
    db: SessionDep
):
    return UserService(db).update_user(current_user.id, user_update)

@router.delete("/me")
def delete_account_me(current_user: CurrentUser, db: SessionDep):
    UserService(db).delete_user(current_user.id)
    return {"message": "User deleted"}