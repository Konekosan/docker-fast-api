from typing import Optional
from pydantic import BaseModel, Field

class EtablissementSchema(BaseModel):
    id: Optional[int]=None
    nom: Optional[str]=None
    adresse: Optional[str]=None
    type: Optional[str]=None
    qualite: Optional[str]=None
    note: Optional[str]=None
    image: Optional[str]=None

    class Config:
        orm_mode = True


class RequestEtablissement(BaseModel):
    parameter: EtablissementSchema = Field(...)