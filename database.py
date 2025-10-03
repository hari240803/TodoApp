from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

from urllib.parse import quote_plus

# Load .env variables
load_dotenv()

# Read components
# DB_USER = os.getenv("DB_USER")
DB_PASS = quote_plus(os.getenv("DB_PASS")) 
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# Build SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{DB_PASS}@localhost:5432/TodoAppDB"
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{DB_PASS}@127.0.0.1:3306/todoappdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()