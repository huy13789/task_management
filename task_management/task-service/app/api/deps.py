from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status
import jwt
from ..db import get_db
from ..core.config import settings

security = HTTPBearer()
SessionDep = Annotated[Session, Depends(get_db)]

def get_current_user_id(
    token_obj: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = token_obj.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("id")

        if user_id is None:
            raise credentials_exception

        return user_id
    except jwt.InvalidTokenError:
        raise credentials_exception

CurrentUser = Annotated[int, Depends(get_current_user_id)]