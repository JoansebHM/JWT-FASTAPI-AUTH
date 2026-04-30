import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Annotated
from fastapi import Depends

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


DbDep = Annotated[Session, Depends(get_db)]


class Base(DeclarativeBase):
    pass
