from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import SessionLocal
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse
from app.services.member_service import (
    get_all_members,
    get_member_by_id,
    search_members,
    create_member,
    update_member,
    delete_member
)
from app.services.auth_service import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Get all members
@router.get("/", response_model=List[MemberResponse])
def list_members(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return get_all_members(db)


# ✅ Search members
@router.get("/search", response_model=List[MemberResponse])
def search(
    query: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return search_members(db, query)


# ✅ Get member by ID
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


# ✅ Add new member
@router.post("/", response_model=MemberResponse)
def add_member(
    member: MemberCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return create_member(db, member)


# ✅ Update member
@router.put("/{member_id}", response_model=MemberResponse)
def edit_member(
    member_id: int,
    member: MemberUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    updated = update_member(db, member_id, member)
    if not updated:
        raise HTTPException(status_code=404, detail="Member not found")
    return updated


# ✅ Delete member
@router.delete("/{member_id}")
def remove_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    result = delete_member(db, member_id)
    if not result:
        raise HTTPException(status_code=404, detail="Member not found")
    return result
