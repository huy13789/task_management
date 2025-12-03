# user-service/app/routers/login.py

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from ..schemas.user import TokenResponse, UserLogin
from ..api.deps import SessionDep 
from ..services.auth_service import AuthService

router = APIRouter(tags=["Authentication"])

@router.post("/auth/login", response_model=TokenResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def login_for_access_token(login_data: UserLogin, db: SessionDep):
    return AuthService(db).login_user(login_data)