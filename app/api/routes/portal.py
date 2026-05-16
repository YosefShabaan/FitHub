from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.member import Member
from app.models.subscription import Subscription
from app.schemas.portal import PortalJoinRequest, PortalJoinResponse
from app.services.subscription_service import calculate_end_date

router = APIRouter()


@router.post("/join", response_model=PortalJoinResponse)
def join_membership(
    request: PortalJoinRequest,
    db: Session = Depends(get_db)
):
    plan = request.plan.lower().strip()
    if plan not in {"monthly", "yearly"}:
        raise HTTPException(status_code=400, detail="Plan must be monthly or yearly")

    name = request.name.strip()
    phone = request.phone.strip()
    email = request.email.strip().lower() if request.email else None

    if not name or not phone:
        raise HTTPException(status_code=400, detail="Name and phone are required")

    duplicate_filters = [Member.phone == phone]
    if email:
        duplicate_filters.append(Member.email == email)

    existing_member = db.query(Member).filter(or_(*duplicate_filters)).first()
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="A member with this phone or email already exists"
        )

    start_date = date.today()
    end_date = calculate_end_date(start_date, plan)

    member = Member(name=name, phone=phone, email=email)
    db.add(member)
    db.flush()

    subscription = Subscription(
        member_id=member.id,
        plan=plan,
        start_date=start_date,
        end_date=end_date,
        status="active"
    )
    db.add(subscription)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="A member with this phone or email already exists"
        )

    db.refresh(member)
    db.refresh(subscription)

    return PortalJoinResponse(
        member_id=member.id,
        subscription_id=subscription.id,
        name=member.name,
        phone=member.phone,
        email=member.email,
        plan=subscription.plan,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        status=subscription.status
    )
