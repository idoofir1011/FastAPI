from ..schemas import PostBase, PostOut, PostWithVotes
from .. import models, oauth2
from fastapi import FastAPI, HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostWithVotes])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .order_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    mapped_results = []
    for post, votes in results:
        post_pydantic = PostOut.model_validate(post)
        mapped_results.append({"Post": post_pydantic, "votes": votes})
    return mapped_results


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostBase,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    print(user_id)
    db_post = models.Post(owner_id=user_id.id, **post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/{id}", response_model=PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = (
    #     db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    #     .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    #     .filter(models.Post.id == id)
    #     .first()
    # )
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    post, votes = results
    post_pydantic = PostOut.model_validate(post)
    return {"Post": post_pydantic, "votes": votes}


@router.put("/{id}", response_model=PostOut)
def update_post(
    id: int,
    post: PostBase,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    print(user_id)
    db_post = db.query(models.Post).filter(models.Post.id == id)
    existing_post = db_post.first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if existing_post.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to preform this action!",
        )
    db_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    print(user_id)
    db_post = db.query(models.Post).filter(models.Post.id == id)
    post = db_post.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if post.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to preform this action!",
        )
    db.delete(post)
    db.commit()
    return None
