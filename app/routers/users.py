from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models
from app.schemas import UserCreate, UserUpdate, UserOut
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


def _conflict(detail: str):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Uniqueness checks
    if db.query(models.User).filter(models.User.email == payload.email).first():
        _conflict("Email is already in use.")
    if db.query(models.User).filter(models.User.username == payload.username).first():
        _conflict("Username is already in use.")

    user = models.User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    search: Optional[str] = None,
):
    """
    List users with pagination.
    Optional search matches username OR email (contains).
    """
    q = db.query(models.User)

    if search:
        like = f"%{search}%"
        q = q.filter((models.User.username.ilike(like)) | (models.User.email.ilike(like)))

    users = q.order_by(models.User.id.asc()).limit(limit).offset(offset).all()
    return users


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Uniqueness checks if fields change
    if payload.email and payload.email != user.email:
        if db.query(models.User).filter(models.User.email == payload.email).first():
            _conflict("Email is already in use.")
        user.email = payload.email

    if payload.username and payload.username != user.username:
        if db.query(models.User).filter(models.User.username == payload.username).first():
            _conflict("Username is already in use.")
        user.username = payload.username

    if payload.password:
        user.hashed_password = hash_password(payload.password)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    db.delete(user)
    db.commit()
    return None