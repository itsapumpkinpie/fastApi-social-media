from fastapi import status, HTTPException, Response, Depends, APIRouter
from app.db.сonnection import get_db
from app.db import models
from app import schemas, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def read_posts(
        database: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    post = database.query(models.Post).filter(models.Post.user_id == current_user.id).all()

    return post


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_posts(
        post: schemas.PostCreate, database: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    database.add(new_post)
    database.commit()
    database.refresh(new_post)
    return new_post


@router.get("/{id}")
def get_post(
        id: int, database: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    post = database.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'failed to find post with id {id}',
        )
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int, database: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    post = database.query(models.Post).filter(models.Post.id == id)
    post_query = post.first()

    if post_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')

    if post_query.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post.delete(synchronize_session=False)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(
        id: int,
        updated_post: schemas.PostCreate,
        database: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
):
    post_query = database.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_query.update(updated_post.dict(), synchronize_session=False)
    database.commit()
    return post_query.first()
