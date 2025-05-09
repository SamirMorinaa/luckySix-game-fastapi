from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect to the local PostgreSQL database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Provide a database session for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

