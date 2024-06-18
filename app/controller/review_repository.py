import logging

from sqlalchemy.orm import Session
from app.model.etablissement import Etablissement
from app.model.revue import Revue
from fastapi import HTTPException, status
from app.schema.revue_schemas import RevueSchema

loggers = logging.getLogger(__name__)

#Logger
def _print(text: str, log_level='info'):
    print(text)
    getattr(loggers, log_level)(text)

# Get review
def get_review(db:Session, skipt:int=0, limit:int=100):
    return db.query(Revue).offset(skipt).limit(limit).all()

# Create review
def create_review(db:Session, revue: RevueSchema):
    _review = Revue(
                   usager_id=revue.usager_id,
                   etablissement_id=revue.etablissement_id,
                   note=revue.note)
    db.add(_review)
    try:
        db.commit()
        db.refresh(_review)
        _print('Revue ajouté avec succès !')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'ajout",
        )
    return _review
