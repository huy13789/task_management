from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from ..models.task import BoardVisibility

class ColumnResponse(BaseModel):
    id: int
    title: str
    position: int
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BoardBase(BaseModel):
    title: str
    visibility: BoardVisibility = BoardVisibility.PRIVATE
    background: Optional[str] = None


class BoardCreate(BoardBase):
    pass


class BoardResponse(BoardBase):
    id: int
    owner_id: int
    is_closed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BoardDetailResponse(BoardResponse):
    columns: List[ColumnResponse] = []