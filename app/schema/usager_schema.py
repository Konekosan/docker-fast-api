from typing import Optional, TypeVar, List
from pydantic import BaseModel, Field
from app.schema.roles_schemas import RoleSchema

class UsagerSchema(BaseModel):
    id: Optional[int]=None
    nom: Optional[str]=None
    prenom: Optional[str]=None
    age: Optional[int]=None
    username: Optional[str]=None
    hashed_pwd: Optional[str]=None
    is_active: Optional[bool]=None
    roles: List[RoleSchema]=[]

    class Config:
        orm_mode = True

class RequestUser(BaseModel):
    parameter: UsagerSchema = Field(...)
