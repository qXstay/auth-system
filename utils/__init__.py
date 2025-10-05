from database.db import SessionLocal
from models.user import User
from .security import verify_password, create_access_token, hash_password

def get_user_by_email(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    finally:
        db.close()