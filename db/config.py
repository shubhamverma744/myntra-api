import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Read the DB URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Setup database engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Declarative base for all models
Base = declarative_base()
