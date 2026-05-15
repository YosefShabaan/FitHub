from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemberCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class MemberResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
