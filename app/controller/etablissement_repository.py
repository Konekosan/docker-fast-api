import logging

from sqlalchemy.orm import Session
from app.model.etablissement import Etablissement
from app.schema.etablissement_schema import EtablissementSchema
from fastapi import HTTPException, status

loggers = logging.getLogger(__name__)

#Logger
def _print(text: str, log_level='info'):
    print(text)
    getattr(loggers, log_level)(text)

# Get etablissement
def get_etablissement(db:Session, skipt:int=0, limit:int=100):
    return db.query(Etablissement).offset(skipt).limit(limit).all()

# Create etablissement
def add_etablissement(db:Session, etablissement: EtablissementSchema):
    _etablissement = Etablissement(
                   nom=etablissement.nom, 
                   adresse=etablissement.adresse, 
                   type=etablissement.type,
                   qualite=etablissement.qualite,
                   note=etablissement.note,
                   image=etablissement.image)

    db.add(_etablissement)
    try:
        db.commit()
        db.refresh(_etablissement)
        _print('Etablissement ajouté avec succès !')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'ajout",
        )
    return _etablissement