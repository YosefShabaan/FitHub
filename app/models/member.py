from sqlalchemy import Column, Integer, String, DateTime
from datetime import UTC, datetime
from app.db.database import Base


def utc_now():
    return datetime.now(UTC)

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=utc_now)
