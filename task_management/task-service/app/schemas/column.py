from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from .card import CardResponse


# Output
class ColumnBase(BaseModel):
    title: str
    position: int

# Output
class ColumnResponse(ColumnBase):
    id: int
    created_at: datetime

    cards: List[CardResponse]

    class Config:
        from_attributes = True

# Input
class ColumnCreate(BaseModel):
    title: str
    board_id: int

# Input - schema update title và thay đổi vị trí column
class ColumnUpdate(BaseModel):
    title: Optional[str] = None
    new_index: Optional[int] = None
    position: Optional[float] = None
