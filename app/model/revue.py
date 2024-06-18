from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from app.model.usager import Usager
#from app.model.burger import Burger
from app.model.etablissement import Etablissement

class Revue(Base):
    __tablename__='Revue'

    id = Column(Integer, primary_key=True, index=True)
    usager_id = Column(Integer, ForeignKey('Usager.id'), nullable=False)
    etablissement_id = Column(Integer, ForeignKey('Etablissement.id'), nullable=False)
    note = Column(Float,  index=True, nullable=False)

    usager = relationship('Usager', back_populates='revues')
    etablissement = relationship('Etablissement', back_populates='revues')
