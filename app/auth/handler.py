from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.tokens import verify_token, create_access_token
from app.router import get_db
from app.model.token import TokenEnum
from app.schema.auth_schemas import RefreshTokenResponseSchema, RefreshTokenRequestSchema
from app.schema.auth_schemas import TokenData


auth_router = APIRouter()

@auth_router.get("/refresh-token")
def refresh_token():
    #access_token = create_access_token(data={"user_id": token_data.id})

    return {'message': 'Hello World'}

@auth_router.post("/refresh-token")
def refresh_token(payload: RefreshTokenRequestSchema, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid Token")
    token_data: TokenData = verify_token(payload.refresh_token, credentials_exception)

    if token_data.token_kind != TokenEnum.RefreshToken:
        raise credentials_exception

    access_token = create_access_token(data={"user_id": token_data.id})

    return RefreshTokenResponseSchema(access_token=access_token, token_type="bearer")


@auth_router.post("/refresh-tokens")
def refresh_tokens(payload: RefreshTokenRequestSchema, db: Session = Depends(get_db)):
    return 1
    credentials_exception = HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid Token")
    token_data: TokenData = verify_token(payload.refresh_token, credentials_exception)

    if token_data.token_kind != TokenEnum.RefreshToken:
        raise credentials_exception

    access_token = create_access_token(data={"user_id": token_data.id})

    return RefreshTokenResponseSchema(access_token=access_token, token_type="bearer")