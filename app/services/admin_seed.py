from sqlalchemy.orm import Session

from app.core.config import DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.user import User


def seed_default_admin() -> None:
    db: Session = SessionLocal()
    try:
        existing_admin = db.query(User).filter(
            User.username == DEFAULT_ADMIN_USERNAME
        ).first()
        if existing_admin:
            existing_admin.password = hash_password(DEFAULT_ADMIN_PASSWORD)
            existing_admin.role = "admin"
            db.commit()
            return

        admin = User(
            username=DEFAULT_ADMIN_USERNAME,
            password=hash_password(DEFAULT_ADMIN_PASSWORD),
            role="admin"
        )
        db.add(admin)
        db.commit()
    finally:
        db.close()
