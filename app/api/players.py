# app/api/players.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.player  import PlayerCreate, PlayerOut, PlayerUpdate
from app.core.database   import get_db
from app.core.security   import hash_password, get_current_user
from app.models.player   import Player as PlayerModel

player_router = APIRouter()

@player_router.post("/", response_model=PlayerOut)
def register_player(user: PlayerCreate, db: Session = Depends(get_db)):
    if db.query(PlayerModel).filter(
        (PlayerModel.username == user.username) |
        (PlayerModel.email == user.email)
    ).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username or email already registered")
    db_user = PlayerModel(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@player_router.get("/me", response_model=PlayerOut)
def read_profile(current: PlayerModel = Depends(get_current_user)):
    return current

@player_router.put("/me", response_model=PlayerOut)
def update_profile(
    data: PlayerUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user),
):
    if not data.email and not data.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No data to update")
    if data.email:
        current.email = data.email
    if data.password:
        current.password = hash_password(data.password)
    db.commit()
    db.refresh(current)
    return current
