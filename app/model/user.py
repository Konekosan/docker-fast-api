from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database import Base

class Test(Base):
    __tablename__='TUser'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    age = Column(Integer, index=True)