from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Output
class CardBase(BaseModel):
    title: str
    description: Optional[str] = None

# Input
class CardCreate(CardBase):
    column_id: int

#Output
class CardResponse(CardBase):
    id: int
    column_id: int
    position: int
    is_archived: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Input
class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    new_index: Optional[int] = None
    column_id: Optional[int] = None
    position: Optional[float] = None

# Input
class CardAssignmentCreate(BaseModel):
    user_id: int

# Output
class CardAssignmentResponse(BaseModel):
    card_id: int
    user_id: int
    role: str
    assigned_at: datetime

    class Config:
        from_attributes = True