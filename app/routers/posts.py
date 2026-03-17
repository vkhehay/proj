from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, database, schema, oauth2

Post = models.Post
Vote = models.Vote
get_db = database.get_db
PostCreate = schema.PostCreate
PostResponse = schema.PostResponse
PostVote = schema.PostVote
get_current_user = oauth2.get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


def find_post(post_id: int, db: Session, current_user: int):
    post_query = db.query(Post).filter(Post.id == post_id)
    print(post_query)
    user_id = db.query(Post.user_id).filter(Post.user_id == current_user).first()[0]
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    if post_query.first().user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no such post")

    return post_query, db


@router.get('/', response_model=List[PostVote])
# @router.get('/', status_code=status.HTTP_201_CREATED, response_model=List[PostResponse])
def post(db: Session = Depends(get_db),
         current_user: int = Depends(get_current_user),
         search: Optional[str] = None,
         limit: int = 5,
         skip: int = 0):
    # query = db.query(app.models.Post).filter(app.models.Post.user_id == current_user)
    # if search:
    #     query = query.filter(app.models.Post.contains(search))
    #
    # post = query.limit(limit).offset(skip).all()

    query = (db.query(Post, func.count(Vote.post_id).label("votes"))
             .join(Vote, Vote.post_id == Post.id, isouter=True)
             .group_by(Post.id))

    if search:
        query = query.filter(Post.contains(search))
    # post = query.limit(limit).offset(skip).all()
    post_query = query.order_by(Post.id).all()

    response = [PostVote(post=post_res, votes=votes) for post_res, votes in post_query]
    return response
    # return post


# @router.get('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
@router.get('/{post_id}', status_code=status.HTTP_202_ACCEPTED, response_model=PostVote)
# router path/{post_id} should be corresponded with argument in function get_id(post_id)
def get_id(post_id: int, db: Session = Depends(get_db),
           current_user: int = Depends(get_current_user)):
    # post_query, _ = find_post(post_id, db, current_user)
    query = (db.query(Post, func.count(Vote.post_id).label("votes"))
             .join(Vote, Vote.post_id == Post.id, isouter=True)
             .group_by(Post.id))
    post_query = query.filter(Post.id == post_id).first()
    print(post_query)
    if post_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

    response = PostVote(post=post_query[0], votes=post_query[1])
    return response
    # return post_query.first()


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
# router path/{post_id} should be corresponded with argument in function delete_post(post_id)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    post_query, db_session = find_post(post_id, db, current_user)
    post_query.delete(synchronize_session=False)
    db_session.commit()
    return {"message": f"post {id} was deleted"}


@router.put('/{post_id}', status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
# router path/{post_id} should be corresponded with argument in function updated_post(post_id)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    post_query, db_session = find_post(post_id, db, current_user)
    post_query.update(post.model_dump(), synchronize_session=False)
    db_session.commit()
    check_result, _ = find_post(post_id, db, current_user)
    return check_result.first()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post_create: PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    new_post = Post(user_id=current_user, **post_create.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
