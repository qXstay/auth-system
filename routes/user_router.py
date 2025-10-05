from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from utils.security import hash_password, verify_password
from pydantic import BaseModel, EmailStr
from typing import Optional
from middlewares.authorization import check_permission

router = APIRouter()

# ---------------- Current User ----------------
def get_current_user(request: Request) -> User:
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

# ---------------- Schemas ----------------
class UpdateUserSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    current_password: str

# ---------------- Routes ----------------
@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role_id": current_user.role_id
    }

@router.get("/all")
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_permission(current_user, element="users", action="read", db=db)
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role_id": user.role_id,
            "is_active": user.is_active
        } for user in users
    ]

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.delete("/me")
def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.is_active = False
    db.commit()
    return {"message": "User account deactivated"}

@router.patch("/me")
def update_current_user(
    data: UpdateUserSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect current password")

    if data.first_name:
        current_user.first_name = data.first_name
    if data.last_name:
        current_user.last_name = data.last_name
    if data.email:
        # Проверяем, что email не занят другим пользователем
        existing_user = db.query(User).filter(User.email == data.email, User.id != current_user.id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already taken")
        current_user.email = data.email
    if data.password:
        current_user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(current_user)

    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email
    }