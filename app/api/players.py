from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, get_current_user
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerOut
from app.models.player import Player

player_router = APIRouter(prefix="/players", tags=["players"])

@player_router.post("/", response_model=PlayerOut)
def register_player(
    data: PlayerCreate,
    db: Session = Depends(get_db),
):
    if db.query(Player).filter(
        (Player.username == data.username) | (Player.email == data.email)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    user = Player(
        username=data.username,
        email=data.email,
        password=get_password_hash(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@player_router.get("/me", response_model=PlayerOut)
def read_profile(current_user: Player = Depends(get_current_user)):
    return current_user

@player_router.put("/me", response_model=PlayerOut)
def update_profile(
    data: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    if not data.email and not data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided"
        )
    if data.email:
        current_user.email = data.email
    if data.password:
        current_user.password = get_password_hash(data.password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
