from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
# 1. Import BaseModel
from pydantic import BaseModel 

from ..db import get_db
from ..core.jwt import decode_access_token 

security = HTTPBearer()
SessionDep = Annotated[Session, Depends(get_db)]

# 2. Định nghĩa Schema cho Token Payload
class TokenPayload(BaseModel):
    id: int
    sub: str # Email

async def get_current_user(
    token_obj: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenPayload:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = token_obj.credentials
    payload = decode_access_token(token) # Trả về Dict
    
    if payload is None:
        raise credentials_exception

    # 4. Validate và chuyển Dict thành Object
    try:
        token_data = TokenPayload(**payload)
    except Exception:
        raise credentials_exception
    
    return token_data

# Type Alias
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]