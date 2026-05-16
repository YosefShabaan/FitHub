from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PortalJoinRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    plan: str


class PortalJoinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: int
    subscription_id: int
    name: str
    phone: str
    email: Optional[str]
    plan: str
    start_date: date
    end_date: date
    status: str
