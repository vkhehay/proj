from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, database, schema, oauth2

# import app.app.models
# from app.app.database import get_db
# from app.app.schema import VoteMessage
# from app.app.oauth2 import get_current_user

VoteMessage = schema.VoteMessage
VoteResponse = schema.VoteResponse
get_db = database.get_db
Post = models.Post
Vote = models.Vote
get_current_user = oauth2.get_current_user

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=VoteMessage)
def vote_post(vote: VoteResponse, db: Session = Depends(get_db),
              current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    query = (db.query(Vote)
             .filter(Vote.post_id == vote.post_id, Vote.user_id == current_user))
    found_vote = query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have voted on this post")
        new_vote = Vote(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        return {"message": "You have successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote was deleted"}
