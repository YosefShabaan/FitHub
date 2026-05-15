from sqlalchemy.orm import Session
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate

def get_all_members(db: Session):
    return db.query(Member).all()

def get_member_by_id(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

def search_members(db: Session, query: str):
    return db.query(Member).filter(
        Member.name.ilike(f"%{query}%") |
        Member.phone.ilike(f"%{query}%")
    ).all()

def create_member(db: Session, member: MemberCreate):
    new_member = Member(
        name=member.name,
        phone=member.phone,
        email=member.email
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def update_member(db: Session, member_id: int, member: MemberUpdate):
    db_member = get_member_by_id(db, member_id)
    if not db_member:
        return None
    if member.name: db_member.name = member.name
    if member.phone: db_member.phone = member.phone
    if member.email: db_member.email = member.email
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = get_member_by_id(db, member_id)
    if not db_member:
        return None
    db.delete(db_member)
    db.commit()
    return {"message": "Member deleted successfully"}
