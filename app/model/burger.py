from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Burger(Base):
    __tablename__='Burger'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    ingredient = Column(String, index=True)
    sauce = Column(String, index=True)
    type = Column(String, unique=True)
    qualite = Column(Integer, nullable=False)
    note = Column(Integer, default=True)
    image = Column(String, default=True)