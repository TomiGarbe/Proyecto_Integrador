# Configuración de PostgreSQL con SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./env.config")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()