from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import schemas, utils, oauth2
from app.db import models
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.db.сonnection import get_db

router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        database: Session = Depends(get_db)):

    user = database.query(models.User).filter(models.User.email
                                              == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid data')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid data')

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
