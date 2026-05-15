from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate

# ✅ حساب end_date حسب الـ plan
def calculate_end_date(start_date: date, plan: str) -> date:
    if plan == "monthly":
        return start_date + timedelta(days=30)
    elif plan == "yearly":
        return start_date + timedelta(days=365)
    return start_date + timedelta(days=30)

# ✅ Auto-expire logic
def check_and_update_status(subscription: Subscription) -> str:
    if date.today() > subscription.end_date:
        return "expired"
    return "active"

def get_all_subscriptions(db: Session):
    subscriptions = db.query(Subscription).all()
    # Auto-update status
    for sub in subscriptions:
        new_status = check_and_update_status(sub)
        if new_status != sub.status:
            sub.status = new_status
            db.commit()
    return subscriptions

def get_subscription_by_id(db: Session, sub_id: int):
    return db.query(Subscription).filter(Subscription.id == sub_id).first()

def get_member_subscriptions(db: Session, member_id: int):
    return db.query(Subscription).filter(
        Subscription.member_id == member_id
    ).all()

def create_subscription(db: Session, sub: SubscriptionCreate):
    end_date = calculate_end_date(sub.start_date, sub.plan)
    new_sub = Subscription(
        member_id=sub.member_id,
        plan=sub.plan,
        start_date=sub.start_date,
        end_date=end_date,
        status="active"
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

def update_subscription(db: Session, sub_id: int, sub: SubscriptionUpdate):
    db_sub = get_subscription_by_id(db, sub_id)
    if not db_sub:
        return None
    if sub.plan:
        db_sub.plan = sub.plan
        db_sub.end_date = calculate_end_date(db_sub.start_date, sub.plan)
    if sub.start_date:
        db_sub.start_date = sub.start_date
        db_sub.end_date = calculate_end_date(sub.start_date, db_sub.plan)
    if sub.status:
        db_sub.status = sub.status
    db.commit()
    db.refresh(db_sub)
    return db_sub

def delete_subscription(db: Session, sub_id: int):
    db_sub = get_subscription_by_id(db, sub_id)
    if not db_sub:
        return None
    db.delete(db_sub)
    db.commit()
    return {"message": "Subscription deleted successfully"}

# ✅ Dashboard stats
def get_dashboard_stats(db: Session):
    all_subs = get_all_subscriptions(db)  # بيعمل auto-expire
    
    from app.models.member import Member
    total_members = db.query(Member).count()
    active_subs = db.query(Subscription).filter(
        Subscription.status == "active"
    ).count()
    expired_subs = db.query(Subscription).filter(
        Subscription.status == "expired"
    ).count()
    monthly_subs = db.query(Subscription).filter(
        Subscription.plan == "monthly"
    ).count()
    yearly_subs = db.query(Subscription).filter(
        Subscription.plan == "yearly"
    ).count()

    return {
        "total_members": total_members,
        "active_subscriptions": active_subs,
        "expired_subscriptions": expired_subs,
        "monthly_plans": monthly_subs,
        "yearly_plans": yearly_subs
    }
