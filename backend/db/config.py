import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
#from db.config import db

# Load environment variables
load_dotenv()

# 🔇 Silence SQLAlchemy logs
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Database config
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
