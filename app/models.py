from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class User(Base):
    __tablename__='User'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    age = Column(Integer, index=True)