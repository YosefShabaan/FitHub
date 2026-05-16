from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: Optional[str]
    created_at: datetime
