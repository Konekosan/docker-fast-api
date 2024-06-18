from app.database import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

class Etablissement(Base):
    __tablename__='Etablissement'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    adresse = Column(String, index=True)
    type = Column(String, index=True)
    qualite = Column(String, index=True)
    note = Column(Integer, nullable=False)
    image = Column(String, default='')
    revues = relationship('Revue', back_populates='etablissement')
