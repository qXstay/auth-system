from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from models.user import User
from models.role import Role
from utils.security import hash_password, verify_password, create_access_token
from database.db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------- Schemas ----------------
class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role_id: int = 2  # По умолчанию роль "user"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# ---------------- Routes ----------------
@router.post("/register")
def register_user(data: RegisterSchema, db: Session = Depends(get_db)):
    # Проверка, что email ещё не зарегистрирован
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Проверка роли
    role = db.query(Role).filter(Role.id == data.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")

    # Создаём пользователя
    new_user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role_id=data.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "email": new_user.email, "role_id": new_user.role_id}


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account deactivated")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}