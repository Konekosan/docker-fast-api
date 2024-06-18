import logging

from sqlalchemy.orm import Session
from app.model.usager import Usager
from app.schema.usager_schema import UsagerSchema
from app.auth.utils import hash_pass
from fastapi import HTTPException, status

loggers = logging.getLogger(__name__)

#Logger
def _print(text: str, log_level='info'):
    print(text)
    getattr(loggers, log_level)(text)

# Get users
def get_users(db:Session, skipt:int=0, limit:int=100):
    return db.query(Usager).offset(skipt).limit(limit).all()

# Get user by id
def fetch_user_by_id(db:Session, usager_id: int):
    return db.query(Usager).filter(Usager.id == usager_id).first()

# Get user by email
def fetch_user_by_username(db:Session, username: str):
    print('on passe la')
    return db.query(Usager).filter(Usager.username == username).first()

# Create user
def add_user(db:Session, user: UsagerSchema):
    _user = Usager(nom=user.nom, 
                   prenom=user.prenom, 
                   age=user.age,
                   username=user.username,
                   hashed_pwd=hash_pass(user.hashed_pwd),
                   is_active=True)
    db.add(_user)
    try:
        db.commit()
        db.refresh(_user)
        _print('Utilisateur ajouté avec succès ! ')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'ajout",
        )
    return _user

# Create user by id
def remove_user(db:Session, user: UsagerSchema):
    _user = fetch_user_by_id(db, user)

    try:
        db.delete(_user)
        _print('Utilisateur supprimé avec succès ! ')
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la supression",
        )

# Update user by id
def update_user(db:Session, usager_id:int, nom: str, prenom: str, age:int, username:str, hashed_pwd:str):
    _user = fetch_user_by_id(db, usager_id)
    _user.nom = nom
    _user.prenom = prenom
    _user.age = age
    _user.username = username
    _user.hashed_pwd = hash_pass(hashed_pwd)
    _user.is_active = True

    try:
        db.commit()
        _print('Utilisateur modifié avec succès ! ')
        db.refresh(_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la modification",
        )
    return _user

