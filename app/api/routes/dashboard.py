from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.subscription_service import get_dashboard_stats
from app.services.auth_service import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Dashboard stats
@router.get("/stats")
def dashboard(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return get_dashboard_stats(db)
