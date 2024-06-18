import logging

from sqlalchemy.orm import Session
from app.model.etablissement import Etablissement
from app.schema.etablissement_schema import EtablissementSchema
from fastapi import HTTPException, status
from sqlalchemy import func, desc
from app.model.revue import Revue

loggers = logging.getLogger(__name__)

#Logger
def _print(text: str, log_level='info'):
    print(text)
    getattr(loggers, log_level)(text)

# Get etablissement
def get_etablissement(db:Session, skipt:int=0, limit:int=100):
    return db.query(Etablissement).offset(skipt).limit(limit).all()

# Calculer la moyenne des notes par etablissements
def get_average_note_per_etablissement(db: Session):
    try:
        results = db.query(
            Etablissement.id,
            Etablissement.nom,
            Etablissement.adresse,
            Etablissement.image,
            func.round(func.avg(Revue.note),2).label('note_moyenne'),
            func.count(Revue.note).label('nombre_notes')
        ).join(Revue, Etablissement.id == Revue.etablissement_id).group_by(Etablissement.id).order_by(desc(('note_moyenne'))).all()
        
        list_avg = [
            {
                "id": result.id,
                "nom": result.nom,
                "adresse": result.adresse,
                "image": result.image,
                "note_moyenne": float(result.note_moyenne),
                "nombre_notes": result.nombre_notes
            }
            for result in results
        ]
        return list_avg
    
    except Exception as e:
        _print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du calcul",
        )

# Create etablissement
def add_etablissement(db:Session, etablissement: EtablissementSchema):
    _etablissement = Etablissement(
                   nom=etablissement.nom, 
                   adresse=etablissement.adresse, 
                   type=etablissement.type,
                   qualite=etablissement.qualite,
                   note=etablissement.note,
                   image=etablissement.image)
    print(_etablissement)
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