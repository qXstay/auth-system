from sqlalchemy.orm import Session
from models.user import User
from models.role import Role
from utils.security import hash_password
from database.db import SessionLocal

def create_user_if_not_exists(first_name, last_name, email, password, role_name="user"):
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return existing
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            raise Exception(f"Role {role_name} not found")
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=hash_password(password),
            role_id=role.id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()