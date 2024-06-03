from typing import Optional, TypeVar
from pydantic import BaseModel, Field

class BurgerSchema(BaseModel):
    id: Optional[int]=None
    nom: Optional[str]=None
    ingredient: Optional[str]=None
    sauce: Optional[str]=None
    type: Optional[str]=None
    qualite: Optional[str]=None
    note: Optional[str]=None
    image: Optional[str]=None

    class Config:
        orm_mode = True


class RequestBurgerSchema(BaseModel):
    parameter: BurgerSchema = Field(...)