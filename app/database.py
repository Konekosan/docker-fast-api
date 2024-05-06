from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres123@postgre_db:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()