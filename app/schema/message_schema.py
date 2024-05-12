from typing import List, Optional
from pydantic import BaseModel, Field


class UsagerMessage(BaseModel):
    id: Optional[int]=None
    message: Optional[str]=None

    class Config:
        orm_mode = True


def test_message (test) -> dict:
    return  {
       'id': str(test['_id']),
       'utilisateur': str(test['utilisateur']),
       'message': str(test['message']),
       'description': str(test['description']),
    }


def list_test(tests) -> list:
    return[test_message(test) for test in tests]