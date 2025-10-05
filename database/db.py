from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Здесь указаны тестовые данные для проверки, вы делаете свои
DATABASE_URL = "postgresql://auth_user:MyAuthPass123@localhost/auth_system_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Функция для dependency injection в FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()