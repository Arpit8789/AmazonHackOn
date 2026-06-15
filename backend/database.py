import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The user-provided NeonDB connection string
import os
from dotenv import load_dotenv

load_dotenv()

# We replace postgresql:// with postgresql+psycopg2:// for SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://neondb_owner:npg_0GcTRvtpC5MS@ep-still-lake-atep79xe.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our models to inherit from
Base = declarative_base()

# Dependency to get DB session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
