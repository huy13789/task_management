from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Output
class ColumnBase(BaseModel):
    title: str
    position: int

# Output
class ColumnResponse(ColumnBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Input
class ColumnCreate(BaseModel):
    title: str
    board_id: int

# Input - schema update title và thay đổi vị trí column
class ColumnUpdate(BaseModel):
    title: Optional[str] = None
    position: Optional[int] = Field(None, ge=0)
