import logging

from sqlalchemy.orm import Session
from app.models import User
from app.schema.user_schema import UserSchema

loggers = logging.getLogger(__name__)

#Logger
def _print(text: str, log_level='info'):
    print(text)
    getattr(loggers, log_level)(text)

# Get users
def get_users(db:Session, skipt:int=0, limit:int=100):
    return db.query(User).offset(skipt).limit(limit).all()

# Get user by id
def fetch_user_by_id(db:Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Create user
def add_user(db:Session, user: UserSchema):
    _user = User(nom=user.nom, prenom=user.prenom, age=user.age)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    _print('Utilisateur ajouté avec succès ! ')
    return _user

# Create user by id
def remove_user(db:Session, user: UserSchema):
    _user = fetch_user_by_id(db, user.id)
    db.delete(_user)
    _print('Utilisateur supprimé avec succès ! ')
    db.commit()

# Update user by id
def update_user(db:Session, user_id:int, nom: str, prenom: str, age:int):
    _user = fetch_user_by_id(db, user_id)
    _user.nom = nom
    _user.prenom = prenom
    _user.age = age
    db.commit()
    _print('Utilisateur modifié avec succès ! ')
    db.refresh(_user)
    return _user

