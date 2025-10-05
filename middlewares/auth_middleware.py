from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session, joinedload
from utils.security import decode_access_token
from models.user import User
from database.db import SessionLocal

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        request.state.user = None
        if token and token.startswith("Bearer "):
            token_value = token[7:]
            payload = decode_access_token(token_value)
            if payload:
                user_id = payload.get("user_id")
                db: Session = SessionLocal()
                try:
                    # Используем joinedload для загрузки роли вместе с пользователем
                    user = db.query(User).options(joinedload(User.role)).filter(User.id == user_id).first()
                    if user and user.is_active:
                        request.state.user = user
                finally:
                    db.close()
        response = await call_next(request)
        return response