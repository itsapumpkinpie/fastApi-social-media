from fastapi import status, Depends, APIRouter, HTTPException
from app import schemas, utils
from app.db import models
from app.db.сonnection import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Users']
)


@router.post(
    "/create_user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SignUpResponse
)
def register(user: schemas.User, database: Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


@router.get("/users/{id}",
            response_model=schemas.SignUpResponse
)
def get_user(id: int, database: Session = Depends(get_db)):

    user = database.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id:{id} does not exist')

    return user
