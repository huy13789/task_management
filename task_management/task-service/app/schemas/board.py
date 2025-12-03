from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from ..models.task import BoardVisibility
from .column import ColumnResponse

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