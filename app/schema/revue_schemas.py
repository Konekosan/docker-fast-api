from typing import Optional
from pydantic import BaseModel, Field

class RevueSchema(BaseModel):
    id: Optional[int]=None
    usager_id: Optional[int]=None
    etablissement_id: Optional[int]=None
    note: Optional[int]=None

    class Config:
        orm_mode = True


class RequestRevue(BaseModel):
    parameter: RevueSchema = Field(...)