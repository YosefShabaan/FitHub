from pydantic import BaseModel
from datetime import date
from typing import Optional

class SubscriptionCreate(BaseModel):
    member_id: int
    plan: str  # monthly / yearly
    start_date: date

class SubscriptionUpdate(BaseModel):
    plan: Optional[str] = None
    start_date: Optional[date] = None
    status: Optional[str] = None

class SubscriptionResponse(BaseModel):
    id: int
    member_id: int
    plan: str
    start_date: date
    end_date: date
    status: str

    class Config:
        from_attributes = True
