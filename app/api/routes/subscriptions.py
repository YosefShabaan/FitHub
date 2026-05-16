from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionResponse
)
from app.services.subscription_service import (
    get_all_subscriptions,
    get_subscription_by_id,
    get_member_subscriptions,
    create_subscription,
    update_subscription,
    delete_subscription
)
from app.services.auth_service import get_current_user

router = APIRouter()


# ✅ Get all subscriptions
@router.get("/", response_model=List[SubscriptionResponse])
def list_subscriptions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return get_all_subscriptions(db)


# ✅ Get subscriptions by member
@router.get("/member/{member_id}", response_model=List[SubscriptionResponse])
def member_subscriptions(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return get_member_subscriptions(db, member_id)


# ✅ Get subscription by ID
@router.get("/{sub_id}", response_model=SubscriptionResponse)
def get_subscription(
    sub_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    sub = get_subscription_by_id(db, sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub


# ✅ Create subscription
@router.post("/", response_model=SubscriptionResponse)
def add_subscription(
    sub: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return create_subscription(db, sub)


# ✅ Update subscription
@router.put("/{sub_id}", response_model=SubscriptionResponse)
def edit_subscription(
    sub_id: int,
    sub: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    updated = update_subscription(db, sub_id, sub)
    if not updated:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return updated


# ✅ Delete subscription
@router.delete("/{sub_id}")
def remove_subscription(
    sub_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    result = delete_subscription(db, sub_id)
    if not result:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return result
