import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# set SQLALCHEMY_DATABASE_URL=postgresql://postgres:Evox@127.0.0.1:5555/evox
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
