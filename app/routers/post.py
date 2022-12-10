from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, utils
from ..database import get_db, engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# @router.get('/', response_model=List[schemas.PostResponse])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # curser.execute("""SELECT * FROM posts""")
    # posts = curser.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() ## For same user posts only

    return result


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_new_post(post_body: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curser.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post_body.title, post_body.content, post_body.published))
    # new_post = curser.fetchone()
    # connect.commit()
    print(current_user.email)
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post_body.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curser.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = curser.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with id: {id}")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # curser.execute(
    #     """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = curser.fetchone()
    # connect.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with id: {id}")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Forbidden Request!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # curser.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = curser.fetchone()
    # connect.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No data found with id: {id}")

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Forbidden Request!")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
